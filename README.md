# Solidity Smart Contract Auditor

This repository contains a Solidity smart contract auditing script that utilizes various tools such as `Slither`, `cspell`, `Mythril`, and OpenAI's GPT-4 to perform comprehensive analysis and identify vulnerabilities.

## Features

- **Solidity Version Management**: Automatically detects and uses the appropriate Solidity compiler version.
- **Code Flattening**: Flattens Solidity contracts for analysis.
- **Static Analysis**: Uses `Slither`  to analyze smart contract security.
- **Spelling Check**: Uses `cspell` to check coding spelling errors.
- **AI-Powered Analysis**: Integrates OpenAI's GPT-4 to provide additional insights and combine results from other tools.

## TODO

- Add other scanning tools

## Prerequisites

Ensure you have the following installed on your system:

- [Python 3.x](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)
- [npm](https://www.npmjs.com/get-npm)

## Installation

### macOS

1. Clone this repository:

    ```sh
    git clone https://github.com/yourusername/solidity-auditor.git
    cd solidity-auditor
    ```

2. Run the installation script for macOS:

    ```sh
    chmod +x install_tools_macos.sh
    ./install_tools_macos.sh
    ```

### Ubuntu

1. Clone this repository:

    ```sh
    git clone https://github.com/yourusername/solidity-auditor.git
    cd solidity-auditor
    ```

2. Run the installation script for Ubuntu:

    ```sh
    chmod +x install_tools_ubuntu.sh
    ./install_tools_ubuntu.sh
    ```

## Configuration

Update the `OPENAI_API_KEY` value in `main.py` with your OpenAI API key:

```python
# Set up your OpenAI API key
OPENAI_API_KEY = "your_openai_api_key_here"
openai.api_key = OPENAI_API_KEY