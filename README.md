# NEXUS RAN

**Agentic RAN Intelligence, Autonomous Network Assurance, Optimization and Verification Platform**

NEXUS RAN is a vendor-independent engineering platform that transforms RAN telemetry into evidence-backed fault diagnosis, governed optimization recommendations, and measurable post-change verification.

> Development status: Early development. The initial release is a simulation-based engineering demonstrator, not a production network controller.

## Product Workflow

OBSERVE -> DETECT -> INVESTIGATE -> DECIDE -> APPROVE -> ACT -> VERIFY / ROLLBACK

## Core Capabilities

- RAN KPI ingestion, normalization, and analysis
- Anomaly detection and fault investigation
- Evidence-backed root cause analysis
- Telecom knowledge retrieval (RAG) with citations
- Agent-coordinated optimization recommendations
- Configuration tracking and change-risk assessment
- Approval-controlled simulated execution
- KPI validation and rollback verification
- Incident lifecycle management and audit history
- Automated scenario testing and engineering evaluation

## Planned Architecture

| Layer | Planned technologies |
|---|---|
| RAN simulation | ns-O-RAN-FlexRIC, synthetic telemetry |
| Streaming | Apache Kafka, Python |
| Data storage | PostgreSQL, TimescaleDB, pgvector |
| Analytics and ML | pandas, scikit-learn, XGBoost |
| Agentic intelligence | Local LLM runtime, Python orchestration |
| Knowledge retrieval | Document processing, hybrid search, RAG |
| API | FastAPI |
| Dashboard | Streamlit |
| Observability | Structured logging, Prometheus, Grafana |
| Deployment | Docker Compose |

These are planned technologies, not claims that all components are implemented.

## Agentic Intelligence

A manager will coordinate specialist roles:

- KPI Intelligence
- Anomaly Detection
- RF Intelligence
- Root Cause Analysis
- Optimization
- Validation

Agents provide analysis and structured recommendations. They cannot independently authorize network changes or bypass policy and approval controls.

## Development Principles

1. Evidence-backed decisions rather than unsupported LLM conclusions.
2. Deterministic calculations for KPI values, risk, constraints, and validation.
3. Human approval before simulated change execution.
4. Traceability of recommendations, decisions, and outcomes.
5. Vendor-independent data contracts and integration boundaries.
6. Automated tests and reproducible experiments.
7. Clear separation between simulated results and production evidence.

## Local Development

Requirements: Windows 11 with WSL2, Python 3.12, Git, and Docker Desktop.

Run unit tests:

    .\.venv\Scripts\python.exe -m pytest -v

Run lint checks:

    .\.venv\Scripts\python.exe -m ruff check .

## Repository Structure

    src/nexus/
        api/
        core/
        telemetry/
        streaming/
        analytics/
        agents/
        knowledge/
        policies/
        control/
        integrations/
        audit/

    tests/
        unit/
        integration/
        simulation/
        end_to_end/

    configs/
    scripts/
    docs/
    dashboard/
    ml/
    deployment/

## Roadmap

- Foundation: configuration, health checks, logging, and tests.
- Telemetry: canonical RAN event schema and synthetic data.
- Simulation: fault scenarios and telemetry integration.
- Streaming and storage: Kafka, PostgreSQL, and TimescaleDB.
- Intelligence: KPI analytics, anomaly detection, and ML.
- Knowledge: telecom document ingestion and RAG.
- Agentic workflows: specialist agents and manager orchestration.
- Governance: risk assessment, approval, simulated execution, and rollback.
- Verification: post-change KPI validation and scenario evaluation.
- Delivery: API, dashboard, observability, documentation, and demonstration.

## Project Status

The repository is in its foundation stage. Planned capabilities are not yet implemented or production-ready.

## License

License to be determined.
