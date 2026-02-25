from .tools import TextAnalyzerTool
from .decision import DecisionEngine

class ReadingOptimizationAgent:
    """
    Agentic Pipeline that orchestrates the Reading Optimizer functionality.
    """

    def __init__(self):
        self.analyzer = TextAnalyzerTool()
        self.decision_engine = DecisionEngine()

    def process_text(self, text: str, current_settings: dict) -> dict:
        """
        Main runner:
        1. Analyzes text density and readability.
        2. Decides the best reading UI settings based on the metrics.
        3. Returns the formulated JSON response.
        """
        # Step 1: Analyze
        analysis_result = self.analyzer.calculate_readability(text)
        readability_score = analysis_result.get("readability_score", 100.0)

        # Step 2: Decide
        recommended_settings, actions_taken, difficulty = self.decision_engine.decide_settings(
            readability_score=readability_score,
            current_settings=current_settings
        )

        # Step 3: Respond
        return {
            "readability_score": readability_score,
            "difficulty_level": difficulty,
            "recommended_settings": recommended_settings,
            "actions_taken": actions_taken,
            "analysis_details": analysis_result
        }
