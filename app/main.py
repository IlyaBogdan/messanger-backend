import uvicorn
from fastapi import FastAPI
from database import SessionLocal, engine, Base
from modules.v1.routers.user import router as UserRouter
from modules.v1.routers.auth import router as AuthRouter

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

if __name__ == '__main__':
    print("hello")
    uvicorn.run("main:app", host='0.0.0.0', port=8080, reload=True, workers=3)