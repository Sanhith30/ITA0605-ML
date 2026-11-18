# Backend application

This package contains the FastAPI application entrypoint and its domain modules. `main.py` wires the HTTP routes, middleware, model loading, validation, and service calls.

- `schemas/` defines request and response data models.
- `services/` contains DOM/URL feature extraction, prediction, and request-rate limiting.
