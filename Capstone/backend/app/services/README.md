# Backend services

Reusable backend logic for the phishing detector:

- `extractor.py`: crawls page content and derives lexical and DOM features.
- `predictor.py`: loads preprocessing/model artefacts, predicts risk, and builds explanations.
- `rate_limiter.py`: limits repeated requests to protect the API.
