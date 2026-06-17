#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inspect_answer.py — vypíše PLNÉ myšlení + odpověď jednoho modelu na daném kontextu.

Slouží k ověření, jestli model jehlu reálně našel — proti hrubému substring grádu v bench.py.
Typické použití (gpt-oss recheck):
  python3 inspect_answer.py gpt-oss:120b --ctx 64k
  python3 inspect_answer.py gpt-oss:120b --ctx 64k --think     # s nativním reasoningem
"""
import argparse, json, uuid
import urllib.request, urllib.error
import bench  # reuse build_prompt, NEEDLES, CONTEXTS, _build_body, _open_generate, OLLAMA

def ctx_to_numctx(label):
    for cl, target, nc in bench.CONTEXTS:
        if cl == label or cl.startswith(label):
            return target, nc
    n = int(label[:-1]) * 1024 if label.lower().endswith("k") else int(label)
    return int(n * 0.8), n

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("model")
    ap.add_argument("--ctx", default="64k", help="např. 0.5k-chat, 32k, 64k, 128k")
    ap.add_argument("--think", action="store_true", help="zapnout nativní reasoning")
    a = ap.parse_args()

    target, num_ctx = ctx_to_numctx(a.ctx)
    bench.DISABLE_THINKING = not a.think     # řídí, zda se pošle think:false
    nonce = f"[REF-{uuid.uuid4().hex[:10]}]\n"
    prompt = bench.build_prompt(target, nonce=nonce)
    body = bench._build_body(a.model, prompt, num_ctx, 2048, "30m", stream=True)

    print(f"# {a.model} @ {a.ctx} (num_ctx={num_ctx}, think={'on' if a.think else 'off'})", flush=True)
    print(f"# prompt obsahuje 3 jehly: {[m for _, m in bench.NEEDLES]}\n", flush=True)

    think_parts, resp_parts = [], []
    with bench._open_generate(body) as r:
        for line in r:
            if not line.strip():
                continue
            c = json.loads(line)
            if c.get("thinking"):
                think_parts.append(c["thinking"])
            if c.get("response"):
                resp_parts.append(c["response"])
            if c.get("done"):
                break

    think, resp = "".join(think_parts), "".join(resp_parts)
    if think:
        print("=== MYŠLENÍ (thinking) ===")
        print(think.strip(), "\n")
    print("=== ODPOVĚĎ (response) ===")
    print(resp.strip(), "\n")
    print("=== KONTROLA JEHEL ===")
    for _, marker in bench.NEEDLES:
        print(f"  {marker:12}  v odpovědi: {'ANO' if marker in resp else 'ne ':3}  | v myšlení: {'ANO' if marker in think else 'ne'}")
    print("\n(Pokud je jehla v odpovědi 'ne', ale v textu je zjevně přítomna jinou formou,"
          "\n jde o artefakt hrubého grádu, ne o selhání retrievalu.)")

if __name__ == "__main__":
    main()
