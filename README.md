# dandiset-search-service

To run the services, firt set the environment variables:

```bash
export QDRANT_HOST=
export QDRANT_PORT=
export QDRANT_COLLECTION_NAME=
export QDRANT_VECTOR_SIZE=
export QDRANT_API_KEY=
export OPENAI_API_KEY=
export DANDI_API_KEY=
```

Running with docker compose pulling images from github packages:

```bash
docker compose up
```

Running with docker compose building images locally:

```bash
docker compose -f docker-compose.dev.yaml up --build
```

Services will be available at:

- http://localhost:5173 - Frontend
- http://localhost:8000 - REST API
- http://localhost:8000/docs - REST API docs
- http://localhost:6333 - Qdrant API
- http://localhost:6333/dashboard - Qdrant dashboard


