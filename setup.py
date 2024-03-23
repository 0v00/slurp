from setuptools import setup, find_packages

setup(
    name="slurp",
    version="1.0.0",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "toml",
        "requests",
        "beautifulsoup4",
        "anthropic",
        "openai",
        "scikit-learn",
        "sentence-transformers",
    ],
    extras_require={
        "dev": ["ruff"],
    },
    entry_points={"console_scripts": ["slurp=cli:main"]},
)
