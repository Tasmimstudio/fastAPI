from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Social Media API Test")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Social Media API is working!", "status": "success"}

@app.get("/test")
def test_endpoint():
    return {"message": "Test endpoint works!"}

@app.post("/test-user")
def create_test_user(name: str):
    return {"message": f"Hello {name}!", "user_created": True}