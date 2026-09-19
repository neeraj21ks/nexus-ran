# crypto-RAG
A hybrid RAG system answering natural-language questions over crypto market data and news, combining SQL and vector retrieval with pgvector.

crypto RAG answers natural-language questions about crypto markets by combining two very different data sources: structured OHLCV/trade data (ingested via the companion API-to-AI pipeline) and unstructured crypto news and exchange announcements. A query router classifies each incoming question and decides whether it needs a SQL lookup, a vector similarity search over embedded news articles, or both — then an LLM synthesizes the retrieved results into a grounded, source-attributed answer.

Built to explore the engineering challenges of production RAG: chunking strategy, embedding consistency between ingestion and query time, hybrid retrieval routing, and hallucination mitigation through explicit grounding — not just wrapping an LLM API call.

Stack: Python · PostgreSQL + pgvector · sentence-transformers · FastAPI · Streamlit

                    ┌─────────────────┐         ┌─────────────────┐
                    │   Binance API   │         │   News & docs   │
                    └────────┬────────┘         └────────┬────────┘
                             │                             │
                    ┌────────▼─────────┐         ┌────────▼─────────┐
                    │ Airflow + dbt ETL│         │ Scrape + chunk   │
                    │ Batch ingestion  │         │ + embed          │
                    └────────┬─────────┘         └────────┬─────────┘
                             │                             │
                    ┌────────▼─────────┐         ┌────────▼─────────┐
                    │ Postgres star    │         │ pgvector store   │
                    │ schema (OHLCV)   │         │ (news embeddings)│
                    └────────┬─────────┘         └────────┬─────────┘
                             │                             │
                             └──────────┬──────────────────┘
                                        │
                              ┌─────────▼──────────┐
                              │   Query router     │
                              │ SQL vs vector vs   │
                              │ hybrid retrieval   │
                              └─────────┬──────────┘
                                        │
                              ┌─────────▼──────────┐
                              │   LLM synthesis    │
                              │ Grounds answer in  │
                              │ retrieved data     │
                              └─────────┬──────────┘
                                        │
                              ┌─────────▼──────────┐
                              │FastAPI + Streamlit │
                              │ Chat interface     │
                              └────────────────────┘

Two ingestion paths converge on a single router: structured market data flows through the existing Airflow/dbt pipeline into a Postgres star schema, while news and docs are scraped, chunked, and embedded into the same Postgres instance via pgvector. Reusing one database for both means no separate vector DB to provision or keep in sync.

                              
