# WN_GPT Research (LaTeX)

## Important: three different systems

| Name | File | What it is |
|------|------|------------|
| **WellnessGPT** (HeyDoc) | `wellnessgpt_tse.tex` | Commercial product essay — Orchestration Engine, **HealthMem**, HIPAA/FHIR, HeyDoc AI |
| **Wellbeing** (WB-001) | `our_agent.tex` | Requirements / vision spec — Neo4j + Pinecone **RAG-first**, evidence panels |
| **WN-GPT Agent** (**ours**) | `Backend/` + `wellnessgpt_architecture_research.tex` | **What we built** — LangGraph, 15 agents, SQLite, supervisor router |

**Do not treat these as the same product.** The internship code is **WN-GPT Agent**, not the full HeyDoc WellnessGPT platform.

## Main document for our implementation

**`wellnessgpt_architecture_research.tex`** (PDF title: **WN-GPT Agent**)

- Clarifies difference from `wellnessgpt_tse.tex`
- Problem statement, process flow, page-indexing roadmap
- Compares **our agent** with Hippocratic AI and August AI

## Compile

```powershell
cd D:\Internship\WN_GPT\Research
pdflatex wellnessgpt_architecture_research.tex
pdflatex wellnessgpt_architecture_research.tex
```

## Other research files

| File | Use |
|------|-----|
| `wellnessgpt_tse.tex` | HeyDoc WellnessGPT marketing / architecture TSE (reference only) |
| `our_agent.tex` | Wellbeing WB-001 SRS — target RAG/orchestration vision |
| `hippocratic_ai_tse.tex` | Competitor: Hippocratic AI |
| `august_ai_tse.tex` | Competitor: August AI |
| `flow_analysis_tse.tex` | Multi-vendor flow study (Wellbeing WB-001 framing) |

## Run our agent (Backend)

```powershell
cd D:\Internship\WN_GPT\Backend
uv run python -m db_init
uv run python -m cli
```
