# presidio_module.py

from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

# Initialize engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()


# ------------------ CUSTOM RECOGNIZERS ------------------

def add_custom_recognizers():

    # 🔹 API Key Recognizer
    api_key_pattern = Pattern(
        name="api_key_pattern",
        regex=r"sk-[a-zA-Z0-9]+",
        score=0.9
    )

    api_key_recognizer = PatternRecognizer(
        supported_entity="API_KEY",
        patterns=[api_key_pattern]
    )

    # 🔹 Phone Number (Pakistan format)
    phone_pattern = Pattern(
        name="phone_pattern",
        regex=r"03[0-9]{9}",
        score=0.8
    )

    phone_recognizer = PatternRecognizer(
        supported_entity="PHONE_CUSTOM",
        patterns=[phone_pattern]
    )

    # 🔹 Employee ID
    emp_pattern = Pattern(
        name="employee_id_pattern",
        regex=r"EMP-[A-Za-z0-9]+",
        score=0.85
    )

    emp_recognizer = PatternRecognizer(
        supported_entity="EMPLOYEE_ID",
        patterns=[emp_pattern]
    )

    # Add all recognizers to registry
    analyzer.registry.add_recognizer(api_key_recognizer)
    analyzer.registry.add_recognizer(phone_recognizer)
    analyzer.registry.add_recognizer(emp_recognizer)


# ------------------ PII ANALYSIS ------------------

def analyze_pii(text):
    results = analyzer.analyze(
        text=text,
        language="en"
    )
    return results


# ------------------ ANONYMIZATION ------------------

def anonymize_text(text, results):
    anonymized = anonymizer.anonymize(
        text=text,
        analyzer_results=results
    )
    return anonymized.text