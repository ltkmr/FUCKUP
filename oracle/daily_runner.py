import subprocess
import unicodedata
from datetime import datetime
from pathlib import Path

import ollama
from data_fetcher import main as fetch_data
from iching import get_hexagram_info, hexagram_number, render_hexagram, throw_coins

DEBUG_MODE = False  # Set to False for normal daily runs
MODEL_NAME = "gemma3:12b"  # Change this to "llama3", "custom-model", etc.

from prompts import (
    ADVISOR_INSTRUCTION,
    ADVISOR_SYSTEM_PROMPT,
    ANALYST_INSTRUCTION,
    ANALYST_SYSTEM_PROMPT,
    COMPRESSION_INSTRUCTION,
    COMPRESSION_SYSTEM_PROMPT,
    ORACLE_INSTRUCTION,
    ORACLE_SYSTEM_PROMPT,
)

# Prepare directories
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
base_dir = Path(__file__).parent.parent / "data" / timestamp
archive_dir = Path(__file__).parent.parent / ".." / "archive"

base_dir.mkdir(parents=True, exist_ok=True)
archive_dir.mkdir(parents=True, exist_ok=True)

# Define subdirectories
raw_data_dir = base_dir / "raw"
compressed_data_dir = base_dir / "compressed"
logs_dir = base_dir / "logs"

# Ensure they exist
raw_data_dir.mkdir(parents=True, exist_ok=True)
compressed_data_dir.mkdir(parents=True, exist_ok=True)
logs_dir.mkdir(parents=True, exist_ok=True)


# Step 1: Data Collection
def collect_data():
    if DEBUG_MODE:
        print("🛠️ Debug mode: Skipping data collection.")
    else:
        print("📰 Collecting data...")
        fetch_data(raw_data_dir)
        print("✅ Data collected.")


# Step 2: Generate I-Ging hexagram
def generate_iching():
    print("🧙 Generating I-Ging hexagram...")
    lines = throw_coins()
    hexagram_text = render_hexagram(lines)
    number = hexagram_number(lines)
    name, meaning = get_hexagram_info(number)
    print(f"✨ Today's Hexagram: #{number} - {name}")
    print(f"Meaning: {meaning}\n")
    return lines, hexagram_text, number, name, meaning


# Step 4: LLM helper

def run_llm(system_prompt, user_prompt, model_name=MODEL_NAME):
    response = ollama.chat(
        model=model_name,
        messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
    )
    return response["message"]["content"].strip()


# Step 5: Format printout
    date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
    hexagram_unicode = chr(0x4DC0 + (number - 1))
    header = f"""
==========================================
    FUCKUP² ORACLE — Daily Prophecy
    {date_str}
==========================================

Hexagram #{number}: {name} {hexagram_unicode}
Meaning: {meaning}

------------------------------------------
Summary of current events:
{analyst_summary}

Hollistic I-Ging interpretation:
{oracle_message}

Action recommendation:
{advisor_recommendation}
==========================================
"""

    # 🛠️ Clean up lines and add form feed for printer
    safe_header = "\n".join(line.strip() for line in header.splitlines())
    return safe_header + "\n\f"


# Step 6: Clean up the LLM output for printer lp compatibility
def sanitize_for_printer(text):
    # Normalize Unicode to remove fancy characters
    normalized = unicodedata.normalize("NFKD", text)
    # Encode to ASCII bytes, ignore errors, then decode back to string
    ascii_text = normalized.encode("ascii", "ignore").decode("ascii")
    return ascii_text


# Step 7: Archive the prophecy
def archive_prophecy(text):
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = archive_dir / f"{timestamp}.txt"
    with filename.open("w", encoding="utf-8") as f:
        f.write(text)
    print(f"📜 Prophecy archived at {filename}")


# Step 8: Print the prophecy
def print_prophecy(text):
    try:
        subprocess.run(["lp"], input=text.encode("utf-8"), check=True)
        print("🖨️ Prophecy sent to printer.")
    except Exception as e:
        print(f"⚠️ Printer error: {e}")


# Step 9: Show folder structure
def print_folder_structure(base_path):
    print("\n📂 Current Data Directory Structure:")
    for root, _, files in base_path.walk():
        level = len(base_path.relative_to(root).parts)
        indent = " " * 4 * level
        print(f"{indent}{root.name}/")
        sub_indent = " " * 4 * (level + 1)
        for f in files:
            print(f"{sub_indent}{f}")
    print()


# Helpers
def clean_conversational_tails(text):
    """Remove common conversational endings and phrases."""
    endings = [
        "Let me know if you'd like me to elaborate.",
        "If you'd like more details, feel free to ask.",
        "Let me know if you need anything else.",
        "Feel free to ask if you want more insights.",
        "Hope this helps!",
        "I'm here if you need more information."
        "Do you want me to elaborate on any of these points or focus on a specific aspect of the news?"
        "I hope this summary is helpful!"
        "If you have any specific questions or need further details about a particular event mentioned in these articles, feel free to ask!",
    ]
    lines = text.splitlines()
    filtered_lines = [line for line in lines if not any(ending.lower() in line.lower() for ending in endings)]
    return "\n".join(filtered_lines).strip()

