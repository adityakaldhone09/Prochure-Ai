import os
import json
import logging
import requests
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    @staticmethod
    def generate_explanation(pr_details, vendors, recommended_vendor):
        """
        Calls an LLM API to generate a natural language explanation for the procurement decision.
        Falls back to a deterministic explanation if AI fails or is disabled.
        """
        
        fallback_explanation = (
            f"{recommended_vendor['vendor_name']} is recommended due to achieving the highest overall score of "
            f"{recommended_vendor['final_score']}/100. They provide a strong balance with a price score of "
            f"{recommended_vendor['price_score']} and delivery score of {recommended_vendor['delivery_score']}, "
            f"remaining within acceptable risk thresholds.\n\n"
            f"Alternatives were not selected due to lower composite scores across price, delivery, and reliability metrics."
        )

        if not Config.AI_ENABLED:
            logger.info("AI Service disabled. Using fallback deterministic explanation.")
            return fallback_explanation

        if not Config.AI_API_KEY:
            logger.warning("AI_API_KEY not found. Falling back to deterministic explanation.")
            return fallback_explanation
            
        try:
            prompt = AIService._build_prompt(pr_details, vendors, recommended_vendor)
            
            url = "https://api.openai.com/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {Config.AI_API_KEY}",
                "Content-Type": "application/json"
            }
            payload = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": "You are a procurement AI assistant. Explain procurement recommendations based purely on the provided scores, prices, and risks. Do NOT fabricate confidence scores. Do NOT hallucinate new scores or facts. Be concise, professional, and explain why the top vendor was chosen and why alternatives were rejected."
                    },
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.3,
                "max_tokens": 500
            }
            
            logger.info("Calling AI API for explanation...")
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return data['choices'][0]['message']['content'].strip()
            else:
                logger.error(f"AI API returned {response.status_code}: {response.text}")
                return fallback_explanation
                
        except Exception as e:
            logger.error(f"AI Service Exception: {e}")
            return fallback_explanation

    @staticmethod
    def _build_prompt(pr_details, vendors, recommended):
        prompt = f"""
Purchase Request:
Product: {pr_details.get('product')}
Quantity: {pr_details.get('quantity')}
Budget per unit: ₹{pr_details.get('budget')}
Required Delivery Date: {pr_details.get('delivery_date')}

Vendor Recommendations:
Recommended Vendor: {recommended['vendor_name']} (Final Score: {recommended['final_score']}/100)
Risk Level: {recommended['risk_level']}
Risks Identified: {', '.join(recommended.get('risks', ['None']))}

All Evaluated Vendors (Ranked by Score):
"""
        for v in vendors:
            prompt += f"- {v['vendor_name']}: Score {v['final_score']}/100, Price: ₹{v['raw_price']}, Delivery: {v['raw_delivery']} days, Reliability: {v.get('reliability_score', 0)}%, Accuracy: {v.get('accuracy_score', 0)}%, Risk: {v['risk_level']}\n"
            
        prompt += """
Please provide a well-structured, 3-paragraph explanation:
1. Recommended Vendor: A concise summary explaining why the recommended vendor was chosen based on their specific strengths.
2. Alternatives: A brief explanation of why the top alternatives were not selected.
3. Risk Summary: A summary of the procurement risks for the chosen vendor.
"""
        return prompt
