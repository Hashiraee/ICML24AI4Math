import io
import json
import os
from contextlib import redirect_stdout
from dotenv import load_dotenv
from openai import OpenAI

DATASET = "test"

SYSTEM_PROMPT="""\
You are GPT4, an AI assistant with expertise in converting textual problem
descriptions into mathematical formulations and Python code. You will receive a
problem description from the user in natural language, enclosed in <problem>
tags like this:

<problem>
{{PROBLEM_DESCRIPTION}}
</problem>

Your task is to respond in the following format:

First, provide the mathematical formulation of the problem in LaTeX, enclosed in a markdown code block and <formulation> tags:

<formulation>
```latex
{{FORMULATION}}
```
</formulation>

Make sure to use:
- (x * 0.5) instead of (x / 2) for division in your LaTeX formulation.
- \leq, \geq, for inequalities insted of \le or \ge.
- For the Python code using the PulP library, use x >= y + 1 instead of x > y (for integer variables).

Next, write Python code to solve the problem using the pulp library, based on
your mathematical formulation. Enclose your code in a Python code block and
<code> tags:

<code>
```python
{{CODE}}
```
</code>

In your code output, ONLY print the items specified in the 'result' key of the
problem description, using the SAME VALUE for the key. For the 'value' of the
'result' key, only output numbers.

To summarize, your complete response should consist ONLY of:

<formulation>
```latex
{{FORMULATION}}
```
</formulation>

<code>
```python
{{CODE}}
```
</code>

Do not include any other text, explanations, or output besides what is specified
above. Think carefully step-by-step to convert the problem into a formulation
and code before providing your response.\
"""


def solve_problem(problem, problem_id):
    problem_description = problem["question"]
    results = problem["results"]

    # Prepare the prompt to send to the LLM
    prompt = f"""\
<problem>
Given the problem:
{problem}

And the required results:
{results}

Provide the solution code in the following format:
<code>
```python
from pulp import *

# Your code here

# Check if an optimal solution was found
if LpStatus[model.status] == 'Optimal':

# From the results dictionary, print the required values without rounding
print(f"key_1: {{value(variable_1)}}")
print(f"key_2: {{value(variable_2)}}")
#...
print(f"key_n: {{value(variable_n)}}")
else:
# If no optimal solution, print 0 for all results
print(f"key_1: 0")
print(f"key_2: 0")
#...
print(f"key_n: 0")
```
</code>
</problem>\
"""

    # Send the prompt to the LLM and get the response
    response = send_to_llm(prompt)

    # Extract the mathematical formulation and Python code from the response
    formulation = extract_formulation(response)
    code = extract_code(response)

    # Write the problem details to the markdown file
    write_to_markdown(problem_id, problem_description, formulation, code)

    # Execute the Python code and get the results
    results = execute_code(code)

    # Update the "results" object with the obtained values
    for key, value in results.items():
        problem["results"][key] = str(value)

    # Save the problem with its results to a separate file
    save_problem_results(problem, problem_id)


def send_to_llm(prompt):
    # Set up the API client
    client = OpenAI()

    # Set the model and other parameters
    MODEL_NAME = "gpt-4o"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.0

    # Create the message history
    solution_message = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": prompt}
    ]

    # Generate the response from the Anthropic API
    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=solution_message,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
    )
    assistant_response = completion.choices[0].message.content
    print(assistant_response)

    return assistant_response


def extract_formulation(response):
    start_tag = "<formulation>"
    end_tag = "</formulation>"
    start_index = response.find(start_tag) + len(start_tag)
    end_index = response.find(end_tag)
    formulation = response[start_index:end_index].strip()
    formulation = formulation.replace("```latex", "").replace("```", "").strip()
    return formulation


def extract_code(response):
    start_tag = "<code>"
    end_tag = "</code>"
    start_index = response.find(start_tag) + len(start_tag)
    end_index = response.find(end_tag)
    code = response[start_index:end_index].strip()
    code = code.replace("```python", "").replace("```", "").strip()
    return code


def execute_code(code):
    # Execute the Python code and capture the printed output
    output = io.StringIO()
    with redirect_stdout(output):
        exec(code, globals())

    # Extract the relevant values from the printed output
    results = {}
    for line in output.getvalue().strip().split("\n"):
        if ":" in line:
            key, value = line.split(":", 1)
            results[key.strip()] = value.strip()
        elif line.startswith("{") and line.endswith("}"):
            # Handle dictionary-like strings
            dictionary = eval(line)
            results.update(dictionary)

    return results


def write_to_markdown(problem_id, question, formulation, code):
    with open(f"data/{DATASET}/solutions_gpt4o/generation.md", "a") as file:
        file.write(f"# id\n{problem_id}\n\n")
        file.write(f"## question\n{question}\n\n")
        file.write(f"## formulation\n```latex\n{formulation}\n```\n\n")
        file.write(f"## code\n```python\n{code}\n```\n---\n")


def save_problem_results(problem, problem_id):
    # Create the directory if it doesn't exist
    os.makedirs(f"data/{DATASET}/problems_gpt4o", exist_ok=True)

    # Save the problem with its results to a separate file
    filename = f"data/{DATASET}/problems_gpt4o/prediction_{problem_id:03d}.json"
    with open(filename, "w") as file:
        json.dump(problem, file, indent=4)


def main():
    # Load environment variables
    load_dotenv()

    # Read the JSON data from the file
    with open(f"data/{DATASET}/task3_{DATASET}_public.json", "r") as file:
        data = json.load(file)

    # Iterate over each problem
    for i, problem in enumerate(data):
        # Check if the prediction file already exists
        prediction_file = f"data/{DATASET}/problems_gpt4o/prediction_{i:03d}.json"
        if os.path.exists(prediction_file):
            print(f"Skipping problem {i} - already solved.")
        else:
            solve_problem(problem, i)


if __name__ == "__main__":
    main()

