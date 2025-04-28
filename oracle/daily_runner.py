import os
import datetime
import subprocess
from iching import throw_coins, render_hexagram, hexagram_number, get_hexagram_info
from data_fetcher import main as fetch_data
from utils import gematria_value
from collections import defaultdict
import ollama
import unicodedata
import subprocess

DEBUG_MODE = False  # Set to False for normal daily runs
MODEL_NAME = "qwen2.5"  # Change this to "llama3", "custom-model", etc.

from prompts import (
    gematria_system_prompt,
    gematria_instruction,
    compression_system_prompt,
    compression_instruction,
    analyst_system_prompt,
    analyst_instruction,
    oracle_system_prompt,
    oracle_instruction,
    advisor_system_prompt,
    advisor_instruction
)

# Prepare directories
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
base_dir = os.path.join(os.path.dirname(__file__), "..", "data", timestamp)
archive_dir = os.path.join(os.path.dirname(__file__), "..", "archive")
os.makedirs(base_dir, exist_ok=True)
os.makedirs(archive_dir, exist_ok=True)

# Define subdirectories
raw_data_dir = os.path.join(base_dir, "raw")
compressed_data_dir = os.path.join(base_dir, "compressed")
logs_dir = os.path.join(base_dir, "logs")

# Ensure they exist
os.makedirs(raw_data_dir, exist_ok=True)
os.makedirs(compressed_data_dir, exist_ok=True)
os.makedirs(logs_dir, exist_ok=True)

# Step 1: Data Collection
def collect_data():
    if DEBUG_MODE:
        print("🛠️ Debug mode: Skipping data collection.")
    else:
        print("📰 Collecting data...")
        fetch_data(base_dir)
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

def run_llm(system_prompt, user_prompt, model_name=MODEL_NAME, temperature=0.7):
    response = ollama.chat(
        model=model_name,
        # temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
    return response['message']['content'].strip()

# Step 5: Format printout
def format_printout(number, name, meaning, hexagram_text, analyst_summary, oracle_message, advisor_recommendation, gematria_outputs=None):
    date_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    gematria_block = ""
    hexagram_unicode = chr(0x4DC0 + (number - 1))
    if gematria_outputs:
        gematria_block += "\n✡ GEMATRIA SYNCHRONICITY ✡\n"
    for result in gematria_outputs:
        gematria_block += f"\n── Value {result['value']} ──\n"
        for i, (title, summary) in enumerate(result['entries'], start=1):
            gematria_block += f"{i}. {title}\n{summary}\n\n"
        gematria_block += f"🔮 {result['message'].strip()}\n"
        gematria_block += "─" * 40 + "\n"

    header = f"""
============================================================================================
    FUCKUP² ORACLE — Daily Prophecy
    {date_str}
============================================================================================

Today's Hexagram #{number}: {name} {hexagram_unicode}
Meaning: {meaning}

--------------------------------------------------------------------------------------------
Summary of current events:
{analyst_summary}
"""

    if gematria_block:
        header += f"\n{gematria_block}"

    header += f"""

Hollistic I-Ging interpretation:
{oracle_message}

Action recommendation:
{advisor_recommendation}

END OF FILE
"""
 
    
    # 🛠️ Clean up lines and add form feed for printer
    safe_header = "\n".join(line.strip() for line in header.splitlines())
    return safe_header + "\n\f"

# Step 6: Clean up the LLM output for printer lp compatibility
def sanitize_for_printer(text):
    # Normalize Unicode to remove fancy characters
    normalized = unicodedata.normalize('NFKD', text)
    # Encode to ASCII bytes, ignore errors, then decode back to string
    ascii_text = normalized.encode('ascii', 'ignore').decode('ascii')
    return ascii_text

# Step 7: Archive the prophecy
def archive_prophecy(text):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")
    filename = os.path.join(archive_dir, f"{timestamp}.txt")
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"📜 Prophecy archived at {filename}")

# Step 8: Print the prophecy
def print_prophecy(text):
    try:
        subprocess.run(['lp'], input=text.encode('utf-8'), check=True)
        print("🖨️ Prophecy sent to printer.")
    except Exception as e:
        print(f"⚠️ Printer error: {e}")

