# Backend

FastAPI service for the PhishShield capstone. It exposes health, metrics, URL prediction, and feature-extraction endpoints, and loads the trained deployment artefacts from `models/`.

- `app/`: API entrypoint, validation schemas, and extraction/prediction services.
- `models/`: serialized preprocessors, feature definitions, and classifiers.
- `Dockerfile`: container image definition.
- `requirements.txt`: Python runtime dependencies.

Run locally from this directory with `uvicorn app.main:app --reload --port 8000` after installing the requirements.
