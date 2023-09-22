# dandiset-search-service

To run the services, firt set the environment variables:

```bash
export QDRANT_HOST=
export QDRANT_PORT=
export QDRANT_COLLECTION_NAME=
export QDRANT_VECTOR_SIZE=
export OPENAI_API_KEY=
export DANDI_API_KEY=
```

Running with docker compose pulling images from github packages:

```bash
docker compose up
```

Running with docker compose building images locally:

```bash
docker compose -f docker-compose.dev.yml up --build
```