# Step 9: Show folder structure
def print_folder_structure(base_path):
    print("\n📂 Current Data Directory Structure:")
    for root, dirs, files in os.walk(base_path):
        level = root.replace(base_path, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
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
        "If you have any specific questions or need further details about a particular event mentioned in these articles, feel free to ask!"
    ]
    lines = text.splitlines()
    filtered_lines = [line for line in lines if not any(ending.lower() in line.lower() for ending in endings)]
    return "\n".join(filtered_lines).strip()

def run_agent(agent_name, system_prompt, instruction, dynamic_input, model_name, temperature=0.7, debug_message="DEBUG: Sample output."):
    print(f"{agent_name} is processing...")
    print(f"🧩 {agent_name} input length: {len(dynamic_input)} characters")

    # Prepare logs folder
    agent_log_file = os.path.join(logs_dir, f"{agent_name.replace(' ', '_').replace('🤖','').replace('🧙','').replace('🧭','').replace('🧩','').strip()}.txt")
    os.makedirs(os.path.dirname(agent_log_file), exist_ok=True)

    # Log input
    with open(agent_log_file, "w", encoding="utf-8") as f:
        f.write("===== INPUT =====\n")
        f.write(dynamic_input.strip() + "\n\n")

    if DEBUG_MODE:
        output = debug_message
    else:
        user_prompt = f"{instruction}\n\n{dynamic_input}"
        try:
            output = run_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt,
                # temperature=temperature,
                model_name=model_name
            )
        except Exception as e:
            print(f"⚠️ Error in {agent_name}: {e}")
            output = debug_message

    output = clean_conversational_tails(output)

    # Log output
    with open(agent_log_file, "a", encoding="utf-8") as f:
        f.write("===== OUTPUT =====\n")
        f.write(output.strip() + "\n")

    print(f"✅ {agent_name} completed. Logged to {agent_log_file}")
    return output
# gematria helper
def collect_gematria_collisions(raw_data_dir, max_length=150):
    """
    Scans raw summaries and groups short ones by their gematria value.
    Returns a dict: { gematria_value: [ (title, summary) ] }
    """
    gematria_groups = defaultdict(list)

    for filename in os.listdir(raw_data_dir):
        filepath = os.path.join(raw_data_dir, filename)
        if os.path.isdir(filepath):
            continue

        with open(filepath, "r", encoding="utf-8") as f:
            entry_lines = []
            title = None
            summary = None

            for line in f:
                line = line.strip()
                if line.startswith("Title:"):
                    title = line[6:].strip()
                elif line.startswith("Summary:"):
                    summary = line[8:].strip()

                if title and summary:
                    if len(summary) < max_length:
                        value = gematria_value(summary)
                        gematria_groups[value].append((title, summary))
                    title = None
                    summary = None

    # Filter only collisions (value occurs more than once)
    collisions = {k: v for k, v in gematria_groups.items() if len(v) > 1}
    return collisions

def safe_truncate(text, max_chars=10000):
    """Truncate text to avoid overloading model input."""
    return text[:max_chars]

