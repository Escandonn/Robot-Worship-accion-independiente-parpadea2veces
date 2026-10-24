from groq import Groq
import os

c = Groq(api_key=os.getenv("GROQ_API_KEY"))
try:
    r = c.chat.completions.create(messages=[{"role": "user", "content": "hi"}], model="llama-3.3-70b-versatile", max_tokens=10)
    print(r.choices[0].message.content)
except Exception as e:
    print(e)
