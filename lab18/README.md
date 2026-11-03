# FIN439 Lab 18 — Legend Investor as Skill

This project uses SEC EDGAR 10-K company facts. Python calculates all financial figures and Buffett checks. Codex writes the qualitative memo. No API key or paid financial data source is required.

## Setup in VS Code terminal

```bash
cd FIN43900/lab18
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export SEC_CONTACT_EMAIL="your.email@example.com"
python warren-buffett-sec/scripts/sec_analysis.py COST
streamlit run app.py
```

To rerun the validation tests after setup:

```bash
python -m unittest -v test_lab18.py
python -m unittest -v test_live_sec.py
```

Use your real email for `SEC_CONTACT_EMAIL`; the SEC requests an identifying User-Agent. Do not commit it. Enter any ticker in the app, then click **Generate AI memo with Codex**. Codex CLI must be installed and signed in. The memo is saved in `memos/TICKER.md`, where you can edit the trust line. If you prefer, ask Codex in VS Code: `Use $warren-buffett-sec to analyze COST and save the memo.`

The repository copy of the skill is `warren-buffett-sec/`. To install it for Codex discovery, copy that folder into `~/.codex/skills/`. The app uses the repository copy of the Python script, so GitHub has every project file. Restart Codex after installing the skill.

The dashboard reads only the script's printed financial results and flags numbers in a memo that are absent from that output. It is a learning demonstration, not investment advice. The simplified owner earnings measure subtracts all capital spending, since the SEC facts do not separate maintenance spending.
