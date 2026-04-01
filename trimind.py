import requests, os, json, datetime, hashlib

GROQ_KEY = os.environ.get("GROQ_KEY")
HISTORY_FILE = os.path.expanduser("~/Terron89/chat_history.json")
CONFIG_FILE = os.path.expanduser("~/Terron89/config.json")

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    return {
        "pin": None,
        "personalities": {
            "Claude": "You are Claude, a thoughtful and nuanced AI. Be analytical and balanced.",
            "ChatGPT": "You are ChatGPT, a helpful and direct AI. Be practical and clear.",
            "Gemini": "You are Gemini, a creative and curious AI. Be imaginative and broad."
        },
        "theme": "dark"
    }

def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)

def hash_pin(pin):
    return hashlib.sha256(pin.encode()).hexdigest()

def check_pin(config):
    if config["pin"] is None:
        print("\nNo PIN set. Set one now.")
        pin = input("Enter new PIN: ")
        config["pin"] = hash_pin(pin)
        save_config(config)
        print("PIN set!")
        return True
    attempts = 3
    while attempts > 0:
        pin = input("\nEnter PIN: ")
        if hash_pin(pin) == config["pin"]:
            print("Access granted!")
            return True
        attempts -= 1
        print(f"Wrong PIN. {attempts} attempts left.")
    print("Locked out!")
    return False

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def ask_ai(question, personality, config):
    prompt = config["personalities"].get(personality, "You are a helpful AI.")
    try:
        r = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer "+GROQ_KEY, "Content-Type": "application/json"},
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": question}
                ]
            }
        )
        return r.json()["choices"][0]["message"]["content"]
    except:
        return str(r.json())

def conference_room(question, history, config):
    print("\n--- CONFERENCE ROOM ---\n")
    answers = []
    for ai in ["Claude", "ChatGPT", "Gemini"]:
        print(f"[{ai}] thinking...")
        ans = ask_ai(question, ai, config)
        print(f"\n[{ai}]: {ans}\n")
        answers.append({"ai": ai, "answer": ans})
    summary = ask_ai(f"Summarize these 3 answers into one final answer:\n1. {answers[0]['answer']}\n2. {answers[1]['answer']}\n3. {answers[2]['answer']}", "Claude", config)
    print(f"\n--- TRIMIND FINAL ANSWER ---\n[Trimind]: {summary}")
    history.append({"time": str(datetime.datetime.now()), "mode": "conference", "question": question, "final": summary})
    save_history(history)

def settings_menu(config):
    while True:
        print("\n--- SETTINGS ---")
        print("1. Change PIN")
        print("2. Edit Claude personality")
        print("3. Edit ChatGPT personality")
        print("4. Edit Gemini personality")
        print("5. View current personalities")
        print("6. Back")
        choice = input("\nChoice: ")
        if choice == "6":
            break
        elif choice == "1":
            pin = input("New PIN: ")
            config["pin"] = hash_pin(pin)
            save_config(config)
            print("PIN changed!")
        elif choice in ["2", "3", "4"]:
            ai = ["Claude", "ChatGPT", "Gemini"][int(choice)-2]
            print(f"\nCurrent: {config['personalities'][ai]}")
            new = input(f"New personality for {ai}: ")
            if new:
                config["personalities"][ai] = new
                save_config(config)
                print("Saved!")
        elif choice == "5":
            for ai, p in config["personalities"].items():
                print(f"\n[{ai}]: {p}")

config = load_config()
if not check_pin(config):
    exit()

history = load_history()

while True:
    print("\n=== TRIMIND-AI ===")
    print("1. Ask one AI")
    print("2. Conference room")
    print("3. View history")
    print("4. Settings")
    print("5. Exit")
    choice = input("\nChoice: ")
    if choice == "5":
        break
    elif choice == "4":
        settings_menu(config)
    elif choice == "3":
        if not history:
            print("No history yet.")
        else:
            for h in history[-5:]:
                print(f"\n[{h['time']}] Q: {h['question']}")
    elif choice in ["1", "2"]:
        question = input("Your question: ")
        if choice == "1":
            ans = ask_ai(question, "Claude", config)
            print("\n[AI]: " + ans)
            history.append({"time": str(datetime.datetime.now()), "mode": "single", "question": question, "answer": ans})
            save_history(history)
        elif choice == "2":
            conference_room(question, history, config)
