from fastapi import FastAPI
import uvicorn

from app.api import routers

app = FastAPI(
    title="Sales API",
    description=(
        "Sales API — это FastAPI приложение для управления продажами "
        "в сети магазинов бытовой техники"
    ),
)

[app.include_router(router) for router in routers]


if __name__ == "main":
    uvicorn.run(app)
