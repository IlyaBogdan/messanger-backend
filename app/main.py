import uvicorn
from fastapi import FastAPI
from database import engine, Base
from modules.v1.routers.user import router as UserRouter
from modules.v1.routers.auth import router as AuthRouter
from modules.v1.routers.chat import router as ChatRouter

Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="Messanger API",
    description="This is my pet-project API",
    version="0.0.1",
    contact={
        "name": "Ilya Bogdan",
        "url": "http://x-force.example.com/contact/",
        "email": "someemail@gmail.com",
    },
)

app.include_router(UserRouter)
app.include_router(AuthRouter)
app.include_router(ChatRouter)

if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)