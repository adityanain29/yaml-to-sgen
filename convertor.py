import yaml
import sys
import argparse

def singularize(word: str) -> str:
    """
    A simple function to singularize a word by removing a trailing 's'.
    This is a naive implementation sufficient for the example's semantics.
    """
    if word.lower().endswith('s'):
        return word[:-1]
    return word

def transform_to_sexp_structure(data):
    """
    Recursively transforms a Python object (from YAML) into a nested
    list structure suitable for S-expression formatting.
    """
    if data is None:
        return 'nil'
    if isinstance(data, dict):
        sexp_list = []
        for key, value in data.items():
            # Apply the special rule for lists/arrays
            if isinstance(value, list):
                singular_key = singularize(key)
                list_items = [ [singular_key, transform_to_sexp_structure(item)] for item in value ]
                sexp_list.append([key, *list_items])
            else:
                sexp_list.append([key, transform_to_sexp_structure(value)])
        return sexp_list
    if isinstance(data, list):
        # This handles lists that are not under a dictionary key (less common in YAML docs)
        return [transform_to_sexp_structure(item) for item in data]
    if isinstance(data, str):
        # Enclose strings in double quotes
        return f'"{data}"'
    # Numbers and booleans are returned as is
    return data

def format_sexp(sexp, indent: int = 0) -> str:
    """
    Recursively formats a nested list structure into a pretty-printed
    S-expression string.
    """
    if not isinstance(sexp, list):
        return str(sexp)

    indent_str = "  " * indent
    next_indent_str = "  " * (indent + 1)

    # Simple, single-line list: (key value)
    if len(sexp) == 2 and not isinstance(sexp[1], list):
        return f"({sexp[0]} {format_sexp(sexp[1])})"

    # Multi-line list
    parts = [f"({sexp[0]}"]
    for item in sexp[1:]:
        parts.append(next_indent_str + format_sexp(item, indent + 1))
    parts.append(indent_str + ")")

    return "\n".join(parts)


def main():
    """
    Main function to parse arguments, read files, perform conversion,
    and write output.
    """
    parser = argparse.ArgumentParser(
        description="Convert a YAML file to an S-expression.",
        epilog="If no output file is specified, the result is printed to standard output."
    )
    parser.add_argument("input_file", help="The path to the source YAML file.")
    parser.add_argument("output_file", nargs='?', default=None, help="(Optional) The path to the output S-expression file.")
    
    args = parser.parse_args()

    try:
        with open(args.input_file, 'r') as f:
            yaml_data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Input file not found at '{args.input_file}'", file=sys.stderr)
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error: Could not parse YAML file '{args.input_file}'.", file=sys.stderr)
        print(f"Details: {e}", file=sys.stderr)
        sys.exit(1)

    if not yaml_data:
        print("Warning: Input YAML file is empty or contains only null values.", file=sys.stderr)
        output_content = "(nil)"
    else:
        sexp_structure = transform_to_sexp_structure(yaml_data)
        
        # The top-level result is a list of lists, so we format it as a single block
        output_lines = ["("]
        for item in sexp_structure:
            output_lines.append("  " + format_sexp(item, 1))
        output_lines.append(")")
        output_content = "\n".join(output_lines)

    if args.output_file:
        try:
            with open(args.output_file, 'w') as f:
                f.write(output_content + "\n")
            print(f"✅ Successfully converted '{args.input_file}' to '{args.output_file}'.")
        except IOError as e:
            print(f"Error: Could not write to output file '{args.output_file}'.", file=sys.stderr)
            print(f"Details: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        print(output_content)


if __name__ == "__main__":
    main()