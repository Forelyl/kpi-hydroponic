from time import time
from fastapi import FastAPI
import fastapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import threading
import sys

from server.routers import api
from server.security.security import add_token_endpoint, add_test_endpoint

from server.database_driver.database import start_playground

# startup-shutdown
is_debug:   bool = False
start_time: int  = 0


@asynccontextmanager
async def lifespan(app: FastAPI):
    global is_debug
    global start_time

    is_debug   = '--reload' in sys.argv
    start_time = int(time())

    # print startup info
    print('=' * 50)
    print("Starting up - Hydroponic Server")
    print(f'Python Version: {sys.version}')
    print(f'FastAPI Version: {fastapi.__version__}')
    print(f'Mode: {"Debug" if is_debug else "Production"}')
    print(f'Startup clock time: {start_time}s')
    print('=' * 50)

    # start playground
    end_conditionalvar = threading.Event()
    thread             = threading.Thread(target=start_playground, args=(end_conditionalvar,))
    thread.start()

    # debug function
    if is_debug:
        @app.get('/get_startup_time')
        def get_startup_time() -> int:
            return start_time

    yield
    print("Shutting down...")

    # stop playground
    end_conditionalvar.set()
    thread.join()

# add fastapi app
app = FastAPI(lifespan=lifespan)

# add routers
app.include_router(api.app)


# add CORS
origins = [
    "http://127.0.0.1:3000", # TODO: to remove
    "http://127.0.0.1:5173",
    "http://127.0.0.1:6789"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add security (authorization) endpoints
add_token_endpoint(app)
add_test_endpoint(app)