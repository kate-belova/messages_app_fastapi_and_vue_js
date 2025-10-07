import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from handlers import routers

app = FastAPI(
    title='Messages CRUD',
    openapi_tags=[
        {'name': 'API 💬', 'description': 'API для работы с сообщениями'}
    ],
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

for router in routers:
    app.include_router(router)

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
