class ProcurementRiskEngine:
    @staticmethod
    def evaluate_risk(vendor_price, budget, vendor_delivery, required_delivery, reliability, accuracy, rating):
        risks = []
        risk_score = 0
        
        # 1. Budget Risk
        if vendor_price > budget:
            overage = vendor_price - budget
            risks.append(f"Price exceeds budget by ₹{overage:,.2f}")
            risk_score += 20
            
        # 2. Delivery Risk
        if vendor_delivery > required_delivery:
            days_late = vendor_delivery - required_delivery
            risks.append(f"Delivery exceeds requirement by {days_late} days")
            risk_score += 20
            
        # 3. Reliability Risk
        if reliability < 80:
            risks.append(f"Reliability ({reliability}%) is below preferred threshold of 80%")
            risk_score += 20
            
        # 4. Order Accuracy Risk
        if accuracy < 90:
            risks.append(f"Order accuracy ({accuracy}%) is below preferred threshold of 90%")
            risk_score += 20
            
        # 5. Vendor Performance Risk
        if rating < 80:
            risks.append(f"Overall rating ({rating}) indicates poor historical performance")
            risk_score += 20
            
        # Determine risk level
        if risk_score <= 25:
            risk_level = "LOW"
        elif risk_score <= 50:
            risk_level = "MEDIUM"
        elif risk_score <= 75:
            risk_level = "HIGH"
        else:
            risk_level = "CRITICAL"
            
        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "risks": risks
        }