# Main runner
def main():

    # Collect data and prepare hexagram
    collect_data()
    lines, hexagram_text, number, name, meaning = generate_iching()
    
    # Check for gematria syncronicity
    gematria_hits = collect_gematria_collisions(raw_data_dir)
    if gematria_hits:
        print(f"🔮 Found {len(gematria_hits)} Gematria synchronistic collisions!")
        for val, items in gematria_hits.items():
            print(f"✡ Value {val}: {len(items)} items")
    else:
        print("🕳️ No Gematria collisions today.")

    gematria_outputs = []

    for value, entries in gematria_hits.items():
        # Create a surreal input block for the agent
        formatted = f"GEMATRIA VALUE: {value}\n\n"
        for idx, (title, summary) in enumerate(entries, start=1):
            formatted += f"{idx}. {title}\n{summary}\n\n"

        surreal_revelation = run_agent(
            f"🧿 Gematria Agent ({value})",
            gematria_system_prompt,
            gematria_instruction,
            formatted.strip(),
            model_name="qwen2.5",
            debug_message="DEBUG: Surreal gematria connection."
        )

        gematria_outputs.append({
            "value": value,
            "entries": entries,
            "message": surreal_revelation
        })
        if gematria_outputs:
            print("\n✡️ GEMATRIA SYNCHRONICITY ✡️")
            for result in gematria_outputs:
                print(f"\n── Gematria {result['value']} ──")
                for i, (title, summary) in enumerate(result['entries'], start=1):
                    print(f"{i}. {title} — {summary}")
                print(f"\n🔮 {result['message']}\n")

    # Prepare data input (read raw feed files)
    print("🧩 Preparing raw data for compression...")
    raw_texts = []

    for filename in os.listdir(raw_data_dir):
        filepath = os.path.join(raw_data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_content = f.read()
            raw_texts.append(f"--- {filename} ---\n{safe_truncate(raw_content)}")

    full_raw_input = "\n\n".join(raw_texts)

    print("✅ Raw data prepared.")

    # Step 3: Compress data using per-source compression
    print("🧩 Starting per-source compression...")

    compressed_chunks = []

    for filename in os.listdir(raw_data_dir):
        filepath = os.path.join(raw_data_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            raw_content = f.read()

        safe_input = safe_truncate(raw_content)

        agent_label = f"🧩 Compression Agent [{filename.replace('.txt','')}]"

        compressed = run_agent(
            agent_label,
            compression_system_prompt,
            compression_instruction,
            safe_input,
            model_name="qwen2.5",
            debug_message=f"DEBUG: Sample compression for {filename}"
        )
        if not DEBUG_MODE:
            print(f"📏 {filename} → Input: {len(safe_input)} chars | Output: {len(compressed)} chars")
        compressed_chunks.append(f"--- {filename} ---\n{compressed.strip()}\n")

    # Merge all compressed chunks into one summary
    compressed_data_summary = "\n".join(compressed_chunks)

    # Save the combined result
    compressed_log = os.path.join(compressed_data_dir, "compressed_input.txt")
    with open(compressed_log, "w", encoding="utf-8") as f:
        f.write(compressed_data_summary)
    print(f"🗂️ Combined compressed input saved to {compressed_log}")

    # Save compressed output for review
    compressed_log = os.path.join(compressed_data_dir, "compressed_input.txt")
    with open(compressed_log, "w", encoding="utf-8") as f:
        f.write(compressed_data_summary)
    print(f"🗂️ Compressed input saved to {compressed_log}")

    # Step 4: Run the rest of the Agents.
    analyst_summary = run_agent(
        "🤖 Analyst Agent",
        analyst_system_prompt,
        analyst_instruction,
        compressed_data_summary,
        model_name="qwen2.5",  # ✅ Faster, leaner model
        temperature=0.1,
        debug_message="DEBUG: Sample analyst summary."
    )

    oracle_dynamic_input = (
        f"Hexagram #{number}: {name}\nMeaning: {meaning}\n\n"
        f"Analyst Summary:\n{analyst_summary}"
    )

    if gematria_outputs:
        oracle_dynamic_input += "\n\n✡ GEMATRIA REVELATIONS ✡\n"
        for result in gematria_outputs:
            oracle_dynamic_input += f"\n── Value {result['value']} ──\n"
            oracle_dynamic_input += result['message'].strip() + "\n"

    oracle_message = run_agent(
        "🧙 Oracle Agent",
        oracle_system_prompt,
        oracle_instruction,
        oracle_dynamic_input,
        model_name="qwen2.5",  # ✅ Creative, rich model
        temperature=0.5,
        debug_message="DEBUG: Sample Oracle Message."
    )

    advisor_dynamic_input = (
        f"[ANALYST SUMMARY]\n{analyst_summary}\n\n"
        f"[ORACLE PROPHECY]\n{oracle_message}"
    )

    advisor_recommendation = run_agent(
        "🧭 Advisor Agent",
        advisor_system_prompt,
        advisor_instruction,
        advisor_dynamic_input,
        model_name="qwen2.5",  # ✅ Authoritative output
        debug_message="DEBUG: Sample Advisor Recommendation."
    )
    # Format, archive, and print
    formatted_output = format_printout(number, name, meaning, hexagram_text, analyst_summary, oracle_message, advisor_recommendation, gematria_outputs=gematria_outputs)
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
