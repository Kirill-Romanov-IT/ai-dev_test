# test_tabouret.py
import unittest
from tabouret_agent import ConversationAgent, Stage

class TestStageTransitions(unittest.TestCase):
    def setUp(self):
        self.agent = ConversationAgent(api_key="dummy-key")  # mock key
        self.agent.model = DummyModel()  # patch model

    def test_full_flow(self):
        stages = []
        for _ in range(7):
            resp = self.agent.process_turn("ok")
            stages.append(resp["stage"])
        self.assertIn(Stage.END, stages)

class DummyModel:
    def generate_content(self, prompt):
        class R: text = "Mocked agent reply."
        return R()

if __name__ == "__main__":
    unittest.main()
