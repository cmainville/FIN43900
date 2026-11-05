"""Focused behavior checks; live SEC comparisons are run separately."""

import importlib.util
import io
import json
import os
import unittest
from pathlib import Path
from unittest.mock import patch

from memo import unsupported_numbers


SCRIPT = Path(__file__).parent / "warren-buffett-sec" / "scripts" / "sec_analysis.py"
spec = importlib.util.spec_from_file_location("sec_analysis", SCRIPT)
sec = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sec)


class Lab18Tests(unittest.TestCase):
    def test_latest_10k_and_full_year_only(self):
        facts = {"facts": {"us-gaap": {"NetIncomeLoss": {"units": {"USD": [
            {"form": "10-K", "start": "2024-09-02", "end": "2025-08-31", "filed": "2025-10-01", "val": 100},
            {"form": "10-K", "start": "2024-09-02", "end": "2025-08-31", "filed": "2026-10-01", "val": 110},
            {"form": "10-Q", "start": "2024-09-02", "end": "2025-08-31", "filed": "2026-10-02", "val": 999},
            {"form": "10-K", "start": "2025-06-01", "end": "2025-08-31", "filed": "2026-10-03", "val": 888},
        ]}}}}}
        self.assertEqual(sec.pick(facts, ("NetIncomeLoss",), "2025-08-31", True)[0], 110)

    def test_missing_owner_earnings_checks(self):
        self.assertEqual(sec.check([None] * 5, lambda values: all(v > 0 for v in values)), "Not Known")
        self.assertEqual(sec.check([1, 2, 3, 4, 5], lambda values: values[-1] > values[0]), "Pass")

    def test_unsupported_costco_roe(self):
        printed = "ROE: 28.3%\nROE >= 15% in all five years: Pass"
        self.assertEqual(unsupported_numbers("Reported ROE was 40.0%.", printed), ["40.0%"])

    def test_streamlit_renders_with_sec_shaped_data(self):
        from streamlit.testing.v1 import AppTest

        gaap = {}
        for tag, value in (("RevenueFromContractWithCustomerExcludingAssessedTax", 100),
                           ("NetIncomeLoss", 10),
                           ("NetCashProvidedByUsedInOperatingActivities", 15),
                           ("PaymentsToAcquirePropertyPlantAndEquipment", 5),
                           ("StockholdersEquity", 50)):
            gaap[tag] = {"units": {"USD": []}}
            for year in range(2021, 2026):
                fact = {"form": "10-K", "end": f"{year}-12-31", "filed": f"{year + 1}-02-01", "val": value * 1_000_000}
                if tag != "StockholdersEquity":
                    fact["start"] = f"{year}-01-01"
                gaap[tag]["units"]["USD"].append(fact)
        companies = {"0": {"ticker": "COST", "cik_str": 1, "title": "Example Company"}}
        facts = {"cik": 1, "facts": {"us-gaap": gaap}}

        def fake_urlopen(request, timeout, context):
            payload = facts if "companyfacts" in request.full_url else companies
            return io.BytesIO(json.dumps(payload).encode())

        with patch.dict(os.environ, {"SEC_CONTACT_EMAIL": "test@example.com"}), patch("urllib.request.urlopen", fake_urlopen):
            app = AppTest.from_file(str(Path(__file__).parent / "app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.get("vega_lite_chart")), 1)
        self.assertEqual(len(app.get("dataframe")), 2)


if __name__ == "__main__":
    unittest.main()
