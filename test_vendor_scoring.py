import unittest
from services.vendor_scoring import VendorScoringEngine

class TestVendorScoring(unittest.TestCase):
    def setUp(self):
        self.vendor_profiles = [
            {'id': 1, 'name': 'Cheapest Vendor', 'reliability': 90, 'accuracy': 90, 'rating': 90},
            {'id': 2, 'name': 'Fastest Vendor', 'reliability': 90, 'accuracy': 90, 'rating': 90},
            {'id': 3, 'name': 'Unreliable Vendor', 'reliability': 40, 'accuracy': 50, 'rating': 50},
            {'id': 4, 'name': 'Late Vendor', 'reliability': 90, 'accuracy': 90, 'rating': 90},
            {'id': 5, 'name': 'Over-budget Vendor', 'reliability': 95, 'accuracy': 95, 'rating': 95},
        ]
        
        self.bids = [
            {'vendor_id': 1, 'price_per_unit': 100, 'delivery_days': 7}, # Cheapest
            {'vendor_id': 2, 'price_per_unit': 120, 'delivery_days': 3}, # Fastest
            {'vendor_id': 3, 'price_per_unit': 110, 'delivery_days': 7}, # Unreliable
            {'vendor_id': 4, 'price_per_unit': 110, 'delivery_days': 12}, # Late (5 days late)
            {'vendor_id': 5, 'price_per_unit': 200, 'delivery_days': 7}, # Over-budget
        ]
        
        self.requested_delivery = 7
        self.budget = 150

    def test_scoring_engine(self):
        results = VendorScoringEngine.score_vendors(self.bids, self.vendor_profiles, self.requested_delivery, self.budget)
        
        # Helper to get result by vendor name
        def get_result(name):
            return next(r for r in results if r['vendor_name'] == name)
            
        cheapest = get_result('Cheapest Vendor')
        fastest = get_result('Fastest Vendor')
        unreliable = get_result('Unreliable Vendor')
        late = get_result('Late Vendor')
        over_budget = get_result('Over-budget Vendor')
        
        print("\n--- Scoring Results ---")
        for r in results:
            print(f"{r['vendor_name']}: {r['final_score']} (Price: {r['price_score']}, Delivery: {r['delivery_score']})")

        # Cheapest vendor should have 100 price score
        self.assertEqual(cheapest['price_score'], 100.0)
        
        # Fastest vendor should have 100 delivery score (within deadline)
        self.assertEqual(fastest['delivery_score'], 100.0)
        
        # Unreliable vendor should have lower reliability score in final output
        self.assertEqual(unreliable['reliability_score'], 40.0)
        
        # Late vendor should have 0 delivery score (5 days late * 20 penalty = 100 penalty)
        self.assertEqual(late['delivery_score'], 0.0)
        
        # Over-budget should have low price score (< 50)
        self.assertTrue(over_budget['price_score'] <= 50.0)
        
        # Ensure it's sorted by final_score descending
        for i in range(len(results) - 1):
            self.assertTrue(results[i]['final_score'] >= results[i+1]['final_score'])

if __name__ == '__main__':
    unittest.main()
