from fastapi import FastAPI, Request
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
WORKFLOW_ID = os.getenv("WORKFLOW_ID")

@app.post("/jotform-to-workhub")
async def receive_from_jotform(request: Request):
    form_data = await request.json()

    # Step 1: Get OAuth Token
    token_response = requests.post(
        "https://app.workhub24.com/api/auth/token",
        json={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "client_credentials"
        },
        headers={"Content-Type": "application/json"}
    )

    if token_response.status_code != 200:
        return {"error": "Failed to get access token", "details": token_response.text}

    token = token_response.json().get("access_token")

    # Step 2: Format Data for WorkHub24 (expand this as needed)
    payload = {
        "title": form_data.get("title", "New Submission")
    }

    # Step 3: Post to WorkHub24
    workhub_response = requests.post(
        f"https://app.workhub24.com/api/workflows/{TENANT_ID}/{WORKFLOW_ID}/cards",
        json=payload,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
    )

    return {
        "status": workhub_response.status_code,
        "workhub_response": workhub_response.json()
    }
