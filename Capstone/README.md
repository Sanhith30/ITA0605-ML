# PhishShield AI Capstone

This capstone is an end-to-end intelligent phishing-website detection platform. It combines a FastAPI backend, a React/Vite dashboard, a Manifest V3 Chrome extension, trained scikit-learn models, explainable-AI notebooks, automated tests, API documentation, and submission reports.

## Main capabilities

- Extracts URL and DOM features from a website.
- Predicts phishing risk with a trained Random Forest model.
- Produces a 0-100 risk score and SHAP-based explanation reasons.
- Provides a dashboard, analytics views, and browser-extension alerts.
- Supports local development and Docker Compose deployment.

## Structure

- `backend/`: FastAPI service, request schemas, feature extraction, prediction services, and model artefacts.
- `frontend/`: React/Vite dashboard.
- `chrome-extension/`: browser extension UI and background logic.
- `ml/`: model-training script, notebooks, and model files.
- `docs/`: endpoint reference.
- `tests/`: backend and extractor tests.
- `MLCapstone Project Report.pdf` and `ML CAPSTONE PROJECT PPT-1.pdf`: report and presentation materials.

## Run locally

Train or refresh deployment models with `python ml/train_deployment_model.py`. Start the API with `cd backend && pip install -r requirements.txt && uvicorn app.main:app --reload --port 8000`; start the dashboard with `cd frontend && npm install && npm run dev`. For the complete containerised stack, run `docker-compose up --build`. Run tests with `python -m unittest discover -s tests`.
