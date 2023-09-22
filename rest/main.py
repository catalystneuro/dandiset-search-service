import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.health import router as health_router
from routers.search import router as search_router
from core.settings import settings


description = """
Documentation for Dandiset search API
"""


def configure_app():
    app = FastAPI(
        title=settings.APP_TITLE,
        description=description,
        version=settings.VERSION,
        docs_url="/docs",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS["origins"],
        allow_credentials=settings.CORS["allow_credentials"],
        allow_methods=settings.CORS["allow_methods"],
        allow_headers=settings.CORS["allow_headers"],
    )

    app.include_router(health_router, tags=["Health"])
    app.include_router(search_router, tags=["Search"])

    return app, settings

app, settings = configure_app()

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.SERVER_HOST,
        port=settings.PORT,
        reload=settings.RELOAD
    )