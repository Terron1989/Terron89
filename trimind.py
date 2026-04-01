import requests, os

GROQ_KEY = os.environ.get("GROQ_KEY")

def ask_ai(question, personality):
    prompts = {
        "Claude": "You are Claude, a thoughtful and nuanced AI. Be analytical and balanced.",
        "ChatGPT": "You are ChatGPT, a helpful and direct AI. Be practical and clear.",
        "Gemini": "You are Gemini, a creative and curious AI. Be imaginative and broad."
    }
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer "+GROQ_KEY, "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": prompts[personality]},
                    {"role": "user", "content": question}
                ]
            }
        )
        return r.json()["choices"][0]["message"]["content"]
    except:
        return str(r.json())

def conference_room(question):
    print("\n--- CONFERENCE ROOM ---\n")
    answers = []
    for ai in ["Claude", "ChatGPT", "Gemini"]:
        print(f"[{ai}] thinking...")
        ans = ask_ai(question, ai)
        print(f"\n[{ai}]: {ans}\n")
        answers.append(ans)
    print("\n--- TRIMIND FINAL ANSWER ---\n")
    summary = ask_ai(f"Summarize these 3 answers into one final answer:\n1. {answers[0]}\n2. {answers[1]}\n3. {answers[2]}", "Claude")
    print(f"[Trimind]: {summary}")

while True:
    print("\n1. Ask one AI\n2. Conference room\n3. Exit")
    choice = input("\nChoice: ")
    if choice == "3":
        break
    question = input("Your question: ")
    if choice == "1":
        print("\n[AI]: " + ask_ai(question, "Claude"))
    elif choice == "2":
        conference_room(question)
