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


def generate_memo(ticker, printed_text, project_dir, investor="Warren Buffett"):
    prompt = f"""Write a short {investor}-style investment memo as a clearly labeled simulation for {ticker}.
Use only the financial numbers in the Python output below. Choose Own, Watch, or Pass.
Use {investor}'s distinct lens: Buffett favors durable returns and owner earnings; Wood favors revenue growth and R&D commitment; Burry favors cash conversion and balance-sheet resilience.
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


def panel_memo(result, investor):
    """A grounded memo that works without the optional Codex CLI."""
    names = {
        "Warren Buffett": ("I focus on repeatable returns and cash owners could receive.", "ROE >= 15% in all five years", "Positive owner earnings in all five years", "Owner earnings increased first to last"),
        "Cathie Wood": ("I focus on sustained growth and reinvestment in research.", "Revenue CAGR >= 15%", "Latest R&D / revenue >= 5%"),
        "Michael Burry": ("I focus on cash backing earnings and balance-sheet risk.", "Operating cash flow >= net income in all five years", "Latest liabilities / equity <= 2"),
    }
    intro, *checks = names[investor]
    lines = [f"### {investor} — {result['verdicts'][investor]}", intro]
    for name in checks:
        lines.append(f"- {name}: {result['details'][name]} — {result['checks'][name]}.")
    if result["verdicts"][investor] == "Pass":
        lines.append("The financial screen passes; business quality and valuation still need separate review.")
    elif result["verdicts"][investor] == "Fail":
        lines.append("A measured criterion fails, so I would investigate the cause before considering the company.")
    else:
        lines.append("The available facts do not support a complete verdict; missing inputs remain not known.")
    return "\n\n".join(lines)
