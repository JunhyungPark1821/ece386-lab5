"""Passes a personal intro statement to an LLM.
The LLM produces valid JSON that could be ingested into a database to create a new user.

Modified from https://ollama.com/blog/structured-outputs
"""
from ollama import chat
from pydantic import BaseModel
import sys


class User(BaseModel):
    name: str
    age: int
    hometown: str
    squadron: int
    major: str


if __name__ == "__main__":
    # Ensure user passes required arguments
    if len(sys.argv) != 2:
        print('Usage: python3 ./user_creation.py "<introduction message>"')
        print("Error")
        sys.exit(1)

    response = chat(
        messages=[
            {
                "role": "system",
                "content": "You are a JSON generator. Process introduction statement from a new user into valid JSON.",
            },
            {
                "role": "user",
                "content": sys.argv[1],
            },
        ],
        model="gemma3:1b",
        format=User.model_json_schema(),
    )

    print(response.message.content)
