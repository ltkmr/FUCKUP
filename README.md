# FUCKUP² — First Universal Cybernetic-Kinetic-Ultramicro-Programmer
An automated cyber-occult oracle machine inspired by Robert Anton Wilson's Illuminatus! trilogy.

## 📜 Project Overview
FUCKUP² is an automated, self-operating oracle system:

📊 Pulls daily world data

🧙 Throws the I-Ging hexagram (with authentic Unicode representation)

🧩 Passes data through a chain of AI agents:

   - Compression Stage: Compression of incomming RSS feeds

   - Analyst Agent: Processes daily data

   - Oracle Agent: Interprets divination + data cryptically

   - Advisor Agent: Suggests action (enigmatic, of course!)

🖨️ Prints the daily prophecy (lp)

🗃️ Archives each reading

🌐 Automatically updates a web archive for browsing prophecies

The system runs fully automated, daily, via cron.

## ⚙️ System Architecture

```
[ Daily Data Sources ]
          │
          ▼
[ Compression Stage ] — Compresses incomming feeds to avoid congesting the Analyst's attenion window.
          │
          ▼
[ Analyst Agent ] — Summarizes data
          │
          ▼
[ Oracle Agent ] — Applies I-Ching & mysticism
          │
          ▼
[ Advisor Agent ] — Gives action recommendation
          │
          ├── 🖨️ Print Prophecy
          ├── 🗃️ Archive Prophecy
          └── 🌐 Update Web Archive (static HTML)
```

## Technologies:

🐍 Python 3

🖨️ Printer via lp

✍️ Static HTML + CSS archive

🧠 Local LLM (Gemma 3, Mistral, or others)

🗓️ Scheduled via cron

## 🚀 Installation
Clone the repository, create and activate Python virtual environment:

```
python3 -m venv venv
source venv/bin/activate
```
Install requirements:

```
pip install -r requirements.txt
```

Set up cronjob (optional, for daily automation):

```
crontab -e
# Add:
0 7 * * * /path/to/venv/bin/python /path/to/fuckup2/oracle/daily_runner.py >> /path/to/fuckup2/oracle/cron.log 2>&1
```

## 🧩 Usage
To manually run the oracle:
```
source venv/bin/activate
python oracle/daily_runner.py
```


To regenerate the web archive:
```
python oracle/generate_html.py
Archives are stored in /archive/.
Web pages are generated in /web/.
```
## 📂 Project Structure
```
fuckup2/
├── oracle/
│   ├── daily_runner.py       # Main oracle script
│   ├── generate_html.py      # Static HTML generator
│   └── iching.py             # I-Ching logic
├── archive/                  # Text archive of prophecies
├── web/                      # Web archive (static HTML)
│   └── style.css             # Styling for the web archive
├── venv/                     # Virtual environment (Python)
└── README.md                 # This document
```
## 🚀 Roadmap
 ✅ Automated daily oracle runs

 ✅ Archive per run (timestamped)

 ✅ Unicode hexagram support in archives

 ✅ Web archive generation

 🗂️ Monthly trend analysis ("Book of the Month")

 🧙‍♂️ Multi-agent logging for deeper analysis

 🖲️ Manual invocation button for public use

 📡 Optional remote data sources and backups

 🎨 Web archive styling improvements

 ## 🖲️ Hints:
 Most small LLMs come with too small num_ctx parameters. Create a modelfile with enough space: 
```
 FROM [Your prefered LLM]
# Parameters
PARAMETER temperature 0.8
PARAMETER top_p 0.7
PARAMETER top_k 30
PARAMETER num_ctx 7680
PARAMETER num_predict 5632
```
Give it some space. Create a new Ollama network with:
```
ollama create [Name of new network] -f [name of modelfile]
```




📝 License:

All rights wronged.

👤 Author
jl



