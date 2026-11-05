"""Deterministic Lab 19 checks against dated SEC company-fact extracts."""
import importlib.util
import unittest
from pathlib import Path

from memo import panel_memo, unsupported_numbers

ROOT = Path(__file__).parent
spec = importlib.util.spec_from_file_location("sec_analysis", ROOT / "warren-buffett-sec/scripts/sec_analysis.py")
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)


class Lab19Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cost = sec.analyze_snapshot("COST")
        cls.nvda = sec.analyze_snapshot("NVDA")

    def test_costco_benchmarks(self):
        c = self.cost
        self.assertEqual([r["fiscal_year_end"][:4] for r in c["rows"]], ["2022", "2023", "2024", "2025", "2026"])
        self.assertEqual(list(c["checks"].values()), ["Pass", "Pass", "Pass", "Fail", "Not Known", "Pass", "Pass"])
        self.assertEqual(c["details"]["Revenue CAGR >= 15%"], "7.51%")
        self.assertEqual(c["details"]["Latest liabilities / equity <= 2"], "1.49x")
        self.assertEqual([f'{r["values"]["liabilities_equity_ratio"]:.2f}' for r in c["rows"]], ["2.11", "1.75", "1.96", "1.64", "1.49"])
        self.assertEqual(c["verdicts"], {"Warren Buffett": "Pass", "Cathie Wood": "Fail", "Michael Burry": "Pass"})

    def test_threshold_experiment_restores_default(self):
        original = self.cost["checks"]["Revenue CAGR >= 15%"]
        at_five, _ = sec.cathie_checks(self.cost["rows"], growth_threshold=0.05)
        self.assertEqual(at_five["Revenue CAGR >= 15%"], "Pass")
        self.assertEqual(at_five["Latest R&D / revenue >= 5%"], "Not Known")
        self.assertEqual(original, "Fail")

    def test_missing_inputs_and_verdict_precedence(self):
        rows = [{"values": {"revenue": None, "research_and_development": None}} for _ in range(5)]
        statuses, ratios = sec.cathie_checks(rows)
        self.assertEqual(list(statuses.values()), ["Not Known", "Not Known"])
        self.assertIsNone(ratios["revenue_cagr"])
        self.assertEqual(sec.verdict(["Pass", "Not Known"]), "Not Known")
        self.assertEqual(sec.verdict(["Fail", "Not Known"]), "Fail")

    def test_nvda_panel_and_all_memos_grounded(self):
        self.assertEqual(self.nvda["verdicts"], {"Warren Buffett": "Pass", "Cathie Wood": "Pass", "Michael Burry": "Fail"})
        for result in (self.cost, self.nvda):
            printed = sec.printed_results(result)
            for investor in sec.INVESTOR_CHECKS:
                self.assertEqual(unsupported_numbers(panel_memo(result, investor), printed), [])
                self.assertEqual(unsupported_numbers(panel_memo(result, investor) + " Unsupported ROE 40.0%.", printed), ["40.0%"])


if __name__ == "__main__":
    unittest.main()
