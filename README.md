# AI4Math: Track 03

This project contains various AI models for mathematical problem-solving,
including GPT-4, GPT-4o, LLAMA3, and Claude 3 Opus.

## Project Structure

```
.
├── LICENSE
├── Makefile
├── README.md
├── data/
├── predictions/
│   ├── gpt4/
│   ├── gpt4o/
│   ├── llama3/
│   ├── opus/
│   ├── prediction.json
│   ├── prediction_empty.json
│   └── prediction_final.json
├── requirements.txt
├── src/
│   ├── gpt4.py
│   ├── gpt4o.py
│   ├── llama3.py
│   └── opus.py
├── submission/
│   └── prediction.json
└── utils/
    ├── combine.py
    └── tokens.py
```

## Setup

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository.
3. Run `make install` to create a virtual environment and install the required packages.

## Usage

Use the following make commands to run different parts of the project:

- `make llama3`: Run the LLAMA3 version
- `make gpt4`: Run GPT-4 version
- `make gpt4o`: Run the GPT-4o version
- `make opus`: Run the OPUS version
- `make combine`: Combine predictions (default: test dataset with claude-3-opus model)

## Requirements

See `requirements.txt` for a list of Python packages required for this project.
