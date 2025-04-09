FROM python:3.13-slim
RUN pip install uv
COPY . /backend
WORKDIR /backend
RUN uv sync
CMD uv run uvicorn app.main:app --host 0.0.0.0
