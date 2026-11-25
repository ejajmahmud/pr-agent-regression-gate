"""Tests for PR Agent Regression Gate."""
import unittest
from pr_agent_regression_gate.core import AgentRegressionGate


class TestAgentRegressionGate(unittest.TestCase):
    def setUp(self):
        self.gate = AgentRegressionGate(max_pass_drop=0.01, max_cost_increase_pct=15.0)

    def test_approves_improvement_within_budget(self):
        res = self.gate.compare(
            {"pass_rate": 0.88, "avg_tokens": 1000, "p95_ms": 1000},
            {"pass_rate": 0.91, "avg_tokens": 1050, "p95_ms": 980},
        )
        self.assertEqual(res["decision"], "APPROVE")

    def test_blocks_token_cost_spike(self):
        res = self.gate.compare(
            {"pass_rate": 0.90, "avg_tokens": 1000, "p95_ms": 1000},
            {"pass_rate": 0.91, "avg_tokens": 1400, "p95_ms": 1000},
        )
        self.assertEqual(res["decision"], "BLOCK")
        self.assertTrue(any("token_cost_regressed" in r for r in res["reasons"]))
