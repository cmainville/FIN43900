"""Lab 15 engine, data, and app checks. Run python3 -m unittest lab15.test_lab15."""
import io
import math
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import pandas as pd

from lab15 import portfolio as p

ROOT = Path(__file__).resolve().parent.parent
DATA = Path(__file__).with_name("prices_growth.csv")


class Lab15Tests(unittest.TestCase):
    def solve_meridian(self, returns=None, correlations=None):
        return p.optimize_portfolio(p.ASSETS, returns or p.EXPECTED_RETURNS,
                                    p.VOLATILITIES, correlations or p.CORRELATIONS,
                                    .065, p.RESERVE_ELIGIBLE, .03)

    def test_cli_regression(self):
        root = subprocess.check_output([sys.executable, str(ROOT / "portfolio.py")])
        copy = subprocess.check_output([sys.executable, str(ROOT / "lab15/portfolio.py")])
        self.assertEqual(root, copy)

    def test_import_path(self):
        self.assertEqual(Path(p.__file__).resolve(), ROOT / "lab15/portfolio.py")

    def test_meridian_cases(self):
        original = self.solve_meridian()
        self.assertEqual(original["weights"], (0, .2, .25, .55))
        self.assertEqual((round(original["return"]*100, 2), round(original["volatility"]*100, 2)), (6.51, 9.44))
        returns = list(p.EXPECTED_RETURNS); returns[3] = .07
        shock = self.solve_meridian(returns=returns)
        self.assertEqual(shock["weights"], (0, .1, .1, .8))
        self.assertEqual((round(shock["return"]*100, 2), round(shock["volatility"]*100, 2)), (6.53, 12.94))
        self.assertEqual(p.largest_weight_change(original, shock), 25)
        corr = [list(row) for row in p.CORRELATIONS]
        corr[2][3] = corr[3][2] = .5
        stressed = self.solve_meridian(correlations=corr)
        self.assertEqual(stressed["weights"], (0, .4, 0, .6))
        self.assertEqual((round(stressed["return"]*100, 2), round(stressed["volatility"]*100, 2)), (6.52, 9.73))
        self.assertEqual(p.CORRELATIONS[2][3], .25)
        self.assertEqual(p.CORRELATIONS[3][2], .25)

    def test_correlation_rejection(self):
        corr = [list(row) for row in p.CORRELATIONS]
        corr[2][3] = .5
        with self.assertRaisesRegex(ValueError, "symmetric"):
            self.solve_meridian(correlations=corr)
        corr[2][3] = corr[3][2] = 1.3
        with self.assertRaisesRegex(ValueError, "within"):
            self.solve_meridian(correlations=corr)

    def test_exhaustive_grid_constraints(self):
        units = list(p.allocation_units(5))
        self.assertEqual(len(units), 10626)
        self.assertEqual(len(set(units)), 10626)
        self.assertTrue(all(sum(row) == 20 and min(row) >= 0 for row in units))
        result = self.solve_meridian()
        self.assertEqual(result["candidate_count"], 1771)
        self.assertAlmostEqual(sum(result["weights"]), 1)
        self.assertTrue(all(w >= 0 and round(w * 20) == w * 20 for w in result["weights"]))
        self.assertGreaterEqual(result["return"], .065)
        self.assertGreaterEqual(result["reserve"], .03)
        self.assertFalse(self.solve_meridian(returns=(.01, .01, .01, .01))["feasible"])
        no_reserve = p.optimize_portfolio(p.ASSETS, p.EXPECTED_RETURNS,
                                           p.VOLATILITIES, p.CORRELATIONS, .065, (), 0)
        self.assertEqual(no_reserve["reserve"], 0)

    def test_arbitrary_universe_and_reserve_rule(self):
        corr3 = ((1, 0, 0), (0, 1, 0), (0, 0, 1))
        three = p.optimize_portfolio(("A", "B", "C"), (.04, .07, .08),
                                     (.01, .1, .2), corr3, .06, ("B",), .25)
        self.assertEqual(three["candidate_count"], 231)
        self.assertGreaterEqual(three["reserve"], .25)
        self.assertGreaterEqual(three["return"], .06)
        impossible = p.optimize_portfolio(("A", "B", "C"), (.04, .07, .08),
                                          (.01, .1, .2), corr3, .08, ("A",), .05)
        self.assertFalse(impossible["feasible"])
        six = p.optimize_portfolio(tuple("ABCDEF"), (.1,)*6, (.1,)*6,
                                   tuple(tuple(1 if i == j else 0 for j in range(6)) for i in range(6)),
                                   .06)
        self.assertEqual(six["candidate_count"], 53130)

    def fixture(self, dates=None, prices=None):
        dates = dates if dates is not None else pd.date_range("2020-01-31", periods=38, freq="ME")
        prices = prices if prices is not None else {"A": [100*(1.01)**i for i in range(len(dates))],
                            "B": [100*(1.02)**i for i in range(len(dates))],
                            "C": [100*(1.005)**i for i in range(len(dates))]}
        frame = pd.DataFrame({"Date": dates.strftime("%Y-%m-%d"), **prices})
        return io.StringIO(frame.to_csv(index=False))

    def test_price_estimator_windows_and_upload(self):
        full = p.estimate_from_monthly_prices(self.fixture())
        short = p.estimate_from_monthly_prices(self.fixture(), True)
        self.assertEqual(full["observation_count"], 37)
        self.assertEqual(short["observation_count"], 36)
        self.assertAlmostEqual(full["expected_returns"][0], .12)
        self.assertAlmostEqual(full["correlations"][0][0], 1)

    def test_sample_volatility_and_covariance(self):
        dates = pd.date_range("2020-01-31", periods=5, freq="ME")
        source = self.fixture(dates, {"A": [100, 110, 110, 121, 121],
                                      "B": [100, 100, 110, 110, 121],
                                      "C": [100, 105, 115, 130, 145]})
        e = p.estimate_from_monthly_prices(source)
        returns = pd.Series([.1, 0, .1, 0])
        self.assertAlmostEqual(e["volatilities"][0], returns.std(ddof=1)*math.sqrt(12))
        cov = p.covariance_matrix(e["volatilities"], e["correlations"])
        self.assertAlmostEqual(cov[0][1], e["volatilities"][0]*e["volatilities"][1]*e["correlations"][0][1])

    def test_bad_csv(self):
        base = pd.read_csv(self.fixture())
        for altered in (base.iloc[::-1], pd.concat([base, base.tail(1)]),
                        base.assign(A=0), base.assign(A=float("nan"))):
            with self.subTest(case=str(altered.head(1))):
                with self.assertRaises(ValueError):
                    p.estimate_from_monthly_prices(io.StringIO(altered.to_csv(index=False)))

    @unittest.skipUnless(DATA.exists(), "Real price data unavailable")
    def test_real_prices_and_scenarios(self):
        frame = pd.read_csv(DATA)
        self.assertEqual(list(frame.columns), ["Date", "VTI", "VXUS", "XLE", "IWM", "IAU"])
        self.assertEqual(len(frame), 60)
        self.assertEqual((frame.Date.iloc[0], frame.Date.iloc[-1]), ("2021-10-31", "2026-09-30"))
        full = p.estimate_from_monthly_prices(DATA)
        short = p.estimate_from_monthly_prices(DATA, True)
        self.assertEqual((full["observation_count"], short["observation_count"]), (59, 36))
        def optimize(est, objective=.06):
            return p.optimize_portfolio(est["assets"], est["expected_returns"],
                                        est["volatilities"], est["correlations"], objective)
        base = optimize(full)
        recent = optimize(short)
        self.assertTrue(base["feasible"] and recent["feasible"])
        self.assertEqual(base["candidate_count"], 10626)
        self.assertEqual(p.largest_weight_change(base, recent), 25)
        weights = (.45, .25, .1, .1, .1)
        self.assertGreater(p.expected_portfolio_return(weights, full["expected_returns"]), .06)
        covariance = p.covariance_matrix(full["volatilities"], full["correlations"])
        self.assertGreater(p.portfolio_variance_and_volatility(weights, covariance)[1], 0)
        for index in (0, 2, 4):
            edited = list(full["expected_returns"]); edited[index] -= .01
            shock = p.optimize_portfolio(full["assets"], edited, full["volatilities"],
                                         full["correlations"], .06)
            self.assertTrue(shock["feasible"])
            self.assertIsNotNone(p.largest_weight_change(base, shock))
        self.assertTrue(optimize(full, .07)["feasible"])
        self.assertFalse(optimize(full, 1.0)["feasible"])

    def test_streamlit_apptest(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(ROOT / "lab15/app.py"), default_timeout=30).run()
        self.assertEqual(len(app.exception), 0, [str(x) for x in app.exception])
        self.assertTrue(any("Portfolio Stability Dashboard" in x.value for x in app.title))
        self.assertIn('"Global equity index fund": "55%"', app.json[1].value)
        app.number_input[3].set_value(7.0).run()
        self.assertIn('"Global equity index fund": "55%"', app.json[0].value)
        self.assertIn('"Global equity index fund": "80%"', app.json[1].value)
        app.number_input[-2].set_value(100.0).run()
        self.assertTrue(any("no mix meets the objective" in x.value for x in app.error))
        app.radio[0].set_value("Long-Term Growth Portfolio").run()
        self.assertEqual(len(app.exception), 0)
        self.assertEqual(app.number_input[-2].value, 6.0)
        app.toggle[0].set_value(True).run()
        self.assertIn('"VXUS": "20%"', app.json[1].value)

    def test_engine_source_edit_apptest(self):
        from streamlit.testing.v1 import AppTest
        path = ROOT / "lab15/portfolio.py"
        original = path.read_text()
        def displayed():
            app = AppTest.from_file(str(ROOT / "lab15/app.py"), default_timeout=30).run()
            self.assertEqual(len(app.exception), 0)
            return app.json[1].value
        try:
            self.assertIn('"Investment-grade bond fund": "25%"', displayed())
            stressed = original.replace('(0.05, 0.80, 1.00, 0.25),',
                                        '(0.05, 0.80, 1.00, 0.50),').replace(
                                        '(0.00, -0.10, 0.25, 1.00),',
                                        '(0.00, -0.10, 0.50, 1.00),')
            self.assertNotEqual(stressed, original)
            path.write_text(stressed)
            self.assertIn('"Treasury 10-year note": "40%"', displayed())
        finally:
            path.write_text(original)
        self.assertIn('"Investment-grade bond fund": "25%"', displayed())


if __name__ == "__main__":
    unittest.main(verbosity=2)
