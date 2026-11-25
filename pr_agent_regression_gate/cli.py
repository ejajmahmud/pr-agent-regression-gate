"""CLI for PR Agent Regression Gate."""
import argparse
import json
from .core import AgentRegressionGate


def main():
    parser = argparse.ArgumentParser(description="PR Agent Regression Gate CLI")
    parser.add_argument("--cand-pass", type=float, default=0.92, help="Candidate pass rate")
    parser.add_argument("--cand-tokens", type=float, default=1100, help="Candidate avg tokens")
    args = parser.parse_args()

    gate = AgentRegressionGate()
    res = gate.compare(
        {"pass_rate": 0.90, "avg_tokens": 1000, "p95_ms": 1200},
        {"pass_rate": args.cand_pass, "avg_tokens": args.cand_tokens, "p95_ms": 1220},
    )
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main()
