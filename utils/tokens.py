import sys
import tiktoken


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    """Returns the number of tokens in a text string."""
    encoding = tiktoken.get_encoding(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 tokens.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]

    # Specify the correct encoding for your file.
    file_encoding = "utf-8"

    try:
        with open(file_name, "r", encoding=file_encoding) as file:
            content = file.read()
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        sys.exit(1)
    except UnicodeDecodeError as e:
        print(f"Error reading file: {e}")
        print("Check if the file encoding is correct.")
        sys.exit(1)

    num_tokens = num_tokens_from_string(content, "cl100k_base")
    print(f"Number of tokens: {num_tokens}")


if __name__ == "__main__":
    main()
