# linkedin_ai


### Installation

Install latest from the GitHub
[repository](https://github.com/shahules786/linkedin_ai):

``` sh
$ pip install git+https://github.com/shahules786/linkedin_ai.git
```

or from [conda](https://anaconda.org/shahules786/linkedin_ai)

``` sh
$ conda install -c shahules786 linkedin_ai
```

or from [pypi](https://pypi.org/project/linkedin_ai/)

``` sh
$ pip install linkedin_ai
```

### Usage

``` python
import os
from linkedin_ai import LinkedInAI

os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_API_KEY"

my_ai = LinkedInAI.from_bm25(posts="<path to linkiedin posts>")
my_ai.ask("What is the best way to learn Python?")
```


                        
                        

