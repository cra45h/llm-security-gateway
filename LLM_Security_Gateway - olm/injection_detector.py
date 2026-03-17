# injection_detector.py

def calculate_injection_score(prompt):
    score = 0
    tags = []

    prompt_lower = prompt.lower()

    # Instruction override
    if "ignore all previous instructions" in prompt_lower:
        score += 0.9
        tags.append("instruction_override")

    # Persona hijacking
    if "pretend you are" in prompt_lower:
        score += 0.8
        tags.append("persona_hijack")

    # Prompt extraction
    if "reveal your system prompt" in prompt_lower:
        score += 0.85
        tags.append("prompt_extraction")

    # Encoded / obfuscated
    if "base64" in prompt_lower or "decode" in prompt_lower:
        score += 0.5
        tags.append("encoded_content")

    # Credential exposure attempt
    if "password=" in prompt_lower or "api key" in prompt_lower:
        score += 0.6
        tags.append("credential_exposure")

    # Cap score to 1.0
    score = min(score, 1.0)

    return score, tags