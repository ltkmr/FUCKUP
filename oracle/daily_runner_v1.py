import os
import datetime
import subprocess
from iching import throw_coins, render_hexagram, hexagram_number, get_hexagram_info
from data_fetcher import main as fetch_data
import ollama

# Step 1: Prepare daily environment
today = datetime.date.today().isoformat()
base_dir = os.path.join(os.path.dirname(__file__), "..", "data", today)
archive_dir = os.path.join(os.path.dirname(__file__), "..", "archive")
os.makedirs(base_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

def collect_data():
    print("📰 Collecting data...")
    fetch_data()
    print("✅ Data collected.")

def generate_iching():
    print("🧙 Generating I-Ching hexagram...")
    hexagram = throw_coins()
    hexagram_text = render_hexagram(hexagram)
    print(f"✨ Today's hexagram:\n{hexagram_text}\n")
    return hexagram, hexagram_text



def build_prompt(hexagram_text, number, name, meaning):
    data_summary = ""
    for filename in os.listdir(base_dir):
        filepath = os.path.join(base_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            data_summary += f"\n\n--- {filename} ---\n\n"
            data_summary += f.read()

    prompt = (
        "You are FUCKUP², First Universal Cybernetic-Kinetic-Ultramicro-Programmer, an occult.technological oracle machine. "
        "Based on the following hexagram and today's world data, compose a summary on today's events. After that devine a cryptic prophecy and finally give a practical suggestion for action.\n\n"
        "Hexagram #{number}: {name}\n"
        "Meaning: {meaning}\n\n"
        "Hexagram Lines:\n{hexagram_text}\n\n"
        "World Data:\n{data_summary}\n\n"
        "Your answer must contain the following parts: 1. The news summary. 2. A surreal, enigmatic prophecy text. 3. A one sentence call to action."
    )
    return prompt

def generate_prophecy(prompt):
    print("🔮 Generating prophecy with local LLM...")
    response = ollama.chat(
        model="mistral",
        messages=[
            {"role": "system", "content": "You are a wise, cryptic oracle machine."},
            {"role": "user", "content": prompt}
        ]
    )
    prophecy = response['message']['content']
    print("✅ Prophecy generated.\n")
    return prophecy

def archive_prophecy(prophecy):
    filename = os.path.join(archive_dir, f"{today}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(prophecy)
    print(f"📜 Prophecy archived at {filename}")

def format_printout(number, name, meaning, hexagram_text, prophecy):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    header = f"""
==========================================
    FUCKUP² ORACLE — Daily Prophecy
    {date_str}
==========================================

Hexagram #{number}: {name}
Meaning: {meaning}

Hexagram Lines:
{hexagram_text}

Prophecy:
{prophecy}

==========================================
"""
    return header



def print_prophecy(prophecy):
    try:
        subprocess.run(['lp'], input=prophecy.encode('utf-8'), check=True)
        print("🖨️ Prophecy sent to printer.")
    except Exception as e:
        print(f"⚠️ Printer error: {e}")

def main():
    collect_data()
    lines, hexagram_text = generate_iching()
    number = hexagram_number(lines)
    name, meaning = get_hexagram_info(number)
    print(f"🧙 Today's Hexagram: #{number} - {name}")
    print(f"Meaning: {meaning}\n")
    prompt = build_prompt(hexagram_text, number, name, meaning)
    prophecy = generate_prophecy(prompt)
    formatted_output = format_printout(number, name, meaning, hexagram_text, prophecy)
    archive_prophecy(formatted_output)
    print_prophecy(formatted_output)
    print("🎉 Daily oracle cycle complete!")

if __name__ == "__main__":
    main()

