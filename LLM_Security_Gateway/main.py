# main.py

import time
from injection_detector import calculate_injection_score
from presidio_module import analyze_pii, anonymize_text, add_custom_recognizers
from policy_engine import decide_policy
from utils import print_result


# Initialize custom recognizers
add_custom_recognizers()


def process_prompt(prompt):

    start_time = time.time()

    # Step 1: Injection Detection
    score, tags = calculate_injection_score(prompt)

    # Step 2: PII Detection
    pii_results = analyze_pii(prompt)

    # Step 3: Policy Decision
    decision = decide_policy(score, pii_results)

    # Step 4: Output handling
    if decision == "MASK":
        output = anonymize_text(prompt, pii_results)

    elif decision == "BLOCK":
        output = "❌ BLOCKED: Unsafe input detected"

    else:
        output = prompt

    latency = time.time() - start_time

    return {
        "prompt": prompt,
        "score": score,
        "tags": tags,
        "decision": decision,
        "output": output,
        "latency": latency
    }


# ------------------ TEST DATA ------------------

if __name__ == "__main__":

    while True:
        print("\nEnter your prompt (type 'exit' to quit):")
        user_input = input(">> ")

        if user_input.lower() == "exit":
            print("Exiting...")
            break

        result = process_prompt(user_input)
        print_result(result)