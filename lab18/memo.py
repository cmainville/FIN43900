"""Codex memo generation and numeric grounding check."""

import re
import subprocess
import tempfile
from decimal import Decimal
from pathlib import Path


NUMBER = re.compile(r"(?<![A-Za-z0-9])\$?-?\d[\d,]*(?:\.\d+)?%?(?![A-Za-z0-9])")


def number_key(token):
    return Decimal(token.replace("$", "").replace(",", "").replace("%", "")), token.endswith("%")


def unsupported_numbers(memo_text, printed_text):
    allowed = {number_key(match.group()) for match in NUMBER.finditer(printed_text)}
    return sorted({match.group() for match in NUMBER.finditer(memo_text)
                   if number_key(match.group()) not in allowed})


def generate_memo(ticker, printed_text, project_dir):
    prompt = f"""Write a short Warren Buffett-style investment memo as a clearly labeled simulation for {ticker}.
Use only the financial numbers in the Python output below. Choose Own, Watch, or Pass.
Discuss business quality, possible moat, profitability, cash generation, consistency, and uncertainty.
Do not assert facts about management or a moat that these figures cannot establish.
Do not discuss stock prices, valuation, intrinsic value, or margin of safety.
Explicitly acknowledge missing figures. Do not calculate any new numbers.
Use Markdown. End with exactly: My trust in this verdict: ____ because ____
Output only the memo text. Do not use tools.

PYTHON OUTPUT:
{printed_text}
"""
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / "memo.md"
        command = ["codex", "exec", "--ephemeral", "--skip-git-repo-check", "-s", "read-only",
                   "-C", str(project_dir), "-o", str(output), "-"]
        completed = subprocess.run(command, input=prompt, text=True, capture_output=True, timeout=180)
        if completed.returncode != 0 or not output.exists():
            raise RuntimeError((completed.stderr or completed.stdout or "Codex memo generation failed.")[-1000:])
        return output.read_text().strip() + "\n"
