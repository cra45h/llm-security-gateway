# policy_engine.py

from config import ALLOW_THRESHOLD, BLOCK_THRESHOLD, HIGH_RISK_ENTITIES


def decide_policy(score, pii_results):

    # BLOCK if injection score high
    if score >= BLOCK_THRESHOLD:
        return "BLOCK"

    # BLOCK if high-risk PII found
    for entity in pii_results:
        if entity.entity_type in HIGH_RISK_ENTITIES:
            return "BLOCK"

    # MASK if PII exists
    if len(pii_results) > 0:
        return "MASK"

    # Otherwise allow
    if score <= ALLOW_THRESHOLD:
        return "ALLOW"

    return "MASK"