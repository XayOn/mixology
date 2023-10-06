FROM python:3.11 AS base_hatch
WORKDIR /app
RUN pip install hatch

FROM base_hatch as builder
COPY . .
RUN hatch build -t wheel

FROM python:3.11-slim

WORKDIR /app
COPY --from=builder /app/dist/mixology*.whl /app/
RUN pip install /app/mixology*.whl
EXPOSE 8000
CMD ["uvicorn", "--factory", "mixology.app:get_app", "--port", "8080", "--host", "0.0.0.0", "--log-level=debug", "--reload"]
