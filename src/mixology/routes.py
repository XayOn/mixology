from fastapi import Depends, FastAPI

from mixology.auth import auth


def setup_routes(app: FastAPI):
    from mixology.configurer.routes import router as configurer_router
    from mixology.preparer.routes import router as preparer_router

    app.include_router(
        preparer_router,
        prefix="/prepare",
        tags=["prepare"],
        dependencies=[Depends(auth)],
    )
    app.include_router(
        configurer_router,
        prefix="/setup",
        tags=["setup"],
    )
