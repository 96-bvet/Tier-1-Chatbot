# Testing Instructions

## Installation

### For development and testing:

```bash
# Clone the repository
git clone https://github.com/96-bvet/Tier-1-Chatbot.git
cd Tier-1-Chatbot

# Install the package in development mode
pip install -e .

# Install development dependencies
pip install -r requirements-dev.txt
```

### For production:

```bash
pip install -e .
```

## Running Tests

### Run all tests:
```bash
pytest
```

### Run tests with coverage:
```bash
pytest --cov=tier1_chatbot --cov-report=html --cov-report=term
```

### Run specific test file:
```bash
pytest tests/test_chatbot.py
```

### Run specific test:
```bash
pytest tests/test_chatbot.py::TestKnowledgeBase::test_check_knowledge_base_password_reset
```

## Running the Application

### Using the command-line entry point:
```bash
tier1-chatbot
```

### Or using Python module:
```bash
python -m tier1_chatbot.chatbot
```

## Environment Variables

Before running the application, set these environment variables:

```bash
export OPENAI_API_KEY="your-openai-api-key"
export SYNCRO_SUBDOMAIN="your-syncro-subdomain"
export SYNCRO_API_KEY="your-syncro-api-key"
export SERP_API_KEY="your-serp-api-key"  # Optional

# For development only - enables Flask debug mode
export FLASK_DEBUG="true"  # Optional, defaults to false for security
```

## Package Structure

```
Tier-1-Chatbot/
├── src/
│   └── tier1_chatbot/
│       ├── __init__.py
│       └── chatbot.py
├── tests/
│   ├── conftest.py
│   └── test_chatbot.py
├── setup.py
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── MANIFEST.in
└── .gitignore
```

## Building and Distribution

### Build source distribution:
```bash
python setup.py sdist
```

### Build wheel distribution:
```bash
pip install wheel
python setup.py bdist_wheel
```

### Install from local build:
```bash
pip install dist/tier1-chatbot-0.1.0.tar.gz
```
