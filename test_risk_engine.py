import unittest
from services.risk_engine import ProcurementRiskEngine

class TestProcurementRiskEngine(unittest.TestCase):

    def test_low_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(500, 600, 5, 7, 95, 95, 90)
        self.assertEqual(res['risk_level'], 'LOW')
        self.assertEqual(res['risk_score'], 0)
        self.assertEqual(len(res['risks']), 0)

    def test_budget_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(700, 600, 5, 7, 95, 95, 90)
        self.assertEqual(res['risk_score'], 20)
        self.assertEqual(res['risk_level'], 'LOW')
        self.assertTrue(any("Price exceeds budget" in r for r in res['risks']))

    def test_delivery_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(500, 600, 10, 7, 95, 95, 90)
        self.assertEqual(res['risk_score'], 20)
        self.assertTrue(any("Delivery exceeds requirement" in r for r in res['risks']))

    def test_reliability_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(500, 600, 5, 7, 75, 95, 90)
        self.assertEqual(res['risk_score'], 20)
        self.assertTrue(any("Reliability" in r for r in res['risks']))

    def test_accuracy_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(500, 600, 5, 7, 95, 85, 90)
        self.assertEqual(res['risk_score'], 20)
        self.assertTrue(any("accuracy" in r for r in res['risks']))

    def test_rating_risk(self):
        res = ProcurementRiskEngine.evaluate_risk(500, 600, 5, 7, 95, 95, 70)
        self.assertEqual(res['risk_score'], 20)
        self.assertTrue(any("Overall rating" in r for r in res['risks']))

    def test_multiple_risks_critical(self):
        # Trigger all 5 risks -> score 100 (CRITICAL)
        res = ProcurementRiskEngine.evaluate_risk(700, 600, 10, 7, 70, 70, 70)
        self.assertEqual(res['risk_score'], 100)
        self.assertEqual(res['risk_level'], 'CRITICAL')
        self.assertEqual(len(res['risks']), 5)

if __name__ == '__main__':
    unittest.main()
