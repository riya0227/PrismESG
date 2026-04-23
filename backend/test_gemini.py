import os
from google import genai

client = genai.Client(api_key=os.getenv("AIzaSyBPBydq6gNAcDCzvKxEneKGtv-SbjlOBJ0"))

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents="Explain ESG in simple terms"
)

print("\n--- GEMINI RESPONSE ---")
print(response.text)