from fastapi import FastAPI
from api.v1.router import router as api_router_v1_0
from configs.configs import config
from fastapi.middleware.cors import CORSMiddleware

if not config.debug and config.sentry_dsn:
    import sentry_sdk

    sentry_sdk.init(config.sentry_dsn)

app = FastAPI(title=config.project_title)
app.include_router(api_router_v1_0, prefix='/v1')

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

if config.debug:
    if __name__ == "__main__":
        import uvicorn

        uvicorn.run(app, host='0.0.0.0', port=4001)
