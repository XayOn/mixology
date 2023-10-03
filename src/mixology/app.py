from fastapi import FastAPI


def get_app():
    app = FastAPI()
    from .routes import setup_routes

    setup_routes(app)
