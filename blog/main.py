from fastapi import FastAPI
from .database import *
from .routers import user, blog, auth


app = FastAPI()


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

# eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjo1LCJyb2xlIjoiZWRpdG9yIiwidHlwZSI6InJlZnJlc2giLCJleHAiOjE3NjYwMzE2MzR9.4Fm8yZee8JV9IMUpaGNtO37y08dH1iGsqUY5RXVdrdQ