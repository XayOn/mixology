from fastapi import FastAPI


def setup_routes(app: FastAPI):
    from mixology.preparer.routes import router as preparer_router

    app.include_router(preparer_router)
