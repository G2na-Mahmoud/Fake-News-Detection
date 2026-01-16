# google_checker.py
import requests
from config import GOOGLE_API_KEY

class GoogleFactChecker:
    def __init__(self):
        self.api_key = GOOGLE_API_KEY
        self.base_url = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
    
    def check_claim(self, claim_text, language="ar"):
        """التحقق من صحة الادعاء باستخدام Google Fact Check"""
        
        if not self.api_key or self.api_key == "AIzaSyDexample...":
            return None
        
        params = {
            "query": claim_text[:100],  # أول 100 حرف فقط
            "languageCode": language,
            "key": self.api_key
        }
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if "claims" in data and len(data["claims"]) > 0:
                    claims = data["claims"][:3]  # أول 3 نتائج فقط
                    
                    results = []
                    for claim in claims:
                        claim_data = {
                            "text": claim.get("text", ""),
                            "claimant": claim.get("claimant", "غير معروف"),
                            "claim_date": claim.get("claimDate", ""),
                            "rating": claim.get("claimReview", [{}])[0].get("textualRating", "غير متوفر"),
                            "reviewer": claim.get("claimReview", [{}])[0].get("publisher", {}).get("name", "غير معروف"),
                            "url": claim.get("claimReview", [{}])[0].get("url", ""),
                        }
                        results.append(claim_data)
                    
                    return results
            
            return None
            
        except Exception as e:
            print(f"خطأ في التحقق من Google: {e}")
            return None
    
    def get_overall_rating(self, google_results):
        """الحصول على تقييم عام من نتائج Google"""
        if not google_results:
            return None
        
        ratings = {
            "TRUE": 0,
            "FALSE": 0,
            "MISLEADING": 0,
            "UNPROVEN": 0
        }
        
        for result in google_results:
            rating = result.get("rating", "").upper()
            if "TRUE" in rating or "صحيح" in rating or "حقيقي" in rating:
                ratings["TRUE"] += 1
            elif "FALSE" in rating or "خاطئ" in rating or "مزيف" in rating:
                ratings["FALSE"] += 1
            elif "MISLEADING" in rating or "مضلل" in rating:
                ratings["MISLEADING"] += 1
            else:
                ratings["UNPROVEN"] += 1
        
        # العثور على التصنيف الأكثر تكرارًا
        max_rating = max(ratings, key=ratings.get)
        
        if ratings[max_rating] > 0:
            return {
                "rating": max_rating,
                "count": ratings[max_rating],
                "total": len(google_results)
            }
        
        return None