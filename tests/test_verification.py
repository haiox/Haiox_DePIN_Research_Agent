import asyncio
import json
import sys
import types
import unittest
from unittest.mock import AsyncMock, patch


# The verification logic can be tested without network/database dependencies.
repository = types.ModuleType("core.repositories")
repository.get_evidence_by_id = lambda _: {"content": "The network has 100 nodes."}
router = types.ModuleType("core.llm_router")
router.call_llm = AsyncMock()
sys.modules["core.repositories"] = repository
sys.modules["core.llm_router"] = router

from agents.verification_agent import validate_verification, verification_node


class VerificationTests(unittest.TestCase):
    def setUp(self):
        self.state = {
            "evidence_id": 1,
            "structured_findings": {
                "tokenomics": {"nodes": 100},
                "risk": {"risk_assessment": {"technical_risks": ["Capacity unknown"], "red_flags": []}},
            },
            "errors": [],
        }

    def test_valid_quote(self):
        data = {
            "verification_summary": "One claim checked",
            "claim_evaluations": [{
                "claim": "Node count", "status": "supported",
                "confidence_score": 0.8, "source_quote": "100 nodes",
            }],
        }
        self.assertEqual(validate_verification(data, "The network has 100 nodes."), data)

    def test_fabricated_quote_is_rejected(self):
        data = {
            "verification_summary": "Claim checked",
            "claim_evaluations": [{
                "claim": "Node count", "status": "supported",
                "confidence_score": 0.85, "source_quote": "Direct scraper output",
            }],
        }
        with self.assertRaises(ValueError):
            validate_verification(data, "The network has 100 nodes.")

    def test_llm_failure_never_becomes_supported(self):
        with patch.object(router, "call_llm", new=AsyncMock(side_effect=TimeoutError("timeout"))):
            result = asyncio.run(verification_node(self.state))
        self.assertEqual(result["current_step"], "failed")
        self.assertNotIn("verification_result", result)

    def test_invalid_json_never_becomes_supported(self):
        with patch.object(router, "call_llm", new=AsyncMock(return_value="not json")):
            result = asyncio.run(verification_node(self.state))
        self.assertEqual(result["current_step"], "failed")
        self.assertNotIn("verification_result", result)


if __name__ == "__main__":
    unittest.main()
