# LinkedIn AI: 
Build Your Own AI Assistant powered by LinkedIn Content

This hackathon repository provides you with the foundation to build an AI assistant that can answer questions based on LinkedIn content. The system uses RAG (Retrieval-Augmented Generation) to provide responses that matchs knowledge of the content author.

## 🚀 Getting Started: Installation

### Option 1: Install directly from GitHub

```
bashpip install git+https://github.com/shahules786/linkedin_ai.git
```

This command downloads and installs the package directly from the GitHub repository. It gives you the latest version without needing to clone the repo locally.

### Option 2: Clone and install locally
```
bashgit clone git@github.com:shahules786/linkedin_ai.git
cd linkedin_ai
pip install -e .
```
This approach clones the repository to your local machine, then installs it in "editable" mode (the -e flag). This allows you to make changes to the code and have them take effect immediately without reinstalling.#

## Quick Example
```py
import os
from linkedin_ai import LinkedinAI

# Set your OpenAI API key in environment variables for security
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

# Create an instance using BM25 retrieval with your LinkedIn data
my_ai = LinkedinAI.from_bm25(posts="path/to/your/linkedin_posts.json")

# Ask questions to your AI assistant
response = my_ai.ask("What is the best way to learn Python?")
print(response)
```

This code initializes a LinkedIn AI assistant that leverages the BM25 algorithm to find relevant content in your LinkedIn posts before generating a response. The response will match the style of the original content.

## Your Hackathon Journey
### Step 1: Explore the Basics
Start by checking out the [example notebook](docs/0_example.ipynb) to understand how the core functionality works. This will introduce you to:

- How to load LinkedIn post data
- How to initialize the AI assistant
- How to ask questions and get responses

### Step 2: Run Your First Experiment
Move on to the [experiment notebook](docs/01_experiment.ipynb) where you'll learn:

- How to create test datasets
- How to set up LLM-based evaluation metrics
- How to run and track experiments systematically
- How to compare different approaches

## Key Features

✅ BM25 Search: Uses the BM25 algorithm for fast keyword-based retrieval  
✅ Vector Search: Supports semantic search using embeddings  
✅ MLFlow Integration: Built-in experiment tracking and logging

