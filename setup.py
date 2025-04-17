from setuptools import setup, find_packages

setup(
    name="linkedin_ai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai",
        "mlflow",
        "numpy",
        "rank_bm25",
        "jinja2",
        "mlflow==3.0.0rc0",
        "ragas_experimental",
        "ipykernel",
    ],
    author="Shahul Es",
    author_email="shahules786@gmail.com",
    description="A tool for LinkedIn data analysis with AI capabilities",
    keywords="linkedin, ai, data analysis",
    url="https://github.com/shahules786/linkedin_ai",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)