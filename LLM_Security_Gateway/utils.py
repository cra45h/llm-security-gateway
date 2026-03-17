# utils.py

def print_separator():
    print("\n" + "="*50 + "\n")


def print_result(result):
    print_separator()
    print(f"Prompt: {result['prompt']}")
    print(f"Injection Score: {result['score']}")
    print(f"Tags: {result['tags']}")
    print(f"Decision: {result['decision']}")
    print(f"Output: {result['output']}")
    print(f"Latency: {round(result['latency'], 4)} sec")
    print_separator()