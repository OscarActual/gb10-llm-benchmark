#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
recheck_gptoss.py — definitivní recheck gpt-oss retrievalu jehel.

Řeší dvě věci, které původní bench nemohl:
  1) gpt-oss IGNORUJE bool think:false → v obou bězích jel na defaultním 'medium'.
     Tady posíláme reasoning effort jako STRING (low/medium/high), jak gpt-oss vyžaduje.
  2) Hrubý substring grád mohl podhodnotit "našel, ale napsal jinak" → gradujeme i NORMALIZOVANĚ
     (malá písmena, bez mezer/pomlček) a kontrolujeme i text MYŠLENÍ.

Spouštět ze složky repa (vedle bench.py).
  python3 recheck_gptoss.py
  python3 recheck_gptoss.py --ctxs 8k,64k,128k --efforts high --num-predict 8192

Výstup: tabulka na stdout + plné odpovědi do souboru (na ověření/citaci).
"""
import argparse, json, re, uuid
import urllib.request, urllib.error
import bench  # build_prompt, NEEDLES, CONTEXTS, OLLAMA

def numctx(label):
    for cl, t, nc in bench.CONTEXTS:
        if cl == label or cl.startswith(label):
            return t, nc
    n = int(label[:-1]) * 1024 if label.lower().endswith("k") else int(label)
    return int(n * 0.8), n

def norm(s):
    return re.sub(r'[^a-z0-9]', '', s.lower())

def grade_norm(text):
    n = norm(text)
    return sum(1 for _, m in bench.NEEDLES if norm(m) in n)

def grade_strict(text):
    return sum(1 for _, m in bench.NEEDLES if m in text)

def run_one(model, ctx, effort, num_predict):
    target, nc = numctx(ctx)
    prompt = bench.build_prompt(target, nonce=f"[REF-{uuid.uuid4().hex[:10]}]\n")
    body = {"model": model, "prompt": prompt, "stream": True, "keep_alive": "30m",
            "think": effort,  # STRING — gpt-oss ignoruje bool
            "options": {"num_ctx": nc, "num_predict": num_predict, "temperature": 0, "seed": 42}}
    req = urllib.request.Request(bench.OLLAMA + "/api/generate", data=json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    think, resp, final = [], [], {}
    with urllib.request.urlopen(req, timeout=7200) as r:
        for line in r:
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("thinking"):
                think.append(c["thinking"])
            if c.get("response"):
                resp.append(c["response"])
            if c.get("done"):
                final = c
                break
    return "".join(think), "".join(resp), final

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gpt-oss:20b,gpt-oss:120b")
    ap.add_argument("--ctxs", default="64k,128k")
    ap.add_argument("--efforts", default="low,medium,high")
    ap.add_argument("--num-predict", type=int, default=4096)
    ap.add_argument("--out", default="gptoss_recheck_answers.txt")
    a = ap.parse_args()
    models = [x.strip() for x in a.models.split(",")]
    ctxs = [x.strip() for x in a.ctxs.split(",")]
    efforts = [x.strip() for x in a.efforts.split(",")]

    rows = []
    fout = open(a.out, "w")
    for model in models:
        for ctx in ctxs:
            for eff in efforts:
                print(f"=== {model} @ {ctx} · effort={eff} ===", flush=True)
                try:
                    think, resp, final = run_one(model, ctx, eff, a.num_predict)
                except urllib.error.HTTPError as e:
                    msg = e.read().decode("utf-8", "ignore")[:150]
                    print(f"   HTTP CHYBA: {msg}", flush=True)
                    continue
                except Exception as e:
                    print(f"   CHYBA: {str(e)[:150]}", flush=True)
                    continue
                gen = final.get("eval_count", 0) or 0
                strict, ng, nt = grade_strict(resp), grade_norm(resp), grade_norm(think)
                trunc = gen >= a.num_predict
                rows.append((model, ctx, eff, gen, strict, ng, nt, trunc))
                print(f"   gen_tok={gen} | strict_ans={strict}/3 | norm_ans={ng}/3 | "
                      f"in_thinking={nt}/3 | truncated={'ANO' if trunc else 'ne'}", flush=True)
                fout.write(f"\n{'='*72}\n{model} @ {ctx} · effort={eff} (gen_tok={gen}, truncated={trunc})\n"
                           f"--- THINKING ({len(think)} zn.) ---\n{think.strip()[:2000]}\n"
                           f"--- ANSWER ---\n{resp.strip()}\n")
    fout.close()

    print("\n## gpt-oss needle recheck\n")
    print("| Model | Ctx | Effort | gen_tok | strict | normalized | in_thinking | truncated |")
    print("|---|---|---|---:|---|---|---|---|")
    for m, c, e, g, s, ng, nt, tr in rows:
        print(f"| {m} | {c} | {e} | {g} | {s}/3 | {ng}/3 | {nt}/3 | {'yes' if tr else 'no'} |")
    print(f"\nPlné odpovědi: `{a.out}`")
    print("- **strict** = doslovný marker v odpovědi · **normalized** = po sjednocení (malá písmena, bez mezer/pomlček)")
    print("- **in_thinking** = jehla nalezena v reasoningu (i když ne v odpovědi)")
    print("- Čtení: norm > strict ⇒ artefakt grádu · in_thinking vysoké + norm nízké ⇒ našel, ale nedal do odpovědi/truncated · obojí nízké ⇒ reálné selhání retrievalu")

if __name__ == "__main__":
    main()
