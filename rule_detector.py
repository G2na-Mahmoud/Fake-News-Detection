# rule_detector.py
import re
from datetime import datetime
from config import TRUSTED_SOURCES, UNTRUSTED_SOURCES

class FakeNewsDetector:
    def __init__(self):
        self.clickbait_words = [
            "عاجل", "خطير", "لن تصدق", "صدمة", "كارثة", "تحذير", 
            "فضيحة", "مذهل", "مفاجأة", "مروع", "صادم", "لا تعليق",
            "breaking", "urgent", "shocking", "unbelievable", "you won't believe"
        ]
        
        self.sensational_words = [
            "كارثة", "إنهيار", "حرب", "أزمة", "إغتيال", "موت", 
            "فضيحة", "إتهام", "فضيحة", "إعتقال", "سجن"
        ]
        
        self.credibility_indicators = [
            "مصدر مسؤول", "حسب مصادر", "صرح لـ", "ذكرت وكالة",
            "نقلاً عن", "حسب ما أفاد", "بحسب"
        ]

    def clean_text(self, text):
        """تنظيف النص"""
        if not text:
            return ""
        
        text = str(text).lower()
        # إزالة الرموز الخاصة
        text = re.sub(r'[^\w\s\u0600-\u06FF]', ' ', text)
        # إزالة المسافات الزائدة
        text = re.sub(r'\s+', ' ', text)
        return text.strip()

    def analyze_style(self, text):
        """تحليل أسلوب النص"""
        score = 0
        reasons = []
        
        clean_text = self.clean_text(text)
        words = clean_text.split()
        
        # 1. كثافة علامات التعجب والاستفهام
        exclamations = text.count('!') + text.count('؟')
        if exclamations >= 3:
            score += 20
            reasons.append(f"كثافة علامات التعجب ({exclamations})")
        
        # 2. النص بالكامل كبير (صراخ)
        if text.isupper():
            score += 15
            reasons.append("النص مكتوب بالكامل بحروف كبيرة")
        
        # 3. كلمات مثيرة
        for word in self.clickbait_words:
            if word in clean_text:
                score += 10
                reasons.append(f"كلمة مثيرة: {word}")
        
        # 4. كثافة الكلمات العاطفية
        emotional_count = 0
        for word in self.sensational_words:
            emotional_count += clean_text.count(word)
        
        if emotional_count >= 3:
            score += 15
            reasons.append(f"كثافة الكلمات العاطفية ({emotional_count})")
        
        # 5. طول النص
        if len(words) < 30:
            score += 10
            reasons.append("النص قصير جداً (أقل من 30 كلمة)")
        
        # 6. علامات المصداقية
        credibility_score = 0
        for indicator in self.credibility_indicators:
            if indicator in text:
                credibility_score += 5
        
        score -= credibility_score  # خصم النقاط للتصريحات الموثقة
        
        return score, reasons

    def analyze_source(self, source):
        """تحليل مصدر الخبر"""
        score = 0
        reasons = []
        
        if not source:
            score += 15
            reasons.append("المصدر غير معروف")
            return score, reasons
        
        source_lower = source.lower()
        
        # تحقق من المصادر الموثوقة
        is_trusted = False
        for trusted in TRUSTED_SOURCES:
            if trusted in source_lower:
                score -= 20
                reasons.append(f"مصدر موثوق: {trusted}")
                is_trusted = True
                break
        
        # تحقق من المصادر غير الموثوقة
        if not is_trusted:
            for untrusted in UNTRUSTED_SOURCES:
                if untrusted in source_lower:
                    score += 25
                    reasons.append(f"مصدر غير موثوق: {untrusted}")
                    break
        
        # إذا المصدر ليس في القوائم
        if score == 0:
            score += 10
            reasons.append("المصدر غير مصنف")
        
        return score, reasons

    def check_url_patterns(self, text):
        """البحث عن روابط غير موثوقة في النص"""
        score = 0
        reasons = []
        
        url_patterns = [
            r'bit\.ly/\w+',
            r'tinyurl\.com/\w+',
            r'goo\.gl/\w+',
            r'is\.gd/\w+'
        ]
        
        for pattern in url_patterns:
            if re.search(pattern, text):
                score += 15
                reasons.append("يحتوي على روابط مختصرة قد تكون مشبوهة")
                break
        
        return score, reasons

    def detect(self, title="", text="", source=""):
        """الكشف الرئيسي عن الأخبار المزيفة"""
        total_score = 0
        all_reasons = []
        
        # 1. تحليل العنوان
        if title:
            title_score, title_reasons = self.analyze_style(title)
            total_score += title_score
            all_reasons.extend(title_reasons)
        
        # 2. تحليل النص
        if text:
            text_score, text_reasons = self.analyze_style(text)
            total_score += text_score
            all_reasons.extend(text_reasons)
            
            # تحليل الأنماط في النص
            url_score, url_reasons = self.check_url_patterns(text)
            total_score += url_score
            all_reasons.extend(url_reasons)
        
        # 3. تحليل المصدر
        if source:
            source_score, source_reasons = self.analyze_source(source)
            total_score += source_score
            all_reasons.extend(source_reasons)
        
        # 4. تحديد النتيجة النهائية
        if total_score >= 50:
            result = "خبر مزيف"
            color = "danger"
            confidence = "عالية"
        elif total_score >= 30:
            result = "مشبوه"
            color = "warning"
            confidence = "متوسطة"
        else:
            result = "خبر حقيقي"
            color = "success"
            confidence = "منخفضة"
        
        return {
            "result": result,
            "score": total_score,
            "reasons": all_reasons[:5],  # أول 5 أسباب فقط
            "color": color,
            "confidence": confidence,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }