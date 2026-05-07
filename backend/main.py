from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os

from agent import run_agents

app = FastAPI()

# ✅ Enable CORS (frontend can call backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Absolute path setup
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATED_DIR = os.path.join(BASE_DIR, "generated_sites")

# ✅ Ensure folder exists
os.makedirs(GENERATED_DIR, exist_ok=True)

# ✅ Mount static files (VERY IMPORTANT)
app.mount(
    "/generated_sites",
    StaticFiles(directory=GENERATED_DIR),
    name="generated_sites"
)

# Request model
class Prompt(BaseModel):
    text: str

# Root check (optional but useful)
@app.get("/")
def home():
    return {"message": "AI Website Builder Running 🚀"}

# Generate API
@app.post("/generate")
def generate(prompt: Prompt):
    try:
        print("Received prompt:", prompt.text)

        code, _ = run_agents(prompt.text)

        file_path = os.path.join(GENERATED_DIR, "index.html")

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(code)

        print("Saved file at:", file_path)
        print("Code preview:", code[:200])

        return {
            "status": "success",
            "file": "/generated_sites/index.html"
        }

    except Exception as e:
        return {"error": str(e)}