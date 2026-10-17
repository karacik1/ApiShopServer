from fastapi import FastAPI
from blog.resourses import router


def get_app():
    app = FastAPI()

    app.include_router(router) # <- вот тут мы зарегистрировали роутер

    return app


app = get_app()

