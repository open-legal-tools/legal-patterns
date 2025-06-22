from setuptools import setup, find_packages

setup(
    name="legal-patterns",
    version="1.0.0",
    author="Open Legal Tools",
    description="Shared patterns and utilities for legal document processing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/open-legal-tools/legal-patterns",
    py_modules=["legal_patterns"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Legal Industry",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ]
    },
)