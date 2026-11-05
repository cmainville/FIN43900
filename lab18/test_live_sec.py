"""Run with SEC_CONTACT_EMAIL set; these tests fetch live SEC EDGAR data."""

import importlib.util
import os
import unittest
from pathlib import Path

from memo import unsupported_numbers


ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("sec_analysis", ROOT / "warren-buffett-sec" / "scripts" / "sec_analysis.py")
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)


class LiveSECTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not os.environ.get("SEC_CONTACT_EMAIL"):
            raise RuntimeError("Set SEC_CONTACT_EMAIL before running live SEC tests.")
        cls.cost = sec.analyze("COST")
        cls.jpm = sec.analyze("JPM")
        cls.nvda = sec.analyze("NVDA")

    def test_costco_professor_benchmarks(self):
        expected = [
            ("2022-08-28", 226954, 5844, 7392, 3891, 20642, 28.3, 3501),
            ("2023-09-03", 242290, 6292, 11068, 4323, 25058, 25.1, 6745),
            ("2024-09-01", 254453, 7367, 11339, 4710, 23622, 31.2, 6629),
            ("2025-08-31", 275235, 8099, 13335, 5498, 29164, 27.8, 7837),
            ("2026-08-30", 303154, 9226, 15817, 6435, 35803, 25.8, 9382),
        ]
        self.assertEqual(len(self.cost["rows"]), 5)
        metrics = ("revenue", "net_income", "operating_cash_flow", "capital_spending", "stockholders_equity", "roe", "owner_earnings")
        for row, benchmark in zip(self.cost["rows"], expected):
            self.assertEqual(row["fiscal_year_end"], benchmark[0])
            for metric, value in zip(metrics, benchmark[1:]):
                actual = row["values"][metric]
                self.assertEqual(round(actual, 1) if metric == "roe" else actual / 1_000_000, value, metric)
        self.assertEqual([self.cost["checks"][name] for name in sec.INVESTOR_CHECKS["Warren Buffett"]], ["Pass", "Pass", "Pass"])
        memo = (ROOT / "memos" / "COST.md").read_text()
        self.assertEqual(unsupported_numbers(memo, sec.printed_results(self.cost)), [])

    def test_jpm_missing_capex(self):
        self.assertEqual(len(self.jpm["rows"]), 5)
        self.assertTrue(all(row["values"]["capital_spending"] is None for row in self.jpm["rows"]))
        self.assertTrue(all(row["values"]["owner_earnings"] is None for row in self.jpm["rows"]))
        self.assertEqual([self.jpm["checks"][name] for name in sec.INVESTOR_CHECKS["Warren Buffett"][1:]], ["Not Known", "Not Known"])
        memo = (ROOT / "memos" / "JPM.md").read_text()
        self.assertIn("Owner earnings therefore cannot be evaluated", memo)
        self.assertEqual(unsupported_numbers(memo, sec.printed_results(self.jpm)), [])

    def test_vti_largest_holding_panel(self):
        self.assertEqual(self.nvda["ticker"], "NVDA")
        self.assertEqual(self.nvda["verdicts"], {"Warren Buffett": "Pass", "Cathie Wood": "Pass", "Michael Burry": "Fail"})
        self.assertEqual(len(self.nvda["checks"]), 7)

    def test_dashboard_flags_injected_roe(self):
        from streamlit.testing.v1 import AppTest

        path = ROOT / "memos" / "COST.md"
        original = path.read_text()
        try:
            path.write_text(original + "\nUnsupported ROE: 40.0%.\n")
            app = AppTest.from_file(str(ROOT / "app.py"), default_timeout=30).run()
            self.assertFalse(app.exception)
            self.assertTrue(any("40.0%" in item.value for item in app.error))
        finally:
            path.write_text(original)


if __name__ == "__main__":
    unittest.main()
