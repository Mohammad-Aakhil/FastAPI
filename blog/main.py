from fastapi import FastAPI
from . import models
from .database import *
from .routers import user, blog, auth



app = FastAPI()

models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)



from fastapi.routing import APIRoute

def list_routes(app):
    route_list = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            route_list.append(route.path)
    return route_list

print("AVAILABLE ROUTES:")
print(list_routes(app))
