import os
from dotenv import load_dotenv
import groq

load_dotenv()
api_key = os.getenv("GROQ_API_KEY") or os.getenv("GEMINI_API_KEY")
client = groq.Groq(api_key=api_key)

for model in client.models.list():
    print(model.id if hasattr(model, 'id') else getattr(model, 'name', None))


# import os
# from dotenv import load_dotenv
# from google import genai

# load_dotenv()

# client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# try:
#     response = client.models.generate_content(
#         model="gemini-2.5-flash",
#         contents="Say hello"
#     )
#     print("SUCCESS:", response.text)
# except Exception as e:
#     print("ERROR:", e)