"""Executable Lab 14 checks A through F (standard-library unittest)."""

import contextlib
import io
import unittest

import mandate
import portfolio


EXPECTED = {
    "Benchmark": ((0.0, 0.0, 40.0, 60.0), 6.80, 10.46, 0.0, True),
    "Equal Weight": ((25.0, 25.0, 25.0, 25.0), 5.20, 5.21, 50.0, False),
    "Inverse Volatility": ((84.3, 6.0, 7.0, 2.6), 3.77, 1.05, 90.3, False),
}


class PortfolioLabTests(unittest.TestCase):
    def assert_known_answers(self):
        results = portfolio.baseline_portfolios()
        for name, (weights, ret, vol, reserve, status) in EXPECTED.items():
            with self.subTest(portfolio=name):
                actual = results[name]
                self.assertEqual(tuple(round(w * 100, 1) for w in actual["weights"]), weights)
                self.assertEqual(round(actual["return"] * 100, 2), ret)
                self.assertEqual(round(actual["volatility"] * 100, 2), vol)
                self.assertEqual(round(actual["reserve"] * 100, 1), reserve)
                self.assertEqual(actual["objective_pass"], status)

    def test_a_known_answers_and_display(self):
        self.assert_known_answers()
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            portfolio.display_portfolio_comparison(portfolio.baseline_portfolios())
        text = output.getvalue()
        self.assertIn("CPI estimate: 2.5%; objective: CPI + 4.0% = 6.5%", text)
        for value in ("6.80%", "10.46%", "5.20%", "5.21%", "3.77%", "1.05%", "90.3%"):
            self.assertIn(value, text)

    def test_b_correlation_sensitivity(self):
        correlations = [list(row) for row in portfolio.CORRELATIONS]
        correlations[2][3] = correlations[3][2] = 0.50
        modified = portfolio.baseline_portfolios(correlations=correlations)["Benchmark"]
        self.assertEqual(round(modified["volatility"] * 100, 2), 11.00)
        self.assertEqual(portfolio.CORRELATIONS[2][3], 0.25)
        self.assertEqual(portfolio.CORRELATIONS[3][2], 0.25)

    def test_c_invalid_correlation(self):
        correlations = [list(row) for row in portfolio.CORRELATIONS]
        correlations[2][3] = correlations[3][2] = 1.3
        with self.assertRaisesRegex(ValueError, r"Correlation.*\[-1, 1\]"):
            portfolio.baseline_portfolios(correlations=correlations)
        self.assertEqual(portfolio.CORRELATIONS[2][3], 0.25)

    def test_d_asymmetric_matrix(self):
        correlations = [list(row) for row in portfolio.CORRELATIONS]
        correlations[2][3] = 0.50
        with self.assertRaisesRegex(ValueError, "symmetric"):
            portfolio.baseline_portfolios(correlations=correlations)

    def test_e_dynamic_calculations(self):
        returns = list(portfolio.EXPECTED_RETURNS)
        returns[3] += 0.01
        changed_return = portfolio.baseline_portfolios(expected_returns=returns)["Benchmark"]
        original = portfolio.baseline_portfolios()["Benchmark"]
        self.assertAlmostEqual(changed_return["return"] - original["return"], 0.006)
        volatilities = list(portfolio.VOLATILITIES)
        volatilities[3] *= 1.10
        changed_vol = portfolio.baseline_portfolios(volatilities=volatilities)
        self.assertGreater(changed_vol["Benchmark"]["volatility"], original["volatility"])
        self.assertNotEqual(changed_vol["Inverse Volatility"]["weights"],
                            portfolio.baseline_portfolios()["Inverse Volatility"]["weights"])
        self.assertEqual(portfolio.EXPECTED_RETURNS[3], 0.080)
        self.assertEqual(portfolio.VOLATILITIES[3], 0.160)

    def test_f_regression_and_mandate(self):
        self.assert_known_answers()
        expected_failures = {"A": 0, "B": 3, "C": 1, "D": 0,
                             "E — Meridian Benchmark": 1}
        for name, failures in expected_failures.items():
            with self.subTest(candidate=name):
                result = mandate.assess_portfolio(mandate.CANDIDATES[name])
                self.assertEqual(result["failed_rules"], failures)
        candidate_e = mandate.assess_portfolio(mandate.CANDIDATES["E — Meridian Benchmark"])
        self.assertEqual(candidate_e["reserve_weight"], 0.0)
        self.assertFalse(candidate_e["reserve_pass"])
        self.assertTrue(candidate_e["liquidity_pass"])


if __name__ == "__main__":
    unittest.main(verbosity=2)
