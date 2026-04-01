import requests, os

GROQ_KEY = os.environ.get("GROQ_KEY")

def ask_groq(question):
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer "+GROQ_KEY, "Content-Type": "application/json"},
            json={"model": "llama-3.3-70b-versatile", "messages": [{"role": "user", "content": question}]}
        )
        return r.json()["choices"][0]["message"]["content"]
    except:
        return str(r.json())

while True:
    print("\n1. Ask AI\n2. Conference room\n3. Exit")
    choice = input("\nChoice: ")
    if choice == "3":
        break
    question = input("Your question: ")
    if choice == "1":
        print("\n[Groq/Llama]: " + ask_groq(question))
