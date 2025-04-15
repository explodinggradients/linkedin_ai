# linkedin_ai


### Installation

Install latest from the GitHub
[repository](https://github.com/shahules786/linkedin_ai):

``` sh
$ pip install git+https://github.com/shahules786/linkedin_ai.git
```
or 

Clone the repo and install:

``` sh
git clone git@github.com:shahules786/linkedin_ai.git
cd linkedin_ai
pip install -e .
```

### Example Usage

``` python
import os
from linkedin_ai import LinkedinAI

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

my_ai = LinkedinAI.from_bm25(posts="<path to linkiedin posts>")
my_ai.ask("What is the best way to learn Python?")
```

Checkout ![example notebook](/docs/0_example.ipynb)

                        
                        
### Features

[x] BM25 Search
[x] Vector Search
[x] MLFlow Support
