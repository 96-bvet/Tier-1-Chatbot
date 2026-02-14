from setuptools import setup, find_packages

with open("README_Version2.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="tier1-chatbot",
    version="0.1.0",
    author="96-bvet",
    description="A tier 1 support chatbot designed to reduce frivolous tickets for tier 2 technicians",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/96-bvet/Tier-1-Chatbot",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-flask>=1.2.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "tier1-chatbot=tier1_chatbot.chatbot:main",
        ],
    },
)
