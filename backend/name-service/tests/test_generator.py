import pytest
from app.generator import NameGenerator

@pytest.fixture
def generator():
    return NameGenerator()

def test_generator_initialization(generator):
    """Test that generator initializes with word lists"""
    assert len(generator.adjectives) > 0
    assert len(generator.nouns) > 0

def test_random_number_generation(generator):
    """Test random number generation"""
    number = generator._get_random_number()
    assert number.isdigit()
    assert 10 <= int(number) <= 9999

def test_word_pair_generation(generator):
    """Test word pair generation for different styles"""
    # Test default style
    adj, noun = generator._get_word_pair("default")
    assert adj in generator.adjectives
    assert noun in generator.nouns
    
    # Test funny style
    adj, noun = generator._get_word_pair("funny")
    assert adj in generator.adjectives
    assert len(adj) < 8  # Funny style uses shorter adjectives
    assert noun in generator.nouns
    
    # Test serious style
    adj, noun = generator._get_word_pair("serious")
    assert adj in generator.adjectives
    assert len(adj) > 5  # Serious style uses longer adjectives
    assert noun in generator.nouns

def test_username_generation(generator):
    """Test username generation with different parameters"""
    # Test default generation
    username = generator.generate()
    assert isinstance(username, str)
    assert len(username) > 0
    
    # Test with prefix
    prefix = "test"
    username = generator.generate(prefix=prefix)
    assert username.startswith(prefix.lower())
    
    # Test with different styles
    for style in ["default", "funny", "serious"]:
        username = generator.generate(style=style)
        assert isinstance(username, str)
        assert len(username) > 0

def test_invalid_style(generator):
    """Test that invalid style raises ValueError"""
    with pytest.raises(ValueError):
        generator.generate(style="invalid_style")

def test_username_format(generator):
    """Test username format requirements"""
    username = generator.generate()
    # Username should be lowercase
    assert username.islower()
    # Username should not contain spaces
    assert " " not in username
