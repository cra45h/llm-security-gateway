# utils.py

def print_separator():
    print("\n" + "=" * 50)


def print_result(result):
    print_separator()
    print(f"Prompt: {result['prompt']}")
    print(f"Injection Score: {result['score']}")
    print(f"Tags: {result['tags']}")
    print(f"Decision: {result['decision']}")
    print(f"Output Sent to LLM: {result['output']}")

    # Show LLM response if exists
    if result.get("llm_response"):
        print("\nLLM Response:")
        print(result["llm_response"])

    print("\n--- Latency ---")
    print(f"Gateway Latency: {round(result['gateway_latency'], 4)} sec")
    print(f"LLM Latency: {round(result['llm_latency'], 4)} sec")
    print(f"Total Latency: {round(result['total_latency'], 4)} sec")

    print_separator()