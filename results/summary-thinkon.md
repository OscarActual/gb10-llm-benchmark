## LLM benchmark — lokální inference na GB10 (Blackwell)

**Hardware:** NVIDIA GB10, 128GB unified, 580.159.03  |  **Ollama:** 0.24.0  |  **Datum:** 2026-06-16

### Výsledky

| Model | Kontext | Prompt tok | Prefill t/s | Decode t/s | TTFT s | Paměť GB | Decode/GB | Jehly |
|---|---|---|---|---|---|---|---|---|
| Llama 3.1 8B · dense · Q4_K_M | 0.5k-chat | 803.0 | 3104.8 | 42.7 | 0.4 | 5.2 | 8.21 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 8k | 5301.0 | 3012.9 | 38.9 | 1.9 | 6.3 | 6.17 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 32k | 21181.0 | 2373.7 | 29.1 | 9.1 | 11.2 | 2.6 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 64k | 43102.0 | 1840.3 | 21.2 | 23.7 | 17.7 | 1.2 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 128k | 82381.0 | 1290.2 | 14.3 | 64.2 | 30.7 | 0.47 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 0.5k-chat | 853.0 | 4357.5 | 56.0 | 11.8 | 10.4 | 5.38 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 8k | 5530.0 | 4357.1 | 54.2 | 13.8 | 10.7 | 5.07 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 32k | 22021.0 | 3849.9 | 47.2 | 19.4 | 11.1 | 4.25 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 64k | 44799.0 | 3417.4 | 41.1 | 27.2 | 11.7 | 3.51 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 128k | 85601.0 | 2802.9 | 33.1 | 49.7 | 13.0 | 2.55 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 0.5k-chat | 902.0 | 3324.8 | 59.3 | 0.5 | 14.0 | 4.24 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 8k | 5655.0 | 3307.0 | 57.4 | 2.0 | 14.2 | 4.04 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 32k | 22433.0 | 2941.7 | 49.3 | 8.0 | 14.9 | 3.31 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 64k | 45597.0 | 2536.5 | 42.8 | 18.5 | 15.8 | 2.71 | 1/3 |
| gpt-oss 20B · MoE · MXFP4 | 128k | 87101.0 | 2037.2 | 34.9 | 43.4 | 17.6 | 1.98 | 1/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 0.5k-chat | 1368.0 | 1574.3 | 13.9 | 1.0 | 16.4 | 0.85 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 8k | 6228.0 | 1070.5 | 13.3 | 6.0 | 17.4 | 0.76 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 32k | 23372.0 | 889.7 | 11.4 | 26.5 | 21.4 | 0.53 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 64k | 47051.0 | 756.9 | 9.6 | 62.5 | 26.8 | 0.36 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 128k | 89467.0 | 617.0 | 7.5 | 145.5 | 37.6 | 0.2 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 0.5k-chat | 869.0 | 579.8 | 11.1 | 1.7 | 22.5 | 0.49 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 8k | 5739.0 | 593.5 | 11.0 | 9.9 | 22.9 | 0.48 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 32k | 22921.0 | 571.6 | 10.3 | 40.4 | 24.7 | 0.42 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 64k | 46646.0 | 550.0 | 9.6 | 85.2 | 27.3 | 0.35 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 128k | 89155.0 | 516.0 | 8.5 | 173.3 | 32.3 | 0.26 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 256k | 174241.0 | 458.3 | 6.7 | 380.9 | 42.5 | 0.16 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 0.5k-chat | 853.0 | 720.3 | 9.9 | 39.0 | 23.1 | 0.43 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 8k | 5529.0 | 664.7 | 9.4 | 50.0 | 25.7 | 0.37 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 32k | 22021.0 | 588.2 | 9.0 | 82.4 | 27.8 | 0.32 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 64k | 44800.0 | 536.8 | 8.3 | 132.0 | 30.5 | 0.27 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 128k | 85602.0 | 441.2 | 7.2 | 249.7 | 36.1 | 0.2 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 256k | 167282.0 | 310.8 | 5.7 | 608.8 | 47.2 | 0.12 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 0.5k-chat | 869.0 | 1351.9 | 59.6 | 0.8 | 26.2 | 2.27 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 8k | 5739.0 | 1390.7 | 57.1 | 4.3 | 26.4 | 2.16 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 32k | 22921.0 | 1337.5 | 51.1 | 17.4 | 27.1 | 1.89 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 64k | 46648.0 | 1283.0 | 45.6 | 36.7 | 28.1 | 1.62 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 128k | 89154.0 | 1191.6 | 37.7 | 75.3 | 30.3 | 1.24 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 256k | 174241.0 | 1051.0 | 27.9 | 166.6 | 34.6 | 0.81 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 0.5k-chat | 803.0 | 292.8 | 4.9 | 2.9 | 42.9 | 0.11 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 8k | 5303.0 | 303.6 | 4.8 | 17.6 | 45.8 | 0.1 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 32k | 21180.0 | 262.2 | 4.3 | 80.9 | 57.1 | 0.08 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 64k | 43102.0 | 226.4 | 3.7 | 190.6 | 72.2 | 0.05 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 128k | 82380.0 | 179.3 | 2.9 | 459.9 | 102.4 | 0.03 | 3/3 |
| gpt-oss 120B · MoE · MXFP4 | 0.5k-chat | 902.0 | 1134.7 | 42.4 | 1.1 | 65.6 | 0.65 | 3/3 |
| gpt-oss 120B · MoE · MXFP4 | 8k | 5656.0 | 1235.6 | 41.0 | 5.0 | 66.0 | 0.62 | 1/3 |
| gpt-oss 120B · MoE · MXFP4 | 32k | 22435.0 | 1186.4 | 35.0 | 19.3 | 66.9 | 0.52 | 1/3 |
| gpt-oss 120B · MoE · MXFP4 | 64k | 45598.0 | 1100.3 | 30.1 | 41.9 | 68.2 | 0.44 | 3/3 |
| gpt-oss 120B · MoE · MXFP4 | 128k | 87102.0 | 953.8 | 24.3 | 92.0 | 70.8 | 0.34 | 1/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 0.5k-chat | 1399.0 | 273.6 | 2.7 | 5.3 | 83.0 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 8k | 6262.0 | 188.6 | 2.7 | 33.5 | 85.2 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 32k | 23406.0 | 160.4 | 2.5 | 146.3 | 94.1 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 64k | 47084.0 | 141.4 | 2.2 | 333.5 | 105.9 | 0.02 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 0.5k-chat | 878.0 | 457.8 | 20.1 | 2.1 | 91.5 | 0.22 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 8k | 5737.0 | 503.0 | 20.0 | 11.6 | 91.5 | 0.22 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 32k | 22882.0 | 533.7 | 19.8 | 43.1 | 91.8 | 0.22 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 64k | 46563.0 | 537.2 | 19.1 | 86.9 | 92.1 | 0.21 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 128k | 88980.0 | 528.2 | 18.5 | 169.0 | 92.8 | 0.2 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 256k | 173893.0 | 506.3 | 17.1 | 344.2 | 94.2 | 0.18 | 3/3 |

### Metodika
- Hodnoty = medián z opakovaných běhů; TTFT měřeno přes streaming
- Flash Attention: 1 · KV cache: f16 (default) · num_predict=2048 · temperature=0 · seed=42
- Thinking/reasoning: ponecháno (default modelu) → srovnatelné TTFT a decode napříč modely
- Paměť (GB) = footprint z `ollama ps`; na GB10 jde o UNIFIED paměť, ne VRAM
- Decode/GB = decode tok/s na 1 GB paměti (vyšší = efektivnější)
- Jehly = retrieval test: kolik ze 3 unikátních faktů model v odpovědi našel (hrubá kontrola, ne plný scoring)
- Kontexty nad schopnosti modelu se nepouští (žádný tichý ořez); chyby vyfiltrovány
- Každý běh má unikátní prefix (nonce) → měří se reálný prefill/TTFT, ne cache hit
- Příkon NENÍ z nvidia-smi (na unified vrací N/A) — doplň ručně z wattmetru

**Detaily:** `results.csv` + `results.jsonl` | Meta: `bench_meta.json`

*Běželo na lokálním hardware bez přístupu k externím API.*
