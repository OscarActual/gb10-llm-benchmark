#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bench_embed.py — embedding benchmark pro ČESKÁ RAG data (ollama /api/embed, stdlib-only)

Měří dvě věci:
  1) PROPUSTNOST: dim, docs/s (dávka), ms/dotaz (latence)
  2) KVALITA CZ RETRIEVALU: recall@1, recall@5, MRR na malém syntetickém českém korpusu
     (parafrázové dotazy → testuje sémantiku, ne shodu klíčových slov)

Použití:
  python3 bench_embed.py pull
  python3 bench_embed.py run
  python3 bench_embed.py run --models "bge-m3,qwen3-embedding"

Pozn.: kvalita je HRUBÝ signál na ~12 dotazech, ne plný MTEB. Reranking se netestuje.
Prefixy se aplikují tam, kde je model očekává (e5, nomic, qwen3-instruct) — jinak by skóre kleslo.
"""
import argparse, json, math, os, statistics, subprocess, sys, time
import urllib.request, urllib.error

OLLAMA = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")

MODELS = [
    ("bge-m3",                  "BGE-M3 · 568M · hybrid · multiling."),
    ("embeddinggemma",          "EmbeddingGemma 300M · multiling."),
    ("qwen3-embedding:0.6b",    "Qwen3-Embedding 0.6B"),
    ("qwen3-embedding:4b",      "Qwen3-Embedding 4B"),
    ("qwen3-embedding:8b",      "Qwen3-Embedding 8B"),
    ("snowflake-arctic-embed2", "Snowflake Arctic Embed 2 · multiling."),
    ("jeffh/intfloat-multilingual-e5-large-instruct:f16",   "Multilingual E5 Large"),
    ("nomic-embed-text",        "Nomic Embed Text · EN-leaning"),
    ("mxbai-embed-large",       "mxbai Embed Large · EN-leaning"),
    ("all-minilm",              "all-MiniLM · baseline EN"),
]

# (query_prefix, doc_prefix) tam, kde to model očekává; jinak prázdné
PREFIX = {
    "jeffh/intfloat-multilingual-e5-large-instruct:f16": ("Instruct: Najdi pasáž odpovídající na dotaz.\nQuery: ", ""),
    "nomic-embed-text": ("search_query: ", "search_document: "),
    "qwen3-embedding:0.6b": ("Instruct: Najdi pasáž odpovídající na dotaz.\nQuery: ", ""),
    "qwen3-embedding:4b":   ("Instruct: Najdi pasáž odpovídající na dotaz.\nQuery: ", ""),
    "qwen3-embedding:8b":   ("Instruct: Najdi pasáž odpovídající na dotaz.\nQuery: ", ""),
}

# === SYNTETICKÝ ČESKÝ KORPUS (0–11 = cílové pasáže, 12–15 = distraktory) ===
CHUNKS = [
    "Citlivá zákaznická data se zpracovávají výhradně na serverech v Evropské unii v souladu s GDPR.",          # 0
    "Smluvní dokumentace se archivuje po dobu deseti let a podléhá pravidelnému internímu auditu.",             # 1
    "Přístup k produkčním systémům je chráněn dvoufaktorovým ověřením a řízen podle rolí uživatelů.",           # 2
    "Plán kontinuity provozu počítá s pravidelným testováním obnovy ze zálohy a s cíli doby obnovy.",           # 3
    "Měsíční náklady na inferenci výrazně klesly po přechodu z externího API na lokální modely.",               # 4
    "Větší investice do infrastruktury schvaluje finanční ředitel na poradě vedení společnosti.",               # 5
    "Zákaznická podpora eviduje požadavky a citlivá témata eskaluje na příslušné odborné oddělení.",            # 6
    "Společnost provozuje vlastní open-source stack pro automatizaci interních procesů.",                       # 7
    "Lokální nasazení modelů vyžaduje pravidelné aktualizace a správu grafických karet.",                       # 8
    "Faktury se vystavují v účetním systému a automaticky se párují s bankovními výpisy.",                       # 9
    "Vývojové prostředí je odděleno od produkčního a veškeré změny procházejí schvalovacím procesem.",          # 10
    "Komunikace s klienty z regulovaných oborů podléhá přísné mlčenlivosti a důvěrnosti.",                      # 11
    "Firemní kavárna nabízí zaměstnancům filtrovanou kávu dováženou z Indonésie.",                              # 12 distraktor
    "Roční teambuilding se tradičně koná na horách začátkem prosince.",                                         # 13 distraktor
    "Parkovací místa před budovou jsou rezervovaná pro návštěvy a klienty.",                                    # 14 distraktor
    "Recepce přebírá zásilky v pracovní dny od osmi do šestnácti hodin.",                                       # 15 distraktor
]

# (dotaz, index správné pasáže) — parafráze, malý lexikální překryv
QUERIES = [
    ("Kde se podle pravidel ukládají osobní údaje klientů?", 0),
    ("Jak dlouho firma uchovává podepsané smlouvy?", 1),
    ("Jak je zabezpečené přihlašování do ostrých systémů?", 2),
    ("Jak se ověřuje, že zálohy skutečně fungují?", 3),
    ("Co se stalo s výdaji po nasazení vlastní AI?", 4),
    ("Kdo schvaluje dražší nákupy hardwaru?", 5),
    ("Co se děje s choulostivými dotazy zákazníků?", 6),
    ("Jakými nástroji firma automatizuje procesy?", 7),
    ("Co je potřeba udržovat při provozu vlastních modelů?", 8),
    ("Jak probíhá zpracování plateb a vystavování dokladů?", 9),
    ("Jak jsou oddělené testovací a ostré systémy?", 10),
    ("Jaká pravidla platí pro důvěrnost u klientů z regulovaných odvětví?", 11),
]

def embed(model, inputs, timeout=600):
    body = {"model": model, "input": inputs}
    req = urllib.request.Request(OLLAMA + "/api/embed", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        d = json.loads(r.read())
    return d.get("embeddings", [])

def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a))
    nb = math.sqrt(sum(y * y for y in b))
    return dot / (na * nb) if na and nb else 0.0

def mem_gb(model):
    try:
        with urllib.request.urlopen(OLLAMA + "/api/ps", timeout=30) as r:
            for m in json.loads(r.read()).get("models", []):
                if m.get("name", "") == model or m.get("name", "").startswith(model):
                    return round(m.get("size_vram", m.get("size", 0)) / 1e9, 1)
    except Exception:
        pass
    return ""

def bench_model(tag, label):
    qp, dp = PREFIX.get(tag, ("", ""))
    # warmup (load) — nepočítá se do propustnosti
    try:
        _ = embed(tag, ["test"])
    except urllib.error.HTTPError as e:
        return {"tag": tag, "label": label, "error": f"HTTP {e.code} (model nejspíš není stažený)"}
    except Exception as e:
        return {"tag": tag, "label": label, "error": str(e)[:160]}

    # propustnost: dávkové embedování korpusu
    t0 = time.time()
    doc_vecs = embed(tag, [dp + c for c in CHUNKS])
    dt = time.time() - t0
    if not doc_vecs or not doc_vecs[0]:
        return {"tag": tag, "label": label, "error": "prázdná embeddings odpověď"}
    dim = len(doc_vecs[0])
    docs_per_s = round(len(CHUNKS) / dt, 1) if dt > 0 else ""

    # latence dotazu (medián) + kvalita
    lat, ranks = [], []
    for q, gold in QUERIES:
        t = time.time()
        qv = embed(tag, [qp + q])[0]
        lat.append((time.time() - t) * 1000)
        order = sorted(range(len(CHUNKS)), key=lambda i: cosine(qv, doc_vecs[i]), reverse=True)
        ranks.append(order.index(gold) + 1)

    n = len(ranks)
    recall1 = round(sum(1 for r in ranks if r == 1) / n, 2)
    recall5 = round(sum(1 for r in ranks if r <= 5) / n, 2)
    mrr = round(sum(1.0 / r for r in ranks) / n, 3)
    return {"tag": tag, "label": label, "dim": dim, "docs_s": docs_per_s,
            "ms_q": round(statistics.median(lat), 1), "r1": recall1, "r5": recall5,
            "mrr": mrr, "mem": mem_gb(tag), "error": ""}

def do_run(model_filter=None):
    active = MODELS
    if model_filter:
        wanted = [m.strip() for m in model_filter.split(",")]
        active = [m for m in MODELS if m[0] in wanted or any(w in m[0] for w in wanted)]

    rows = []
    for tag, label in active:
        print(f"=== {label} ({tag}) ===", flush=True)
        res = bench_model(tag, label)
        if res.get("error"):
            print(f"  PŘESKOČENO: {res['error']}", flush=True)
        else:
            print(f"  dim {res['dim']} | {res['docs_s']} docs/s | {res['ms_q']} ms/dotaz | "
                  f"recall@1 {res['r1']} | recall@5 {res['r5']} | MRR {res['mrr']} | {res['mem']} GB", flush=True)
        rows.append(res)
        try:
            urllib.request.urlopen(urllib.request.Request(
                OLLAMA + "/api/generate", data=json.dumps({"model": tag, "keep_alive": 0}).encode(),
                headers={"Content-Type": "application/json"}), timeout=60)
        except Exception:
            pass

    ok = [r for r in rows if not r.get("error")]
    ok.sort(key=lambda r: (r["r1"], r["mrr"]), reverse=True)

    print("\n## Embedding benchmark — česká RAG data (GB10)\n")
    print(f"Korpus: {len(CHUNKS)} pasáží ({len(QUERIES)} cílových + {len(CHUNKS)-len(QUERIES)} distraktorů) · "
          f"{len(QUERIES)} parafrázových dotazů\n")
    print("| Model | Dim | docs/s | ms/dotaz | recall@1 | recall@5 | MRR | Paměť GB |")
    print("|---|---|---|---|---|---|---|---|")
    for r in ok:
        print(f"| {r['label']} | {r['dim']} | {r['docs_s']} | {r['ms_q']} | {r['r1']} | {r['r5']} | {r['mrr']} | {r['mem']} |")
    skipped = [r for r in rows if r.get("error")]
    if skipped:
        print("\nPřeskočeno:")
        for r in skipped:
            print(f"- {r['label']} ({r['tag']}): {r['error']}")
    print("\n### Metodika")
    print("- recall@1/@5 + MRR z parafrázových CZ dotazů (sémantické vyhledání, ne shoda slov)")
    print("- Prefixy aplikovány u modelů, které je očekávají (e5-instruct Instruct/Query, nomic search_*, qwen3 Instruct)")
    print("- docs/s = dávkové embedování korpusu (warm); ms/dotaz = medián latence jednoho dotazu")
    print("- HRUBÝ signál na malém setu — pro produkci doplnit větším CZ retrieval datasetem + rerankerem")
    print("- Běželo lokálně přes ollama /api/embed, bez externích API")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("pull")
    p_run = sub.add_parser("run")
    p_run.add_argument("--models", type=str, help="Čárkou oddělené tagy/části názvů")
    a = ap.parse_args()
    if a.cmd == "pull":
        for tag, _ in MODELS:
            print(f"== ollama pull {tag} ==", flush=True)
            subprocess.run(["ollama", "pull", tag])
    else:
        do_run(model_filter=a.models)
