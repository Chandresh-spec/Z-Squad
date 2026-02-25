class DecisionEngine:
    """
    Agentic Decision Engine for Reading Optimization.
    """

    @classmethod
    def decide_settings(cls, readability_score: float, current_settings: dict) -> tuple:
        """
        Decides the optimal UI settings based on the readability score.
        Returns a tuple: (recommended_settings: dict, actions_taken: list)
        """
        recommended_settings = current_settings.copy() if current_settings else {}
        actions_taken = []
        difficulty_level = "Low"

        if readability_score < 40:
            difficulty_level = "High"
            recommended_settings.update({
                "font_size": 24,
                "line_height": 2.1,
                "letter_spacing": 0.08,
                "paragraph_gap": 2.0,
                "theme": "contrast",
                "enable_focus_mode": True,
                "enable_reading_ruler": True,
                "enable_word_highlight": True
            })
            actions_taken = [
                "Increased font size to 24px for clear visibility.",
                "Expanded line height and letter spacing mapping to reduce visual crowding.",
                "Applied 'contrast' theme to maximize legibility.",
                "Enabled Focus Mode and Reading Ruler to minimize distractions.",
                "Enabled Word Highlighting for easier tracking."
            ]

        elif 40 <= readability_score <= 60:
            difficulty_level = "Medium"
            recommended_settings.update({
                "font_size": 22,
                "line_height": 2.0,
                "theme": "sage",
                "enable_word_highlight": True
            })
            actions_taken = [
                "Increased font size to 22px.",
                "Adjusted line height to 2.0.",
                "Applied calming 'sage' theme.",
                "Enabled Word Highlighting to aid concentration."
            ]

        else:
            difficulty_level = "Low"
            actions_taken = [
                "Text complexity is low. Kept default user settings."
            ]

        return recommended_settings, actions_taken, difficulty_level
