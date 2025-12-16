from fastapi import FastAPI
from .database import *
from .routers import user, blog, auth
from fastapi.responses import JSONResponse

app = FastAPI()


app.include_router(auth.router)
app.include_router(blog.router)
app.include_router(user.router)


#--------------------------------------------------------------------------------------------------------
from fastapi.routing import APIRoute

def list_routes(app):
    route_list = []
    for route in app.routes:
        if isinstance(route, APIRoute):
            route_list.append(route.path)
    return route_list

print("AVAILABLE ROUTES:")
print(list_routes(app))

#--------------------------------------------------------------------------------------------------------
#--MIDDLEWARES--^-_-^
from fastapi import FastAPI, Request
import time

# app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    response = await call_next(request)
    
    duration = time.time() - start_time
    print(f"{request.method} {request.url} took {duration:.2f}s")
    
    return response


# @app.middleware("http")
# async def auth_middleware(request: Request, call_next):
#     token = request.headers.get("Authorization")
    
#     if not token:
#         return JSONResponse(
#             status_code=401,
#             content={"detail": "Unauthorized-middleware"}
#         )
    
#     response = await call_next(request)
#     return response
