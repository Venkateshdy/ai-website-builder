from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os
from groq import Groq

# Initialize FastAPI
app = FastAPI()

# Enable CORS (important for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class PromptRequest(BaseModel):
    text: str

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")  # MUST be set in Render
)

# Root route (test)
@app.get("/")
def home():
    return {"message": "AI Website Builder Running 🚀"}

# Generate website route
@app.post("/generate")
def generate(request: PromptRequest):
    try:
        prompt = f"""
        Create a complete HTML website with inline CSS and JavaScript.
        User request: {request.text}

        Requirements:
        - Modern UI
        - Responsive design
        - Clean layout
        - Include headings, sections, styling
        """

        response = client.chat.completions.create(
            model="llama3-70b-8192",  # working Groq model
            messages=[
                {"role": "system", "content": "You are a creative web developer."},
                {"role": "user", "content": prompt}
            ],
        )

        html_output = response.choices[0].message.content

        return {"html": html_output}

    except Exception as e:
        return {"error": str(e)}