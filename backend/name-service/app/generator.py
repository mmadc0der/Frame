import random
from typing import Optional, List
from .word_lists import adjectives, nouns

class NameGenerator:
    def __init__(self):
        self.adjectives = adjectives
        self.nouns = nouns
        
    def _get_random_number(self) -> str:
        """Generate a random 2-4 digit number"""
        return str(random.randint(10, 9999))
    
    def _get_word_pair(self, style: str) -> tuple[str, str]:
        """Get a random adjective-noun pair based on style"""
        if style == "funny":
            # Use more playful adjectives for funny style
            adj = random.choice([a for a in self.adjectives if len(a) < 8])
        elif style == "serious":
            # Use more formal adjectives for serious style
            adj = random.choice([a for a in self.adjectives if len(a) > 5])
        else:
            # Default style - use any adjective
            adj = random.choice(self.adjectives)
            
        noun = random.choice(self.nouns)
        return adj, noun
    
    def generate(self, prefix: Optional[str] = None, style: str = "default") -> str:
        """
        Generate a username
        
        Args:
            prefix: Optional prefix for the username
            style: Style of the username (default, funny, serious)
            
        Returns:
            A generated username
        """
        if style not in ["default", "funny", "serious"]:
            raise ValueError(f"Invalid style: {style}")
            
        adj, noun = self._get_word_pair(style)
        
        # 50% chance to add a number
        add_number = random.choice([True, False])
        number = self._get_random_number() if add_number else ""
        
        if prefix:
            # If prefix is provided, use it instead of adjective
            username = f"{prefix}{noun}{number}"
        else:
            username = f"{adj}{noun}{number}"
            
        return username.lower()
