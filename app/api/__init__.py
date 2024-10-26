from .cities.router import router as cities_router
from .stores.router import router as stores_router
from .products.router import router as products_router
from .sales.router import router as sales_router

__all__ = ("routers")

routers = (cities_router, products_router, stores_router, sales_router)
