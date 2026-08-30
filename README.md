BusinessIntelligence.ai: KPI Storytelling Engine

Accenture Innovation Challenge 2026 - Round 2 Submission

Problem Track 3: BusinessIntelligence.ai

Live: https://nitishh710-businessintelligence-aic-app-ro5z0k.streamlit.app/#kpi-storytelling-copilot

Watch the Prototype Demo Video Here: https://youtu.be/ByzG0HqMZ6c


Executive Summary

Modern Business Intelligence (BI) dashboards are fundamentally passive. They excel at displaying what a metric is (e.g., "Revenue dropped by 8%"), but consistently fail to explain why it happened or what concrete action leaders should take next.

BusinessIntelligence.ai connects the raw data to executive decision-making. Built strictly around the core directive of Round 2—"The LLM should not be treated as the source of quantitative truth"—our solution uses a Hybrid Architecture.

The Hybrid Architecture

Deterministic Analytical Engine (Python/Math): Handles all quantitative calculations, multi-factor variance decomposition, missing data validation, and confidence scoring. The LLM is completely isolated from doing math.

Contextual Synthesizer (LLM Layer): Takes the hard mathematical facts and translates them into role-tailored narratives and actionable operational steps.

Addressing the Evaluation Criteria

Round 2 PDF Requirement

Implementation in Prototype

1. Multi-Factor KPI Movement

Analyzes a W06 Revenue drop by mathematically decomposing variance into Ad Spend cuts vs Organic Volume.

2. Low-Confidence & Abstention

When IoT telemetry from APAC is missing, confidence drops to 22%. The system refuses to hallucinate and issues an explicit System Abstention warning.

3. Sparse-History Scenarios

Evaluates a new Product launch (N=4 days). Recognizes that enterprise baseline requires N>=30 days and adjusts confidence to 48%, warning against hasty capital adjustments.

4. Role-Based Access (RBAC)

Regional Director: Gets strategic summary & financial ROI.



Operations Analyst: Gets driver breakdown & data lineage.

5. Governed Action Formatting

Outputs map strictly to: Driver -> Action -> Impact -> Owner -> Monitoring Plan.

6. Runtime Telemetry

Live UI metrics displaying execution latency, token consumption, and cost per insight ($).

Execution Instructions

1. Clone the repository

git clone https://github.com/nitishh710/BusinessIntelligence_AIC.git
cd BusinessIntelligence_AIC


2. Set up a Virtual Environment (Recommended for Linux/macOS)
To avoid modifying system packages and encountering the "externally-managed-environment" error:

python3 -m venv venv
source venv/bin/activate


(On Windows, use venv\Scripts\activate instead of source venv/bin/activate)

3. Install dependencies

pip install -r requirements.txt


4. Run the application

streamlit run app.py


Note: For the purpose of this prototype and to ensure seamless evaluation without requiring external API keys, the LLM layer and database ingestion are functionally simulated in Python to demonstrate the exact UX, latency, and token economics of a live production environment.
