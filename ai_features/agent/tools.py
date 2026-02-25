import re

class TextAnalyzerTool:
    """
    A tool to analyze text and compute readability scores and text density.
    """
    
    @staticmethod
    def _count_syllables(word):
        word = word.lower()
        if len(word) <= 3:
            return 1
        word = re.sub(r'(?:[^laeiouy]es|ed|[^laeiouy]e)$', '', word)
        word = re.sub(r'^y', '', word)
        syllables = len(re.findall(r'[aeiouy]{1,2}', word))
        return max(1, syllables)

    @classmethod
    def calculate_readability(cls, text: str) -> dict:
        """
        Calculates the Flesch Reading Ease score and extracts density metrics.
        Returns: {
            "readability_score": float,
            "word_count": int,
            "sentence_count": int,
            "avg_words_per_sentence": float,
            "density": str
        }
        """
        if not text:
            return {
                "readability_score": 100.0,
                "word_count": 0,
                "sentence_count": 0,
                "avg_words_per_sentence": 0.0,
                "density": "Low"
            }

        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        words = re.findall(r'\b\w+\b', text)
        
        word_count = len(words)
        sentence_count = len(sentences) or 1
        syllable_count = sum(cls._count_syllables(w) for w in words)
        
        if word_count == 0:
            return {
                "readability_score": 100.0,
                "word_count": 0,
                "sentence_count": sentence_count,
                "avg_words_per_sentence": 0.0,
                "density": "Low"
            }

        avg_words_per_sentence = word_count / sentence_count
        avg_syllables_per_word = syllable_count / word_count

        # Flesch Reading Ease Formula
        score = 206.835 - 1.015 * avg_words_per_sentence - 84.6 * avg_syllables_per_word
        
        if avg_words_per_sentence > 25:
            density = "High"
        elif avg_words_per_sentence > 15:
            density = "Medium"
        else:
            density = "Low"

        return {
            "readability_score": round(max(0.0, min(100.0, score)), 2),
            "word_count": word_count,
            "sentence_count": sentence_count,
            "avg_words_per_sentence": round(avg_words_per_sentence, 2),
            "density": density
        }
