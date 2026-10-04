import importlib.util
import sys
import types
import unittest
from unittest.mock import patch


class FakeGraph:
    def __init__(self, _state_type):
        self.routes = {}

    def add_node(self, *_args):
        pass

    def set_entry_point(self, *_args):
        pass

    def add_conditional_edges(self, source, route, _mapping):
        self.routes[source] = route

    def add_edge(self, *_args):
        pass

    def compile(self):
        return self


class GraphRoutingTests(unittest.TestCase):
    def test_every_stage_stops_on_error(self):
        modules = {}
        graph_lib = types.ModuleType("langgraph.graph")
        graph_lib.StateGraph = FakeGraph
        graph_lib.END = "__end__"
        modules["langgraph"] = types.ModuleType("langgraph")
        modules["langgraph.graph"] = graph_lib
        for name, symbol in (
            ("agents.twitter_agent", "twitter_factory_node"),
            ("agents.persist_agent", "persist_research_node"),
            ("agents.tokenomics_agent", "tokenomics_node"),
            ("agents.risk_agent", "risk_node"),
            ("agents.verification_agent", "verification_node"),
            ("tools.smart_miner_adapter", "fetch_raw_data_from_miner"),
            ("core.repositories", "save_evidence"),
        ):
            module = types.ModuleType(name)
            setattr(module, symbol, lambda *_args: None)
            modules[name] = module
        spec = importlib.util.spec_from_file_location("graph_under_test", "agents/graph.py")
        graph = importlib.util.module_from_spec(spec)
        with patch.dict(sys.modules, modules):
            spec.loader.exec_module(graph)
        self.assertEqual(len(graph.workflow.routes), 5)
        for route in graph.workflow.routes.values():
            self.assertEqual(route({"errors": ["failure"]}), "__end__")
            self.assertEqual(route({"errors": [], "current_step": "failed"}), "__end__")
            self.assertNotEqual(route({"errors": [], "current_step": "ok"}), "__end__")


if __name__ == "__main__":
    unittest.main()
