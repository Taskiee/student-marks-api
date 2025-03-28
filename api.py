from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json

# Load JSON file
with open("q-vercel-python.json", "r") as file:
    student_data = json.load(file)

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api")
def get_marks(name: list[str] = Query(None)):
    if not name:
        return {"error": "Please provide at least one name."}
    
    marks = [student_data.get(n, None) for n in name]
    return {"marks": marks}
