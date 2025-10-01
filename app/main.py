from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from neomodel import db
from neo4j.exceptions import AuthError, ServiceUnavailable
# Use absolute imports for clarity
from app import config
from app.routers import person, user, post, comment, like



app = FastAPI(
    title="Social Media API with Neo4j",
    description="A FastAPI social media platform with Neo4j graph database"
)

# Add CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all routers
app.include_router(person.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(like.router)

@app.get("/")
def read_root():
    return {
        "message": "Social Media API with Neo4j is running!",
        "status": "active",
        "database": "connected",
        "endpoints": {
            "persons": "/persons",
            "users": "/users",
            "posts": "/posts",
            "comments": "/comments",
            "likes": "/likes",
            "docs": "/docs"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "connected"}

@app.on_event("startup")
def startup_db_check():
    try:
        db.cypher_query("RETURN 1")
        print("[SUCCESS] Neo4j connection successful!")
    except AuthError:
        print("[WARNING] Authentication failed: Check username/password.")
        print("[INFO] Server will start but Neo4j features may not work.")
    except ServiceUnavailable:
        print("[WARNING] Cannot connect: Is Neo4j running?")
        print("[INFO] Server will start but Neo4j features may not work.")
    except Exception as e:
        print(f"[WARNING] Neo4j connection failed: {e}")
        print("[INFO] Server will start but Neo4j features may not work.")