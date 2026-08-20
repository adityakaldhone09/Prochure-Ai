class VendorScoringEngine:
    WEIGHTS = {
        'price': 0.35,
        'delivery': 0.25,
        'reliability': 0.20,
        'accuracy': 0.10,
        'rating': 0.10
    }

    @staticmethod
    def calculate_delivery_score(vendor_days, requested_days):
        """
        Compare vendor delivery time with requested delivery requirement.
        Within deadline: 100 (high score)
        Slightly late: reduced score (-20 points per day late)
        Significantly late: large penalty (drops to 0 quickly)
        """
        if vendor_days <= requested_days:
            return 100.0
        
        days_late = vendor_days - requested_days
        score = 100.0 - (days_late * 20.0)
        return max(0.0, score)

    @staticmethod
    def score_vendors(bids, vendor_profiles, requested_delivery, budget):
        """
        bids: list of dicts [{'vendor_id': 1, 'price_per_unit': 500, 'delivery_days': 5}]
        vendor_profiles: list of dicts [{'id': 1, 'name': 'A', 'reliability': 90, 'accuracy': 95, 'rating': 85}]
        """
        if not bids:
            return []

        # Find the lowest price among the bids to calculate price score
        valid_prices = [bid['price_per_unit'] for bid in bids]
        lowest_price = min(valid_prices) if valid_prices else 0

        scored_vendors = []

        # Create a lookup for vendor profiles
        profile_map = {v['id']: v for v in vendor_profiles}

        for bid in bids:
            vid = bid['vendor_id']
            profile = profile_map.get(vid, {})
            
            # Price Score Calculation
            price = bid['price_per_unit']
            if price > 0:
                price_score = (lowest_price / price) * 100.0
            else:
                price_score = 0.0
            
            # Additional penalty if over budget
            if price > budget:
                price_score *= 0.8 # 20% penalty for exceeding budget
                
            # Delivery Score Calculation
            delivery_score = VendorScoringEngine.calculate_delivery_score(
                bid['delivery_days'], requested_delivery
            )

            # Profile Scores
            reliability_score = float(profile.get('reliability', 50))
            accuracy_score = float(profile.get('accuracy', 50))
            rating_score = float(profile.get('rating', 50))

            # Final Score Calculation
            final_score = (
                (price_score * VendorScoringEngine.WEIGHTS['price']) +
                (delivery_score * VendorScoringEngine.WEIGHTS['delivery']) +
                (reliability_score * VendorScoringEngine.WEIGHTS['reliability']) +
                (accuracy_score * VendorScoringEngine.WEIGHTS['accuracy']) +
                (rating_score * VendorScoringEngine.WEIGHTS['rating'])
            )

            scored_vendors.append({
                'vendor_id': vid,
                'vendor_name': profile.get('name', f"Vendor {vid}"),
                'price_score': round(price_score, 2),
                'delivery_score': round(delivery_score, 2),
                'reliability_score': round(reliability_score, 2),
                'accuracy_score': round(accuracy_score, 2),
                'rating_score': round(rating_score, 2),
                'final_score': round(final_score, 2),
                'raw_price': price,
                'raw_delivery': bid['delivery_days']
            })

        # Sort descending by final score
        scored_vendors.sort(key=lambda x: x['final_score'], reverse=True)
        return scored_vendors
