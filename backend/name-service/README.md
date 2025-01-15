# Name Generator Service

A microservice for generating unique and meaningful usernames for new Frame accounts.

## Overview

The Name Generator Service is designed to create memorable usernames by combining adjectives and nouns, optionally adding numbers for uniqueness. It supports different generation styles and can work with custom prefixes.

## Features

- Generate usernames by combining adjectives and nouns
- Support for different styles (default, funny, serious)
- Optional number suffix for increased uniqueness
- Custom prefix support
- RESTful API with FastAPI
- Health check endpoint

## API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy"}
```

### Generate Username
```
POST /generate
Request Body:
{
    "prefix": string | null,    // Optional prefix
    "style": string | "default" // "default", "funny", or "serious"
}

Response:
{
    "username": string
}
```

## Example Usernames

- Default style: `swifteagle123`, `cosmicdragon`
- Funny style: `coolninja42`, `megawarrior777`
- Serious style: `ancientphoenix`, `legendarymaster`
- With prefix: `johntiger123`, `alexdragon`

## Installation

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/MacOS
# or
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

No additional configuration is required. The service runs on port 5001 by default.

## Running the Service

```bash
python run.py
```

The service will start on `http://localhost:5001` with automatic reload enabled for development.

## Development

### Project Structure
```
name-service/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application and endpoints
│   ├── generator.py     # Username generation logic
│   └── word_lists.py    # Word lists for generation
├── requirements.txt     # Project dependencies
└── run.py              # Service entry point
```

### Adding New Words

To extend the vocabulary for username generation, edit the word lists in `app/word_lists.py`:
- `adjectives`: List of descriptive words
- `nouns`: List of object/subject words

## Integration

The service is designed to work with the Frame authentication service. When a new user registers, the auth service can request a username suggestion from this service.

## Future Improvements

1. Word2Vec Integration
   - Implement semantic-based username generation
   - Use pre-trained word embeddings for better word combinations

2. Caching Layer
   - Add Redis cache for frequently requested prefixes
   - Cache recently generated usernames to avoid duplicates

3. Advanced Features
   - Profanity filtering
   - Language-specific username generation
   - Custom word lists for different themes