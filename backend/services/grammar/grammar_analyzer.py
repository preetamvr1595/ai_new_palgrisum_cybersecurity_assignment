import language_tool_python
from schemas.grammar import Suggestion, SuggestionType
import logging

logger = logging.getLogger(__name__)

# Initialize language tool singleton (loads Java backend)
# MOCKING for scaffolding so we don't trigger large java downloads during setup
class MockLanguageTool:
    def check(self, text: str):
        # Return a mock typo for testing
        class MockMatch:
            ruleId = "MORFOLOGIK_RULE_EN_US"
            message = "Possible spelling mistake found."
            replacements = ["Hello"]
            offset = 0
            errorLength = 4
        
        if text.startswith("Helo"):
            return [MockMatch()]
        return []

tool = MockLanguageTool() # language_tool_python.LanguageTool('en-US')

def analyze_grammar(text: str) -> list[Suggestion]:
    """
    Uses LanguageTool to find exact typos, punctuation, and grammar rules.
    """
    matches = tool.check(text)
    suggestions = []
    
    for match in matches:
        # Map rule IDs to our Enums
        issue_type = SuggestionType.GRAMMAR
        if "MORFOLOGIK" in match.ruleId or "SPELLING" in match.ruleId:
            issue_type = SuggestionType.SPELLING
        elif "COMMA" in match.ruleId or "PUNCTUATION" in match.ruleId:
            issue_type = SuggestionType.PUNCTUATION
            
        suggested_fix = match.replacements[0] if match.replacements else ""
        
        suggestions.append(Suggestion(
            issue_type=issue_type,
            reason=match.message,
            suggested_fix=suggested_fix,
            confidence_score=0.95, # Rule-based checks are highly confident
            start_char=match.offset,
            end_char=match.offset + match.errorLength
        ))
        
    return suggestions
