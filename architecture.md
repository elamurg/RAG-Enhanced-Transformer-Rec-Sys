# RAG Music Recommendation System — Deployed Architecture

**Project:** Addressing the Cold-Start Problem in Spotify Music Recommendation Systems Using RAG and NLP  
**Student:** Ela Murgelj | QMUL MSc Computer Science 2025–26  
**Supervisor:** Dr. Fabrizio Smeraldi

---

## System Overview

The deployed system is a RAG-enhanced recommendation engine that accepts natural language queries from cold-start users and returns ranked, explainable track recommendations. It operates as a containerised FastAPI service backed by a FAISS vector store and an LLM orchestrated via LangChain.

---

## Online Inference Flow

```
User (natural language query)
        │
        ▼
┌─────────────────────────┐
│   FastAPI REST API      │  ← Docker container
└─────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  NLP + Embedding Layer                                  │
│                                                         │
│  Query parser  →  Embedding model  →  Query vector      │
│  (preprocessing)  (MiniLM / BGE /    (dense float       │
│                    OpenAI)            embedding)         │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  Vector Store                                           │
│                                                         │
│  FAISS index  →  Track metadata store  →  Top-k         │
│  (ANN search)    (Spotify Web API data)   candidates    │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────────────────────────────────────┐
│  RAG Pipeline (LangChain)                               │
│                                                         │
│  Context assembler  →  LLM  →  Ranked recommendations  │
│  (prompt construction)  (ranking + explanation)         │
└─────────────────────────────────────────────────────────┘
        │
        ▼
┌─────────────────────────┐
│   FastAPI response      │  ← JSON recommendations
└─────────────────────────┘
        │
        ▼
User (ranked track list)
```

---

## Offline Indexing Pipeline

Runs once (or periodically) to populate the FAISS index. Not part of the live request path.

```
Spotify Web API
        │  track metadata + audio features
        ▼
Preprocessing
        │  feature engineering + semantic text field construction
        ▼
Embedding generation
        │  same embedding model used in the online path
        ▼
FAISS index  ←─────────────────────────────────── feeds vector store
```

> The offline pipeline uses the same embedding model as the online inference path to ensure the query vector space and the indexed track vector space are aligned.

---

## Component Summary

| Layer | Component | Role |
|---|---|---|
| Serving | FastAPI | Exposes REST endpoint, handles request/response lifecycle |
| Serving | Docker | Containerises the full stack for reproducible deployment |
| NLP | Query parser | Cleans and normalises the raw natural language input |
| NLP | Embedding model | Encodes the query into a dense vector (MiniLM-L6-v2, BGE-small-en-v1.5, or OpenAI text-embedding-3-small) |
| Vector store | FAISS index | Performs approximate nearest-neighbour search over track embeddings |
| Vector store | Track metadata store | Holds track name, artist, album, genre tags, and audio feature descriptors sourced from the Spotify Web API |
| RAG | Context assembler | Constructs the LLM prompt from the retrieved candidates and the original query |
| RAG | LLM (via LangChain) | Ranks candidates and generates natural language explanations for each recommendation |

---

## Key Design Decisions

- **Cold-start by design.** The system requires no prior listening history. The only input is a natural language query, making it suitable for new users from the first interaction.
- **Embedding model is interchangeable.** Three models are evaluated (MiniLM, BGE, OpenAI) and the best-performing configuration is used in the deployed system.
- **Separation of online and offline paths.** FAISS indexing is a one-time offline process. The live request path only performs query embedding and retrieval — no training or re-indexing occurs at inference time.
- **Explainability.** The LLM produces a natural language rationale alongside each recommendation, distinguishing this approach from opaque CF/CBF baselines.