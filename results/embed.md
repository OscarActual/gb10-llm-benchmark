=== BGE-M3 · 568M · hybrid · multiling. (bge-m3) ===
  dim 1024 | 55.7 docs/s | 118.4 ms/dotaz | recall@1 0.92 | recall@5 1.0 | MRR 0.958 | 1.3 GB
=== EmbeddingGemma 300M · multiling. (embeddinggemma) ===
  dim 768 | 79.1 docs/s | 93.0 ms/dotaz | recall@1 0.67 | recall@5 1.0 | MRR 0.799 | 1.1 GB
=== Qwen3-Embedding 0.6B (qwen3-embedding:0.6b) ===
  dim 1024 | 33.5 docs/s | 69.3 ms/dotaz | recall@1 0.83 | recall@5 1.0 | MRR 0.889 | 6.3 GB
=== Qwen3-Embedding 4B (qwen3-embedding:4b) ===
  dim 2560 | 25.5 docs/s | 94.1 ms/dotaz | recall@1 0.83 | recall@5 1.0 | MRR 0.917 | 13.0 GB
=== Qwen3-Embedding 8B (qwen3-embedding:8b) ===
  dim 4096 | 19.9 docs/s | 99.4 ms/dotaz | recall@1 1.0 | recall@5 1.0 | MRR 1.0 | 15.4 GB
=== Snowflake Arctic Embed 2 · multiling. (snowflake-arctic-embed2) ===
  dim 1024 | 51.5 docs/s | 148.9 ms/dotaz | recall@1 1.0 | recall@5 1.0 | MRR 1.0 | 1.3 GB
=== Multilingual E5 Large (jeffh/intfloat-multilingual-e5-large-instruct:f16) ===
  dim 1024 | 56.2 docs/s | 125.2 ms/dotaz | recall@1 0.92 | recall@5 1.0 | MRR 0.958 | 1.1 GB
=== Nomic Embed Text · EN-leaning (nomic-embed-text) ===
  dim 768 | 154.0 docs/s | 14.8 ms/dotaz | recall@1 0.25 | recall@5 0.58 | MRR 0.46 | 0.6 GB
=== mxbai Embed Large · EN-leaning (mxbai-embed-large) ===
  dim 1024 | 87.5 docs/s | 28.4 ms/dotaz | recall@1 0.08 | recall@5 0.42 | MRR 0.236 | 0.8 GB
=== all-MiniLM · baseline EN (all-minilm) ===
  dim 384 | 175.9 docs/s | 14.3 ms/dotaz | recall@1 0.08 | recall@5 0.5 | MRR 0.258 | 0.1 GB

## Embedding benchmark — česká RAG data (GB10)

Korpus: 16 pasáží (12 cílových + 4 distraktorů) · 12 parafrázových dotazů

| Model | Dim | docs/s | ms/dotaz | recall@1 | recall@5 | MRR | Paměť GB |
|---|---|---|---|---|---|---|---|
| Qwen3-Embedding 8B | 4096 | 19.9 | 99.4 | 1.0 | 1.0 | 1.0 | 15.4 |
| Snowflake Arctic Embed 2 · multiling. | 1024 | 51.5 | 148.9 | 1.0 | 1.0 | 1.0 | 1.3 |
| BGE-M3 · 568M · hybrid · multiling. | 1024 | 55.7 | 118.4 | 0.92 | 1.0 | 0.958 | 1.3 |
| Multilingual E5 Large | 1024 | 56.2 | 125.2 | 0.92 | 1.0 | 0.958 | 1.1 |
| Qwen3-Embedding 4B | 2560 | 25.5 | 94.1 | 0.83 | 1.0 | 0.917 | 13.0 |
| Qwen3-Embedding 0.6B | 1024 | 33.5 | 69.3 | 0.83 | 1.0 | 0.889 | 6.3 |
| EmbeddingGemma 300M · multiling. | 768 | 79.1 | 93.0 | 0.67 | 1.0 | 0.799 | 1.1 |
| Nomic Embed Text · EN-leaning | 768 | 154.0 | 14.8 | 0.25 | 0.58 | 0.46 | 0.6 |
| all-MiniLM · baseline EN | 384 | 175.9 | 14.3 | 0.08 | 0.5 | 0.258 | 0.1 |
| mxbai Embed Large · EN-leaning | 1024 | 87.5 | 28.4 | 0.08 | 0.42 | 0.236 | 0.8 |

### Metodika
- recall@1/@5 + MRR z parafrázových CZ dotazů (sémantické vyhledání, ne shoda slov)
- Prefixy aplikovány u modelů, které je očekávají (e5-instruct Instruct/Query, nomic search_*, qwen3 Instruct)
- docs/s = dávkové embedování korpusu (warm); ms/dotaz = medián latence jednoho dotazu
- HRUBÝ signál na malém setu — pro produkci doplnit větším CZ retrieval datasetem + rerankerem
- Běželo lokálně přes ollama /api/embed, bez externích API
