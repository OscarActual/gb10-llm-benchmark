## LLM benchmark — lokální inference na GB10 (Blackwell)

**Hardware:** NVIDIA GB10, 128GB unified, 580.159.03  |  **Ollama:** 0.24.0  |  **Datum:** 2026-06-16

### Výsledky

| Model | Kontext | Prompt tok | Prefill t/s | Decode t/s | TTFT s | Paměť GB | Decode/GB | Jehly |
|---|---|---|---|---|---|---|---|---|
| Llama 3.1 8B · dense · Q4_K_M | 0.5k-chat | 802.0 | 3067.7 | 42.7 | 0.4 | 5.2 | 8.21 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 8k | 5303.0 | 2941.3 | 38.9 | 1.9 | 6.3 | 6.17 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 32k | 21180.0 | 2319.6 | 29.0 | 9.3 | 11.2 | 2.59 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 64k | 43102.0 | 1826.0 | 21.0 | 23.8 | 17.7 | 1.19 | 3/3 |
| Llama 3.1 8B · dense · Q4_K_M | 128k | 82381.0 | 1293.2 | 14.3 | 64.0 | 30.7 | 0.47 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 0.5k-chat | 845.0 | 4338.1 | 56.6 | 0.4 | 10.4 | 5.44 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 8k | 5522.0 | 4344.7 | 54.9 | 1.5 | 10.7 | 5.13 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 32k | 22014.0 | 3902.8 | 47.0 | 6.0 | 11.1 | 4.23 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 64k | 44793.0 | 3419.8 | 40.8 | 13.6 | 11.7 | 3.49 | 3/3 |
| Gemma 4 E4B · edge · Q4_K_M | 128k | 85594.0 | 2774.8 | 33.5 | 31.5 | 13.0 | 2.58 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 0.5k-chat | 897.0 | 3276.8 | 58.8 | 0.5 | 14.0 | 4.2 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 8k | 5650.0 | 3290.2 | 57.5 | 2.0 | 14.2 | 4.05 | 2/3 |
| gpt-oss 20B · MoE · MXFP4 | 32k | 22428.0 | 2983.0 | 49.3 | 7.9 | 14.9 | 3.31 | 3/3 |
| gpt-oss 20B · MoE · MXFP4 | 64k | 45594.0 | 2541.7 | 43.1 | 18.4 | 15.8 | 2.73 | 1/3 |
| gpt-oss 20B · MoE · MXFP4 | 128k | 87096.0 | 2037.8 | 35.0 | 43.3 | 17.6 | 1.99 | 1/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 0.5k-chat | 1366.0 | 1561.2 | 13.9 | 1.0 | 16.4 | 0.85 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 8k | 6228.0 | 1075.3 | 13.2 | 5.9 | 17.4 | 0.76 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 32k | 23373.0 | 890.9 | 11.4 | 26.5 | 21.4 | 0.53 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 64k | 47052.0 | 764.9 | 9.6 | 61.8 | 26.8 | 0.36 | 3/3 |
| Mistral Small 3.2 24B · dense · Q4_K_M | 128k | 89468.0 | 616.8 | 7.5 | 145.5 | 37.6 | 0.2 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 0.5k-chat | 871.0 | 586.3 | 11.5 | 1.7 | 22.5 | 0.51 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 8k | 5741.0 | 594.1 | 11.3 | 9.9 | 22.9 | 0.49 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 32k | 22924.0 | 573.7 | 10.6 | 40.2 | 24.7 | 0.43 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 64k | 46649.0 | 549.1 | 9.9 | 85.2 | 27.3 | 0.36 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 128k | 89156.0 | 512.0 | 8.7 | 174.6 | 32.3 | 0.27 | 3/3 |
| Qwen 3.6 27B · dense · Q4_K_M | 256k | 174243.0 | 453.8 | 7.0 | 384.7 | 42.5 | 0.16 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 0.5k-chat | 849.0 | 716.2 | 10.3 | 1.4 | 23.1 | 0.45 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 8k | 5525.0 | 661.1 | 9.0 | 8.6 | 25.7 | 0.35 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 32k | 22018.0 | 561.4 | 9.4 | 39.6 | 27.8 | 0.34 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 64k | 44797.0 | 535.9 | 8.6 | 84.0 | 30.5 | 0.28 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 128k | 85598.0 | 441.1 | 7.5 | 194.9 | 36.1 | 0.21 | 3/3 |
| Gemma 4 31B · dense · Q4_K_M | 256k | 167280.0 | 315.2 | 5.9 | 532.0 | 47.2 | 0.12 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 0.5k-chat | 872.0 | 1367.1 | 60.2 | 0.8 | 26.2 | 2.3 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 8k | 5742.0 | 1398.4 | 56.7 | 4.3 | 26.4 | 2.15 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 32k | 22924.0 | 1345.6 | 50.9 | 17.3 | 27.1 | 1.88 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 64k | 46649.0 | 1275.6 | 44.3 | 36.9 | 28.1 | 1.58 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 128k | 89156.0 | 1190.9 | 36.6 | 75.3 | 30.3 | 1.21 | 3/3 |
| Qwen 3.6 35B-A3B · MoE 3B akt. · Q4_K_M | 256k | 174243.0 | 1056.4 | 27.8 | 165.7 | 34.6 | 0.8 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 0.5k-chat | 803.0 | 294.3 | 4.9 | 2.8 | 42.9 | 0.11 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 8k | 5302.0 | 304.6 | 4.7 | 17.6 | 45.8 | 0.1 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 32k | 21181.0 | 262.6 | 4.3 | 80.9 | 57.1 | 0.08 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 64k | 43101.0 | 226.6 | 3.7 | 190.5 | 72.2 | 0.05 | 3/3 |
| Llama 3.3 70B · dense · Q4_K_M | 128k | 82380.0 | 180.7 | 2.9 | 456.2 | 102.4 | 0.03 | 3/3 |
| gpt-oss 120B · MoE · MXFP4 | 0.5k-chat | 897.0 | 1134.4 | 42.3 | 1.1 | 65.6 | 0.64 | 3/3 |
| gpt-oss 120B · MoE · MXFP4 | 8k | 5650.0 | 1244.6 | 41.2 | 4.8 | 66.0 | 0.62 | 1/3 |
| gpt-oss 120B · MoE · MXFP4 | 32k | 22429.0 | 1200.4 | 35.1 | 19.1 | 66.9 | 0.52 | 1/3 |
| gpt-oss 120B · MoE · MXFP4 | 64k | 45591.0 | 1096.5 | 30.2 | 42.1 | 68.2 | 0.44 | 1/3 |
| gpt-oss 120B · MoE · MXFP4 | 128k | 87097.0 | 958.3 | 24.4 | 91.5 | 70.8 | 0.34 | 1/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 0.5k-chat | 1396.0 | 273.7 | 2.7 | 5.3 | 83.0 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 8k | 6261.0 | 174.4 | 2.7 | 57.8 | 85.2 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 32k | 23407.0 | 161.3 | 2.5 | 145.4 | 94.1 | 0.03 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 64k | 47084.0 | 141.8 | 2.2 | 332.5 | 105.9 | 0.02 | 3/3 |
| Mistral Medium 3.5 128B · dense · Q4_K_M | 128k | 89502.0 | 114.9 | 0.8 | 780.2 | 121.7 | 0.01 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 0.5k-chat | 874.0 | 454.6 | 20.6 | 2.1 | 91.5 | 0.23 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 8k | 5737.0 | 498.6 | 20.3 | 34.8 | 91.5 | 0.22 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 32k | 22882.0 | 532.1 | 20.0 | 43.2 | 91.8 | 0.22 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 64k | 46562.0 | 538.7 | 19.6 | 86.7 | 92.1 | 0.21 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 128k | 88979.0 | 529.2 | 18.9 | 168.6 | 92.8 | 0.2 | 3/3 |
| Nemotron 3 Super 120B-A12B · MoE 12B akt. · Q4_K_M | 256k | 173893.0 | 504.5 | 17.8 | 345.5 | 94.2 | 0.19 | 3/3 |

### Metodika
- Hodnoty = medián z opakovaných běhů; TTFT měřeno přes streaming
- Flash Attention: 1 · KV cache: f16 (default) · num_predict=512 · temperature=0 · seed=42
- Thinking/reasoning: vypnuto (think:false) → srovnatelné TTFT a decode napříč modely
- Paměť (GB) = footprint z `ollama ps`; na GB10 jde o UNIFIED paměť, ne VRAM
- Decode/GB = decode tok/s na 1 GB paměti (vyšší = efektivnější)
- Jehly = retrieval test: kolik ze 3 unikátních faktů model v odpovědi našel (hrubá kontrola, ne plný scoring)
- Kontexty nad schopnosti modelu se nepouští (žádný tichý ořez); chyby vyfiltrovány
- Každý běh má unikátní prefix (nonce) → měří se reálný prefill/TTFT, ne cache hit
- Příkon NENÍ z nvidia-smi (na unified vrací N/A) — doplň ručně z wattmetru

**Detaily:** `results.csv` + `results.jsonl` | Meta: `bench_meta.json`

*Běželo na lokálním hardware bez přístupu k externím API.*
