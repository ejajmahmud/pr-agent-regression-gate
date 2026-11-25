"""Core CI/CD regression gate comparing baseline vs candidate agent eval metrics."""
from typing import Any, Dict, List


class AgentRegressionGate:
    """Evaluates candidate vs baseline agent benchmarks against strict CI merge thresholds."""

    def __init__(
        self,
        max_pass_drop: float = 0.01,
        max_cost_increase_pct: float = 15.0,
        max_latency_increase_pct: float = 25.0,
    ):
        self.max_pass_drop = max_pass_drop
        self.max_cost_increase_pct = max_cost_increase_pct
        self.max_latency_increase_pct = max_latency_increase_pct

    def compare(self, baseline: Dict[str, float], candidate: Dict[str, float]) -> Dict[str, Any]:
        reasons: List[str] = []

        pass_delta = candidate["pass_rate"] - baseline["pass_rate"]
        if pass_delta < -self.max_pass_drop:
            reasons.append(f"pass_rate_dropped:{pass_delta:.3f}")

        cost_pct = ((candidate["avg_tokens"] - baseline["avg_tokens"]) / max(1e-6, baseline["avg_tokens"])) * 100.0
        if cost_pct > self.max_cost_increase_pct:
            reasons.append(f"token_cost_regressed:{cost_pct:.1f}%")

        lat_pct = ((candidate["p95_ms"] - baseline["p95_ms"]) / max(1e-6, baseline["p95_ms"])) * 100.0
        if lat_pct > self.max_latency_increase_pct:
            reasons.append(f"latency_regressed:{lat_pct:.1f}%")

        return {
            "decision": "APPROVE" if not reasons else "BLOCK",
            "pass_delta": round(pass_delta, 4),
            "token_delta_pct": round(cost_pct, 2),
            "latency_delta_pct": round(lat_pct, 2),
            "reasons": reasons,
        }
