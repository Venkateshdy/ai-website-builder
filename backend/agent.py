from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Planner
def planner(prompt):
    return f"Plan a website structure for: {prompt}"

# Designer
def designer(plan):
    return f"Design modern UI/UX for: {plan}"

# Developer (main AI)
def developer(design):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Generate complete HTML, CSS website code:\n{design}"
            }
        ]
    )
    return response.choices[0].message.content

# Run all agents
def run_agents(prompt):
    plan = planner(prompt)
    design = designer(plan)
    code = developer(design)
    return code, "Generated successfully"