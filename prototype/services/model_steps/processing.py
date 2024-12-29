
from enum import Enum
import spacy
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import threading

class CriticityLevel(Enum):
    LOW = "LOW"
    MEDIUM = "MED"
    HIGH = "HIGH"

class Processing:
    risk_criteria = {
            "delays": {
                "delay": CriticityLevel.MEDIUM,
                "behind schedule": CriticityLevel.HIGH,
                "late": CriticityLevel.MEDIUM,
                "deadline": CriticityLevel.MEDIUM,
                "postpone": CriticityLevel.HIGH,
                "reschedule": CriticityLevel.MEDIUM,
                "untrack": CriticityLevel.HIGH,
                "slippage": CriticityLevel.HIGH,
                "defer": CriticityLevel.LOW,
                "extension": CriticityLevel.LOW,
                "overdue": CriticityLevel.HIGH,
            },
            "costs": {
                "overbudget": CriticityLevel.HIGH,
                "budget overrun": CriticityLevel.HIGH,
                "unexpected cost": CriticityLevel.HIGH,
                "too expensive": CriticityLevel.MEDIUM,
                "cost increase": CriticityLevel.MEDIUM,
                "financial": CriticityLevel.LOW,
                "costly": CriticityLevel.MEDIUM,
                "fund": CriticityLevel.LOW,
                "underestimate": CriticityLevel.MEDIUM,
                "excess": CriticityLevel.MEDIUM,
                "extra": CriticityLevel.LOW,
                "expense": CriticityLevel.LOW,
                "price": CriticityLevel.LOW,
                "surge": CriticityLevel.MEDIUM,
                "expenditure": CriticityLevel.MEDIUM,
            },
            "quality": {
                "defect": CriticityLevel.HIGH,
                "poor quality": CriticityLevel.HIGH,
                "rework": CriticityLevel.MEDIUM,
                "redo": CriticityLevel.MEDIUM,
                "issue": CriticityLevel.MEDIUM,
                "problem": CriticityLevel.MEDIUM,
                "nonconformity": CriticityLevel.HIGH,
                "outdate": CriticityLevel.MEDIUM,
                "bug": CriticityLevel.HIGH,
                "glitch": CriticityLevel.MEDIUM,
                "substandard": CriticityLevel.HIGH,
                "flaw": CriticityLevel.HIGH,
                "deficiency": CriticityLevel.HIGH,
                "not meet standard": CriticityLevel.HIGH,
                "incomplete": CriticityLevel.HIGH,
                "redesign": CriticityLevel.MEDIUM,
                "quality drop": CriticityLevel.HIGH,
                "malfunction": CriticityLevel.HIGH,
                "improvement": CriticityLevel.LOW,
                "unplanned": CriticityLevel.HIGH,
            },
        }

    # print("Loading spacy model...")
    # nlp = spacy.load('en_core_web_md')
    # print("Done !")
    _nlp_instance = None
    _lock = threading.Lock()

    @classmethod
    def get_nlp(cls):
        # Lazy loading avec verrou pour éviter les problèmes en multi-threading
        if cls._nlp_instance is None:
            with cls._lock:
                if cls._nlp_instance is None:  # Double vérification
                    print("Loading spacy model...")
                    cls._nlp_instance = spacy.load('en_core_web_md')
                    print("Done!")
        return cls._nlp_instance

    @staticmethod
    def analyze_risks(text):
        nlp = Processing.get_nlp()

        # Analyser le texte avec SpaCy
        doc = nlp(text) # To be moved to an upper block
        lemmatized_text = " ".join([token.lemma_.lower() for token in doc if token.is_alpha])
        detected_risks = [] 
        # TODO : parallélisme
        text_vectors = [nlp(word).vector for word in lemmatized_text.split()]
        
        similarity_threshold = 0.8
        for category, keywords in Processing.risk_criteria.items():
            for keyword, criticity in keywords.items():
                # Le mot clé est exactement reconnu
                if keyword in lemmatized_text:
                    detected_risks.append({
                        "CATEGORY" : category,
                        "CRITERIA" : keyword,
                        "RISK_LEVEL" : criticity.value
                    })
                    continue
                # Recherche par similitude vectorielle (embeddedings)
                keyword_vector = nlp(keyword).vector
                similarities = cosine_similarity([keyword_vector], text_vectors)
                max_similarity = np.max(similarities)
                if max_similarity >= similarity_threshold:
                    detected_risks.append({
                        "CATEGORY" : category,
                        "CRITERIA" : keyword,
                        "RISK_LEVEL" : criticity.value
                    })
                    continue
        return detected_risks
    
if __name__ == "__main__":
    message1 = "The project was postponned"
    print("Analazing message 1...")
    detected_risk = Processing.analyze_risks(message1)
    print("Risk detected : ", detected_risk)

    message2 = "What a nice day !"
    print("Analazing message 2...")
    detected_risk = Processing.analyze_risks(message2)
    print("Risk detected : ", detected_risk)
    
    message3 = "There are a lot of bugs in the project."
    print("Analazing message 3...")
    detected_risk = Processing.analyze_risks(message3)
    print("Risk detected : ", detected_risk)