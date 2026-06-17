#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PGX / GB10 LLM benchmark (ollama API, stdlib-only) — v3 2026-06

Použití:
  python3 bench.py pull
  python3 bench.py run --runs 3
  python3 bench.py run --runs 1 --models "qwen3.6,gemma4" --max-ctx 128k
  python3 bench.py summary

DŮLEŽITÉ — Flash Attention se zapíná na straně serveru, ne tady. Pusť:
  sudo systemctl stop ollama 2>/dev/null
  OLLAMA_FLASH_ATTENTION=1 OLLAMA_MAX_LOADED_MODELS=1 OLLAMA_NUM_PARALLEL=1 ollama serve
Skript si tyto proměnné přečte a zapíše do bench_meta.json + summary (žádné lživé tvrzení o konfiguraci).

Fragilní modely (paměť): mistral-medium-3.5:128b a nemotron-3-super:120b běž SAMOSTATNĚ,
naposledy, s krátkým kontextem a po `sudo sh -c 'sync; echo 3 > /proc/sys/vm/drop_caches'`.

Thinking/reasoning je VYPNUTÉ (think:false) u všech modelů → srovnatelné TTFT/decode napříč
modely a funkční grading jehel. Modely bez podpory thinking si skript ošetří (zkusí to bez něj).
"""
import argparse, csv, json, os, statistics, subprocess, sys, time
import urllib.request, urllib.error
import uuid

OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
DISABLE_THINKING = True  # vypnout reasoning/thinking u všech modelů (srovnatelnost TTFT + funkční grading)

# === MODELY (pořadí = stoupající paměťová náročnost; fragilní giganti naposledy) ===
MODELS = [
    ("llama3.1:8b",             "Llama 3.1 8B · dense · Q4_K_M"),
    ("gemma4:e4b",              "Gemma 4 E4B · edge · Q4_K_M"),
    ("gpt-oss:20b",             "gpt-oss 20B · MoE · MXFP4"),
    ("mistral-small3.2:24b",    "Mistral Small 3.2 24B · dense · Q4_K_M"),
    ("qwen3.6:27b",             "Qwen 3.6 27B · dense · Q4_K_M"),
    ("gemma4:31b",              "Gemma 4 31B · dense · Q4_K_M"),
    ("qwen3.6:35b-a3b",         "Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M"),
    ("llama3.3:70b",            "Llama 3.3 70B · dense · Q4_K_M"),
    ("gpt-oss:120b",            "gpt-oss 120B · MoE · MXFP4"),
    ("mistral-medium-3.5:128b", "Mistral Medium 3.5 128B · dense · Q4_K_M"),
    ("nemotron-3-super:120b",   "Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M"),
    # ("qwen3.6:35b-a3b-coding-nvfp4", "…")  # Mac/MLX-only, na GB10 v ollama nejede
]

# === STROP KONTEXTU NA MODEL (zabraňuje tichému ořezu „256k", co by jinak protekl jako falešná data) ===
MODEL_MAX_CTX = {
    "llama3.1:8b": 131072,
    "gemma4:e4b": 131072,
    "gpt-oss:20b": 131072,
    "mistral-small3.2:24b": 131072,
    "qwen3.6:27b": 262144,
    "gemma4:31b": 262144,
    "qwen3.6:35b-a3b": 262144,
    "llama3.3:70b": 131072,
    "gpt-oss:120b": 131072,
    "mistral-medium-3.5:128b": 262144,   # umí 256K, ale na 128GB GB10 nejspíš OOM nad ~32–64k → pouštěj s --max-ctx
    "nemotron-3-super:120b": 262144,
}
DEFAULT_MAX_CTX = 131072  # konzervativní default pro neznámé modely

# === KONTEXTY ===
CONTEXTS = [
    ("0.5k-chat", 400,    2048),
    ("8k",        6600,   8192),
    ("32k",       27000,  32768),
    ("64k",       55000,  65536),
    ("128k",      105000, 131072),
    ("256k",      205000, 262144),
]

NUM_PREDICT = 512
CSV_PATH, JSONL_PATH, META_PATH = "results.csv", "results.jsonl", "bench_meta.json"

def measured_num_predict():
    # s vypnutým thinkingem stačí 512; se zapnutým reasoning sežere budget → zvedneme, ať dorazí i odpověď (jehly)
    return NUM_PREDICT if DISABLE_THINKING else max(NUM_PREDICT, 2048)

# === NEUTRÁLNÍ VÝPLŇ (žádná smyšlená fakta o reálných modelech — bezpečné pro publikaci) ===
DOCS = [
    "Společnost zpracovává citlivá zákaznická data výhradně na serverech umístěných v Evropské unii v souladu s GDPR a zákonem č. 110/2019 Sb.",
    "Oddělení compliance požaduje, aby veškeré zpracování probíhalo na hardware umístěném v členských státech Evropské unie a aby byly operace logovány.",
    "Provozním rizikem lokálního nasazení je nutnost pravidelné aktualizace, správy infrastruktury a zajištění kybernetické bezpečnosti.",
    "Roční rozpočet na infrastrukturu se schvaluje na poradě vedení, přičemž větší výdaje vyžadují souhlas finančního ředitele.",
    "Smluvní dokumentace se archivuje po dobu deseti let a podléhá pravidelnému internímu auditu kvality a úplnosti.",
    "Přístup k produkčním systémům je řízen rolemi a dvoufaktorovým ověřením; změny prochází schvalovacím procesem.",
    "Zákaznická podpora eviduje požadavky v interním systému a u citlivých témat eskaluje na příslušné oddělení.",
    "Plán kontinuity provozu počítá s pravidelným testováním obnovy ze zálohy a s definovanými cíli doby obnovy.",
]

# Jehly = neutrální, s UNIKÁTNÍM markerem pro automatické hodnocení retrievalu (začátek/střed/konec)
NEEDLE_A = ("\n\n[ZÁZNAM A] Interní aktivační kód pilotního projektu je QX-7741-ZN a platí do konce čtvrtletí.", "QX-7741-ZN")
NEEDLE_B = ("\n\n[ZÁZNAM B] Záložní uzel infrastruktury je v dokumentaci veden pod označením lokality D-12.", "D-12")
NEEDLE_C = ("\n\n[ZÁZNAM C] Maximální povolená doba odezvy podle interní směrnice je 350 milisekund.", "350")
NEEDLES = [NEEDLE_A, NEEDLE_B, NEEDLE_C]

QUESTION = (
    "\n\nOdpověz stručně a přesně, u každé otázky uveď přesnou hodnotu:\n"
    "1. Jaký je interní aktivační kód pilotního projektu?\n"
    "2. Pod jakým označením lokality je veden záložní uzel?\n"
    "3. Jaká je maximální povolená doba odezvy podle směrnice (v ms)?"
)

def build_prompt(target_tokens: int, nonce: str = "") -> str:
    """Více dokumentů + jehly na různých pozicích. Obsah neutrální; měříme rychlost + zda model jehly najde.
    `nonce` na úplném začátku = unikátní prefix → ollama nemůže recyklovat KV cache → reálný prefill/TTFT."""
    target_chars = int(target_tokens * 3.0)  # CZ ~3–3.6 znaku/token; raději mírně podhodnotit, ať nepřetečeme num_ctx
    block = "\n\n".join(DOCS)
    reps = max(2, target_chars // (len(block) + 160))
    parts = []
    for i in range(reps):
        parts.append(block)
        if i % 3 == 1:
            parts.append(f"Dodatečná interní směrnice č. {2025 + i}: veškeré operace se logují a podléhají revizi oddělení compliance.")
    context = "\n\n".join(parts)
    mid = len(context) // 2
    full = (nonce + NEEDLE_A[0] + "\n\n" + context[:mid] + "\n\n" +
            NEEDLE_B[0] + "\n\n" + context[mid:] + "\n\n" +
            NEEDLE_C[0] + QUESTION)
    return full

def grade_needles(text: str) -> str:
    """Hrubá kontrola retrievalu: kolik ze 3 unikátních markerů je v odpovědi. Nikdy nespadne."""
    if not text:
        return ""
    hits = sum(1 for _, marker in NEEDLES if marker in text)
    return f"{hits}/3"

def _post(path, body, timeout=7200):
    req = urllib.request.Request(OLLAMA + path, data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read())

def _think_val():
    return False if DISABLE_THINKING else None

def _build_body(model, prompt, num_ctx, num_predict, keep_alive, stream):
    body = {"model": model, "prompt": prompt, "stream": stream, "keep_alive": keep_alive,
            "options": {"num_ctx": num_ctx, "num_predict": num_predict, "temperature": 0, "seed": 42}}
    tv = _think_val()
    if tv is not None:
        body["think"] = tv          # top-level param ollama; modely bez podpory ošetří _open_generate
    return body

def _is_thinking_error(e):
    try:
        msg = e.read().decode("utf-8", "ignore").lower()
    except Exception:
        msg = str(e).lower()
    return "think" in msg

def _open_generate(body, timeout=7200):
    """Otevře /api/generate; pokud model nepodporuje 'think', zopakuje dotaz bez něj."""
    def _do(b):
        req = urllib.request.Request(OLLAMA + "/api/generate", data=json.dumps(b).encode(),
                                     headers={"Content-Type": "application/json"})
        return urllib.request.urlopen(req, timeout=timeout)
    try:
        return _do(body)
    except urllib.error.HTTPError as e:
        if "think" in body and _is_thinking_error(e):
            b2 = dict(body); b2.pop("think", None)
            return _do(b2)
        raise

def gen(model, prompt, num_ctx, num_predict=NUM_PREDICT, keep_alive="30m"):
    """Non-streaming (warmup)."""
    body = _build_body(model, prompt, num_ctx, num_predict, keep_alive, stream=False)
    t0 = time.time()
    with _open_generate(body) as r:
        d = json.loads(r.read())
    d["_wall_s"] = round(time.time() - t0, 2)
    return d

def gen_stream_metrics(model, prompt, num_ctx, num_predict=NUM_PREDICT, keep_alive="30m"):
    """Streaming s měřením TTFT + akumulací textu (pro grading jehel)."""
    body = _build_body(model, prompt, num_ctx, num_predict, keep_alive, stream=True)
    t0 = time.time()
    first_token_ts = None
    final_stats = {}
    text_parts = []
    with _open_generate(body) as r:
        for line in r:
            if not line.strip():
                continue
            chunk = json.loads(line)
            if first_token_ts is None and "response" in chunk:
                first_token_ts = time.time() - t0
            if "response" in chunk:
                text_parts.append(chunk.get("response", ""))
            if chunk.get("done"):
                final_stats = chunk
                break
    return {
        "prompt_eval_count": final_stats.get("prompt_eval_count", 0),
        "prompt_eval_duration": final_stats.get("prompt_eval_duration", 0),
        "eval_count": final_stats.get("eval_count", 0),
        "eval_duration": final_stats.get("eval_duration", 0),
        "load_duration": final_stats.get("load_duration", 0),
        "_ttft_s": round(first_token_ts, 3) if first_token_ts else None,
        "_wall_s": round(time.time() - t0, 2),
        "_text": "".join(text_parts),
    }

def unload(model):
    try:
        _post("/api/generate", {"model": model, "prompt": "", "keep_alive": 0, "stream": False}, timeout=120)
    except Exception:
        pass

def mem_gb(model):
    """Footprint z ollama /api/ps. Na GB10 jde o UNIFIED paměť, ne VRAM. Přesný match → fallback na prefix."""
    try:
        with urllib.request.urlopen(OLLAMA + "/api/ps", timeout=30) as r:
            models = json.loads(r.read()).get("models", [])
        for m in models:
            if m.get("name", "") == model:
                return round(m.get("size_vram", m.get("size", 0)) / 1e9, 1)
        for m in models:
            if m.get("name", "").startswith(model):
                return round(m.get("size_vram", m.get("size", 0)) / 1e9, 1)
    except Exception:
        pass
    return ""

def mem_avail_gb():
    """Volná systémová paměť (OOM canary) z /proc/meminfo — relevantní na unified memory."""
    try:
        for line in open("/proc/meminfo"):
            if line.startswith("MemAvailable:"):
                return round(int(line.split()[1]) / 1024 / 1024, 1)  # kB → GB
    except Exception:
        pass
    return ""

def get_gpu_info():
    try:
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total,driver_version", "--format=csv,noheader"],
                             capture_output=True, text=True, timeout=15).stdout.strip()
        return out.split("\n")[0] if out else "?"
    except Exception:
        return "?"

def _server_env():
    """Přečte OLLAMA_* proměnné SKUTEČNÉHO běžícího serveru z /proc/<pid>/environ.
    Funguje i při systemd (kde shell skriptu ty proměnné nemá). Fallback: prázdno."""
    out, pid = {}, None
    try:
        r = subprocess.run(["systemctl", "show", "ollama", "-p", "MainPID", "--value"],
                           capture_output=True, text=True, timeout=10).stdout.strip()
        if r.isdigit() and int(r) > 0:
            pid = r
    except Exception:
        pass
    if not pid:
        try:
            r = subprocess.run(["pgrep", "-f", "ollama serve"], capture_output=True, text=True, timeout=10).stdout.split()
            pid = r[0] if r else None
        except Exception:
            pass
    if pid:
        try:
            with open(f"/proc/{pid}/environ", "rb") as f:
                for kv in f.read().split(b"\x00"):
                    if b"=" in kv:
                        k, v = kv.decode("utf-8", "ignore").split("=", 1)
                        if k.startswith("OLLAMA_"):
                            out[k] = v
        except Exception:
            pass
    return out

def env_flags():
    keys = ["OLLAMA_FLASH_ATTENTION", "OLLAMA_KV_CACHE_TYPE", "OLLAMA_NUM_PARALLEL", "OLLAMA_MAX_LOADED_MODELS"]
    srv = _server_env()  # reálné prostředí serveru má přednost před shellem skriptu
    return {k: (srv.get(k) or os.environ.get(k, "")) for k in keys}

def write_meta():
    meta = {"ts": time.strftime("%F %T"), "host": OLLAMA, "gpu": get_gpu_info(),
            "flags": env_flags(), "think_disabled": DISABLE_THINKING,
            "num_predict": measured_num_predict()}
    try:
        with urllib.request.urlopen(OLLAMA + "/api/version", timeout=10) as r:
            meta["ollama"] = json.loads(r.read()).get("version", "?")
    except Exception:
        meta["ollama"] = "?"
    json.dump(meta, open(META_PATH, "w"), indent=2)
    print("meta:", meta)
    if not meta["flags"].get("OLLAMA_FLASH_ATTENTION"):
        print("  ⚠ OLLAMA_FLASH_ATTENTION není nastaveno — summary to uvede čestně (nelži o FA v blogu).")

FIELDS = ["ts", "model", "label", "ctx", "num_ctx", "run", "prompt_tok", "gen_tok", "needles_ok",
          "prefill_tps", "decode_tps", "ttft_s", "prompt_s", "gen_s", "load_s", "wall_s",
          "mem_gb", "error"]

def append_row(row):
    new = not os.path.exists(CSV_PATH)
    with open(CSV_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if new:
            w.writeheader()
        w.writerow(row)
    with open(JSONL_PATH, "a") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def ns(d, k):
    return d.get(k, 0) or 0

def do_run(runs, model_filter=None, max_ctx=None):
    write_meta()

    active_models = MODELS
    if model_filter:
        wanted = [m.strip() for m in model_filter.split(",")]
        active_models = [m for m in MODELS if m[0] in wanted or any(w in m[0] for w in wanted)]

    active_contexts = CONTEXTS
    if max_ctx:
        mc = max_ctx.lower().strip()
        max_val = int(mc[:-1]) * 1024 if mc.endswith("k") else int(mc)
        active_contexts = [c for c in CONTEXTS if c[2] <= max_val]

    total_cfg = len(active_models) * len(active_contexts) * runs
    print(f"Matice: {len(active_models)} modelů x {len(active_contexts)} kontextů x {runs} běhů = {total_cfg} měření (+ warmupy).")
    print("Pozor na čas: malé modely jednotky minut/měření; 70B/120B/128B na 128k–256k klidně 10–40 min/měření → celý běh jednotky až desítky hodin.\n")

    for tag, label in active_models:
        print(f"=== {label} ({tag}) ===", flush=True)
        ceiling = MODEL_MAX_CTX.get(tag, DEFAULT_MAX_CTX)

        try:
            w = gen(tag, "Odpověz jedním slovem: ahoj.", 2048, num_predict=16)
            load_s = round(ns(w, "load_duration") / 1e9, 2)
            print(f" cold load: {load_s}s | volná RAM po loadu: {mem_avail_gb()} GB | strop kontextu: {ceiling}", flush=True)
        except Exception as e:
            print(f" !! load selhal: {e} — přeskakuji model", flush=True)
            append_row({"ts": time.strftime("%F %T"), "model": tag, "label": label, "ctx": "-",
                        "num_ctx": "", "run": 0, "error": str(e)[:200],
                        **{k: "" for k in FIELDS if k not in ("ts", "model", "label", "ctx", "num_ctx", "run", "error")}})
            continue

        for ctx_label, target, num_ctx in active_contexts:
            # Per-model strop: kontext nad schopnosti modelu vůbec nepouštíme (jinak tichý ořez = falešná data)
            if num_ctx > ceiling:
                print(f"  [{ctx_label}] přeskočeno — model nepodporuje {num_ctx} (strop {ceiling})", flush=True)
                continue

            if num_ctx > 8192:
                try:
                    _ = gen(tag, "Shrň následující text.", num_ctx, num_predict=32)
                    print(f"  warmup {ctx_label} OK", flush=True)
                except Exception as we:
                    print(f"  warmup {ctx_label} selhal: {we}", flush=True)

            for r in range(1, runs + 1):
                nonce = f"[REF-{uuid.uuid4().hex[:10]}]\n"   # unikátní prefix každý běh → reálný prefill/TTFT
                prompt = build_prompt(target, nonce=nonce)
                row = {"ts": time.strftime("%F %T"), "model": tag, "label": label,
                       "ctx": ctx_label, "num_ctx": num_ctx, "run": r, "error": ""}
                try:
                    d = gen_stream_metrics(tag, prompt, num_ctx, num_predict=measured_num_predict())
                    pe_c, pe_d = ns(d, "prompt_eval_count"), ns(d, "prompt_eval_duration")
                    ev_c, ev_d = ns(d, "eval_count"), ns(d, "eval_duration")
                    ttft = d.get("_ttft_s", "")
                    row.update({
                        "prompt_tok": pe_c, "gen_tok": ev_c,
                        "needles_ok": grade_needles(d.get("_text", "")),
                        "prefill_tps": round(pe_c / pe_d * 1e9, 1) if pe_d else "",
                        "decode_tps": round(ev_c / ev_d * 1e9, 1) if ev_d else "",
                        "ttft_s": ttft,
                        "prompt_s": round(pe_d / 1e9, 2), "gen_s": round(ev_d / 1e9, 2),
                        "load_s": round(ns(d, "load_duration") / 1e9, 2), "wall_s": d["_wall_s"],
                        "mem_gb": mem_gb(tag) if r == 1 else "",
                    })
                    print(f" [{ctx_label} #{r}] prompt {pe_c} tok | prefill {row['prefill_tps']} t/s | "
                          f"decode {row['decode_tps']} t/s | TTFT {ttft}s | jehly {row['needles_ok']}", flush=True)
                except Exception as e:
                    err = str(e)[:400]
                    row["error"] = err
                    for k in FIELDS:
                        row.setdefault(k, "")
                    # OOM / kontext → přeskoč zbytek běhů tohoto kontextu (u OOM zvaž --max-ctx níž)
                    if any(x in err.lower() for x in ["context", "exceeds", "too large", "maximum", "memory", "oom", "alloc"]):
                        print(f"  [{ctx_label}] chyba kontext/paměť → přeskakuji zbývající běhy: {err}", flush=True)
                        append_row(row)
                        break
                    print(f" [{ctx_label} #{r}] CHYBA: {err}", flush=True)
                append_row(row)

        unload(tag)
        time.sleep(5)

    print(f"\nHotovo -> {CSV_PATH}, {JSONL_PATH}. Souhrn: python3 bench.py summary")

def do_summary():
    if not os.path.exists(CSV_PATH):
        sys.exit("results.csv neexistuje — nejdřív `run`.")
    meta = {}
    if os.path.exists(META_PATH):
        try:
            meta = json.load(open(META_PATH))
        except Exception:
            pass

    groups = {}
    with open(CSV_PATH) as f:
        for row in csv.DictReader(f):
            if row["error"] or not row["decode_tps"]:
                continue
            groups.setdefault((row["model"], row["label"], row["ctx"]), []).append(row)

    order_m = {t: i for i, (t, _) in enumerate(MODELS)}
    order_c = {c: i for i, (c, _, _) in enumerate(CONTEXTS)}

    flags = meta.get("flags", {})
    fa = flags.get("OLLAMA_FLASH_ATTENTION") or "nenastaveno (default)"
    kv = flags.get("OLLAMA_KV_CACHE_TYPE") or "f16 (default)"

    print("## LLM benchmark — lokální inference na GB10 (Blackwell)\n")
    print(f"**Hardware:** {meta.get('gpu', 'N/A')}  |  **Ollama:** {meta.get('ollama', 'N/A')}  |  **Datum:** {meta.get('ts', 'N/A')}\n")

    print("### Výsledky\n")
    print("| Model | Kontext | Prompt tok | Prefill t/s | Decode t/s | TTFT s | Paměť GB | Decode/GB | Jehly |")
    print("|---|---|---|---|---|---|---|---|---|")

    for (tag, label, ctx), rows in sorted(groups.items(),
            key=lambda kv_: (order_m.get(kv_[0][0], 99), order_c.get(kv_[0][2], 99))):
        def safe_med(key):
            vals = [float(r[key]) for r in rows if r.get(key) not in (None, "", "None")]
            return round(statistics.median(vals), 1) if vals else ""
        ptok = safe_med("prompt_tok")
        mem = next((r["mem_gb"] for r in rows if r.get("mem_gb")), "")
        prefill, decode, ttft = safe_med("prefill_tps"), safe_med("decode_tps"), safe_med("ttft_s")
        needles = next((r["needles_ok"] for r in rows if r.get("needles_ok")), "")
        eff = round(float(decode) / float(mem), 2) if decode and mem and float(mem) > 0 else ""
        print(f"| {label} | {ctx} | {ptok} | {prefill} | {decode} | {ttft} | {mem} | {eff} | {needles} |")

    print("\n### Metodika")
    print("- Hodnoty = medián z opakovaných běhů; TTFT měřeno přes streaming")
    think_txt = "vypnuto (think:false)" if meta.get("think_disabled") else "ponecháno (default modelu)"
    npred = meta.get("num_predict", 512)
    print(f"- Flash Attention: {fa} · KV cache: {kv} · num_predict={npred} · temperature=0 · seed=42")
    print(f"- Thinking/reasoning: {think_txt} → srovnatelné TTFT a decode napříč modely")
    print("- Paměť (GB) = footprint z `ollama ps`; na GB10 jde o UNIFIED paměť, ne VRAM")
    print("- Decode/GB = decode tok/s na 1 GB paměti (vyšší = efektivnější)")
    print("- Jehly = retrieval test: kolik ze 3 unikátních faktů model v odpovědi našel (hrubá kontrola, ne plný scoring)")
    print("- Kontexty nad schopnosti modelu se nepouští (žádný tichý ořez); chyby vyfiltrovány")
    print("- Každý běh má unikátní prefix (nonce) → měří se reálný prefill/TTFT, ne cache hit")
    print("- Příkon NENÍ z nvidia-smi (na unified vrací N/A) — doplň ručně z wattmetru")
    print("\n**Detaily:** `results.csv` + `results.jsonl` | Meta: `bench_meta.json`")
    print("\n*Běželo na lokálním hardware bez přístupu k externím API.*")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pull")
    p_run = sub.add_parser("run")
    p_run.add_argument("--runs", type=int, default=3)
    p_run.add_argument("--models", type=str, help="Čárkou oddělené tagy nebo části názvů (např. qwen3.6,gemma4)")
    p_run.add_argument("--max-ctx", type=str, help="Maximální kontext (např. 64k, 128k)")
    p_run.add_argument("--think", action="store_true",
                       help="Zapnout reasoning/thinking (default: vypnuto kvůli srovnatelnosti). Zvedne i num_predict.")
    sub.add_parser("summary")
    a = ap.parse_args()
    if a.cmd == "pull":
        for tag, _ in MODELS:
            print(f"== ollama pull {tag} ==", flush=True)
            subprocess.run(["ollama", "pull", tag])
    elif a.cmd == "run":
        if a.think:
            DISABLE_THINKING = False   # reassign globálu (běží v __main__ scope) → _think_val/meta/num_predict ho přečtou
        do_run(a.runs, model_filter=a.models, max_ctx=a.max_ctx)
    else:
        do_summary()
