FROM python3.10 AS build

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip && \
    pip install --upgrade setuptools && \
    pip install --upgrade wheel

RUN mkdir ./pipelines
WORKDIR /pipelines

FROM build AS dev

COPY simple_pipeline ./simple_pipeline
RUN pip install -e ./simple_pipeline

CMD ["python", "-m", "simple_pipeline"]