def run_agent(agent_name, system_prompt, instruction, dynamic_input, model_name, debug_message="DEBUG: Sample output."):
    print(f"{agent_name} is processing...")
    print(f"🧩 {agent_name} input length: {len(dynamic_input)} characters")

    # Prepare logs folder
    agent_path_name = (
        agent_name.replace(" ", "_").replace("🤖", "").replace("🧙", "").replace("🧭", "").replace("🧩", "").strip()
    )
    agent_log_file: Path = (logs_dir / agent_path_name).with_suffix(".txt")
    agent_log_file.mkdir(parents=True, exists_ok=True)

    # Log input
    with agent_log_file.open("w", encoding="utf-8") as f:
        f.write("===== INPUT =====\n")
        f.write(dynamic_input.strip() + "\n\n")

    if DEBUG_MODE:
        output = debug_message
    else:
        user_prompt = f"{instruction}\n\n{dynamic_input}"
        try:
            output = run_llm(system_prompt=system_prompt, user_prompt=user_prompt, model_name=model_name)
        except Exception as e:
            print(f"⚠️ Error in {agent_name}: {e}")
            output = debug_message

    output = clean_conversational_tails(output)

    # Log output
    with agent_log_file.open("a", encoding="utf-8") as f:
        f.write("===== OUTPUT =====\n")
        f.write(output.strip() + "\n")

    print(f"✅ {agent_name} completed. Logged to {agent_log_file}")
    return output



def safe_truncate(text, max_chars=100000):
    """Truncate text to avoid overloading model input."""
    return text[:max_chars]


# Main runner
def main():
    # Run agents
    # Step 1: Collect data and prepare hexagram
    collect_data()
    lines, hexagram_text, number, name, meaning = generate_iching()

    # Step 2: Prepare data input (read raw feed files)
    print("🧩 Preparing raw data for compression...")
    raw_texts = []

    for filename in raw_data_dir.iterdir():
        filepath = raw_data_dir / filename
        with filepath.open("r", encoding="utf-8") as f:
            raw_content = f.read()
            raw_texts.append(f"--- {filename} ---\n{safe_truncate(raw_content)}")

    print("✅ Raw data prepared.")

    # Step 3: Compress data using per-source compression
    print("🧩 Starting per-source compression...")

    compressed_chunks = []

    for filename in raw_data_dir.iterdir():
        filepath = raw_data_dir / filename
        with filepath.open("r", encoding="utf-8") as f:
            raw_content = f.read()

        safe_input = safe_truncate(raw_content)

        agent_label = f"🧩 Compression Agent [{filename.replace('.txt','')}]"

        compressed = run_agent(
            agent_label,
            COMPRESSION_SYSTEM_PROMPT,
            COMPRESSION_INSTRUCTION,
            safe_input,
            model_name="dolphin3:latest",
            debug_message=f"DEBUG: Sample compression for {filename}",
        )
        if not DEBUG_MODE:
            print(f"📏 {filename} → Input: {len(safe_input)} chars | Output: {len(compressed)} chars")
        compressed_chunks.append(f"--- {filename} ---\n{compressed.strip()}\n")

    # Merge all compressed chunks into one summary
    compressed_data_summary = "\n".join(compressed_chunks)

    # Save the combined result
    compressed_log = compressed_data_dir / "compressed_input.txt"
    with compressed_log.open("w", encoding="utf-8") as f:
        f.write(compressed_data_summary)
    print(f"🗂️ Combined compressed input saved to {compressed_log}")

    # Save compressed output for review
    compressed_log = compressed_data_dir / "compressed_input.txt"
    with compressed_log.open("w", encoding="utf-8") as f:
        f.write(compressed_data_summary)
    print(f"🗂️ Compressed input saved to {compressed_log}")

    # Step 4: Run the rest of the Agents.
    analyst_summary = run_agent(
        "🤖 Analyst Agent",
        ANALYST_SYSTEM_PROMPT,
        ANALYST_INSTRUCTION,
        compressed_data_summary,
        model_name="dolphin3:latest",  # ✅ Faster, leaner model
        debug_message="DEBUG: Sample analyst summary.",
    )

    oracle_dynamic_input = f"Hexagram #{number}: {name}\nMeaning: {meaning}\n\n" f"Analyst Summary:\n{analyst_summary}"

    oracle_message = run_agent(
        "🧙 Oracle Agent",
        ORACLE_SYSTEM_PROMPT,
        ORACLE_INSTRUCTION,
        oracle_dynamic_input,
        model_name="gemma3:12b",  # ✅ Creative, rich model
        debug_message="DEBUG: Sample Oracle Message.",
    )

    advisor_dynamic_input = f"[ANALYST SUMMARY]\n{analyst_summary}\n\n" f"[ORACLE PROPHECY]\n{oracle_message}"

    advisor_recommendation = run_agent(
        "🧭 Advisor Agent",
        ADVISOR_SYSTEM_PROMPT,
        ADVISOR_INSTRUCTION,
        advisor_dynamic_input,
        model_name="gemma3:12b",  # ✅ Authoritative output
        debug_message="DEBUG: Sample Advisor Recommendation.",
    )
    # Format, archive, and print
    formatted_output = format_printout(number, name, meaning, hexagram_text, analyst_summary, oracle_message, advisor_recommendation)
    safe_output = sanitize_for_printer(formatted_output)
    archive_prophecy(formatted_output)
    print_prophecy(safe_output)

    print("🎉 Daily oracle cycle complete!")
    print_folder_structure(base_dir)


if __name__ == "__main__":
    main()

print("🌐 Updating web archive...")
subprocess.run(["python", "oracle/generate_html.py"], check=True)
print("✅ Web archive updated.")
print("✨ FUCKUP machine cycle complete. Ready for tomorrow's divination.")
