from dotenv import load_dotenv  # loads .env for local development
import os
import openai
import logging

# NOTE: This module wraps the LLM client for the app. Keep logic small and
# focused: build a minimal prompt, call the model, and return the assistant text.

# Try to import dataset loader helper (optional). If present, load dataset for use in chat logic.
# The dataset loader is optional because not all deployments will need or want
# the additional dataset dependency or memory usage.
try:
    from .dataset_loader import get_vet_dataset
except Exception:
    # dataset_loader may not exist in some environments; fall back gracefully.
    get_vet_dataset = None

# Load environment variables from an .env file for local development.
# In production, prefer real environment variables or a secret manager.
load_dotenv()
if not os.getenv("OPENAI_API_KEY") and os.path.exists("backend/.env"):
    # Fallback to backend/.env for cases where the backend runs with a different cwd
    # during development/test runs.
    load_dotenv("backend/.env")

# Accept either `OPENAI_API_KEY` (preferred) or a legacy `API_KEY` for backwards compatibility.
# Fail fast with a clear error if no key is present to help developers notice missing config.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError("OpenAI API key not found. Set OPENAI_API_KEY in .env or environment variables.")

# Initialize OpenAI client with the environment key (do NOT print the key anywhere).
# The `openai` SDK is used here; keep the client usage isolated to this module.
client = openai.OpenAI(api_key=OPENAI_API_KEY)

# System prompt: guides assistant behavior for every request. Keep concise and
# explicit about disallowed behavior (no medical advice, diagnoses, or product
# recommendations). The assistant should only generate three simple,
# educational questions owners can ask their veterinarian.
conversation_history = [
    {
        "role": "system",
        "content": (
            "You are a Veterinary Communication Assistant. Your goal is to improve dog owners'"
            " conversations with their veterinarian. You do not provide medical advice, diagnoses,"
            " treatment plans, or product recommendations. Instead, generate 3 simple, educational"
            " questions the owner can ask their veterinarian. "
            "Consider the dog's Age and Health Status when formulating these questions. "
            "Draw upon veterinary knowledge consistent with the ViggoVet dataset."
        ),
    }
]

def chat_with_gpt(user_input: str):
        """Send `user_input` (age + health statuses) to the LLM and return the assistant reply.

        Design goals / safety:
        - Only a short, focused conversation is sent (system + current user input)
            to avoid leaking history and limit token usage.
        - Use conservative model parameters (low temperature, penalties) so output
            is deterministic and concise for medical-adjacent content.

        Returns:
                assistant_text (str): the raw assistant response (expected to contain
                three short questions). Callers may split into lines if needed.
        """
        
        # Ensure dataset is loaded (lazy load) to provide context if needed in future
        if get_vet_dataset:
             _ = get_vet_dataset()

        # Build a minimal messages payload: system prompt + current user input.
        # Keeps the request focused and reduces the chance of leaking other data.
        messages = [conversation_history[0], {"role": "user", "content": user_input}]

        # Call the OpenAI chat completion endpoint. This may raise exceptions from
        # the client/network; callers should handle exceptions if needed.
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                temperature=0.3,
                frequency_penalty=0.7,
                presence_penalty=0.25,
                max_tokens=200,
        )

        # Extract assistant text from response (SDK returns a nested choices structure).
        assistant_text = response.choices[0].message.content

        # Append assistant reply to in-memory history for debugging/inspection only.
        # IMPORTANT: Do not persist this history or include sensitive user data in logs.
        conversation_history.append({"role": "assistant", "content": assistant_text})

        # Return the assistant's text (the generated 3 vet questions).
        return assistant_text

