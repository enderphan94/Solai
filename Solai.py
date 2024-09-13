import os
import subprocess
import sys
import re
import openai
import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()


# Set up your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')



def install_tools():
    tools = ["solc-select", "solc", "slither", "cspell"]
    for tool in tools:
        if not is_tool_installed(tool):
            install_tool(tool)


def is_tool_installed(tool):
    try:
        if tool == "solc-select":
            subprocess.check_output(["solc-select", "--help"], stderr=subprocess.STDOUT)
        else:
            subprocess.check_output([tool, "--version"], stderr=subprocess.STDOUT)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def install_tool(tool):
    if tool == "solc":
        print("Installing solc...")
        os.system("brew update && brew tap ethereum/ethereum && brew install solidity")
    elif tool == "solc-select":
        print("Installing solc-select...")
        os.system("brew install solc-select")
    elif tool == "slither":
        print("Installing slither...")
        os.system("pip3 install slither-analyzer")
    elif tool == "cspell":
        print("Installing cspell...")
        os.system("npm install -g cspell")
    else:
        print(f"Please install {tool} manually.")


def extract_solidity_version(contract_file):
    with open(contract_file, 'r') as file:
        content = file.read()

    match = re.search(r'pragma\s+solidity\s+\^?(\d+\.\d+\.\d+);', content)
    if match:
        return match.group(1)
    else:
        print("Solidity version not found in the contract. Defaulting to version 0.8.0.")
        return "0.8.0"


def use_solidity_version(version):
    os.system(f"solc-select install {version}")
    os.system(f"solc-select use {version}")


def flatten_contract(contract_file, flattened_file):
    with open(flattened_file, 'w') as outfile:
        with open(contract_file, 'r') as infile:
            outfile.write(infile.read())


def compile_contract(flattened_file):
    command = f"solc --optimize --bin {flattened_file}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Compilation failed with output:\n{result.stderr}")
        sys.exit(1)
    else:
        print(f"Compilation output:\n{result.stdout}")


def run_slither(flattened_file):
    command = f"slither {flattened_file} --json slither_output.json"
    subprocess.run(command, shell=True, check=True)


def run_cspell(flattened_file):
    command = f"cspell {flattened_file} --output cspell_output.txt"
    subprocess.run(command, shell=True, check=True)


def analyze_with_gpt4(flattened_file, slither_results, cspell_results):
    with open(flattened_file, 'r') as file:
        contract_content = file.read()

    system_prompt = (
        "You are an expert in Solidity auditing. Review the given Solidity code for known vulnerabilities, best practices, and spelling errors. "
        "Also review the results from Slither and Cspell. Provide a JSON output with the following fields:\n"
        "1. Issue name\n2. Severity level\n3. Impact of the vulnerability\n4. The vulnerable code snippet\n5. Mitigation solution"
    )

    user_prompt_correct = "Analyze the following Solidity code and combine it with results from Slither and Cspell:"

    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"{user_prompt_correct}\nSolidity Contract:\n{contract_content}\n\nSlither Results:\n{slither_results}\n\nCspell Results:\n{cspell_results}\n"}
        ],
        n=1,
        stop=None,
        temperature=0.7,
        response_format={"type": "json_object"},
        max_tokens=10000
    )

    report_json = json.loads(response['choices'][0]['message']['content'].strip())
    return report_json


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 audit.py <path_to_solidity_file>")
        sys.exit(1)

    contract_file = sys.argv[1]

    if not os.path.isfile(contract_file):
        print(f"File {contract_file} does not exist.")
        sys.exit(1)

    flattened_file = "flattened.sol"

    install_tools()

    print("Extracting Solidity version...")
    solc_version = extract_solidity_version(contract_file)
    print(f"Using Solidity version {solc_version}...")

    use_solidity_version(solc_version)

    print("Flattening contract...")
    flatten_contract(contract_file, flattened_file)

    print("Compiling contract...")
    compile_contract(flattened_file)

    print("Running Slither for vulnerabilities and best practices...")
    try:
        run_slither(flattened_file)
    except subprocess.CalledProcessError as e:
        print(f"Slither failed with error: {e}")

    print("Checking for spelling errors...")
    run_cspell(flattened_file)

    print("Analyzing with GPT-4 for comprehensive audit...")
    # Read slither and cspell results
    slither_results = ""
    cspell_results = ""

    if os.path.exists("slither_output.json"):
        with open("slither_output.json", 'r') as file:
            slither_results = file.read()
    if os.path.exists("cspell_output.txt"):
        with open("cspell_output.txt", 'r') as file:
            cspell_results = file.read()

    final_results = analyze_with_gpt4(flattened_file, slither_results, cspell_results)

    # Save final results to a JSON file
    with open("final_audit_results.json", "w") as outfile:
        json.dump(final_results, outfile, indent=4)

    print("Audit completed. Results saved in final_audit_results.json")


if __name__ == "__main__":
    main()