# main.py

import time
import requests

from injection_detector import calculate_injection_score
from presidio_module import analyze_pii, anonymize_text, add_custom_recognizers
from policy_engine import decide_policy
from utils import print_result

# Initialize Presidio custom recognizers
add_custom_recognizers()


# ------------------ LLM FUNCTION ------------------

def send_to_llm(prompt):
    start_time = time.time()

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": prompt,
                "stream": False
            }
        )

        llm_latency = time.time() - start_time

        # Extract response text
        result = response.json().get("response", "No response from LLM")

        return result, llm_latency

    except Exception as e:
        return f"LLM Error: {e}", 0


# ------------------ MAIN PIPELINE ------------------

def process_prompt(prompt):

    gateway_start = time.time()

    # Step 1: Injection Detection
    score, tags = calculate_injection_score(prompt)

    # Step 2: PII Detection
    pii_results = analyze_pii(prompt)

    # Step 3: Policy Decision
    decision = decide_policy(score, pii_results)

    # Step 4: Output Handling
    llm_response = None
    llm_latency = 0

    if decision == "MASK":
        sanitized = anonymize_text(prompt, pii_results)
        llm_response, llm_latency = send_to_llm(sanitized)
        output = sanitized

    elif decision == "ALLOW":
        llm_response, llm_latency = send_to_llm(prompt)
        output = prompt

    else:
        output = "❌ BLOCKED: Unsafe input detected"

    gateway_latency = time.time() - gateway_start
    total_latency = gateway_latency + llm_latency

    return {
        "prompt": prompt,
        "score": score,
        "tags": tags,
        "decision": decision,
        "output": output,
        "llm_response": llm_response,
        "gateway_latency": gateway_latency,
        "llm_latency": llm_latency,
        "total_latency": total_latency
    }


# ------------------ USER INPUT LOOP ------------------

if __name__ == "__main__":

    print("🔐 LLM Security Gateway with Ollama (Type 'exit' to quit)")

    while True:
        print("\nEnter your prompt:")
        user_input = input(">> ")

        if user_input.lower() == "exit":
            print("Exiting program...")
            break

        result = process_prompt(user_input)

        print_result(result)