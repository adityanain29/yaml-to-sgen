# SAIL to CGEN: YAML to S-Expression Converter

This project provides a command-line tool to convert structured data from YAML format into S-expressions (Symbolic Expressions), as used in Lisp-family languages. This serves as a practical solution to the "SAIL to CGEN" coding challenge.

The tool is written in Python and uses the `PyYAML` library for robust YAML parsing.

## Table of Contents

1.  [Overview](#overview)
2.  [Conversion Semantics (Rules)](#conversion-semantics-rules)
3.  [Requirements](#requirements)
4.  [Setup](#setup)
5.  [Usage](#usage)
6.  [Example](#example)

---

### Overview

The goal is to transform a hierarchical data structure (like a YAML file) into a nested list format that is syntactically correct for S-expressions. The script reads a YAML file, parses it into an internal Python data structure, and then recursively transforms that structure into a formatted S-expression string.

**Key Features:**
-   Handles nested objects, lists, strings, numbers, and null values.
-   Provides clear, indented output for readability.
-   Includes error handling for invalid YAML files.
-   Operates as a standard command-line interface (CLI) tool.

---

### Conversion Semantics (Rules)

The transformation from YAML to S-expressions follows a well-defined set of rules:

1.  **Key-Value Pairs**: Each key-value pair `key: value` becomes a two-element list `(key value)`.

2.  **Objects (Maps)**: A YAML object is converted into a list of the key-value lists it contains. The parent key wraps this list.
    ```yaml
    customer:
      name: "Dorothy"
    ```
    becomes: `(customer (name "Dorothy"))`

3.  **Lists (Arrays)**: A YAML list under a key like `items` is transformed into a parent list. Each element in the YAML list is wrapped in its own list, using a **singularized** version of the parent key (e.g., `items` -> `item`).
    ```yaml
    items:
      - part_no: A4786
      - part_no: E1628
    ```
    becomes: `(items (item (part_no "A4786")) (item (part_no "E1628")))`

4.  **Data Types**:
    -   **Strings**: Are enclosed in double quotes (`"`).
    -   **Numbers**: Are represented directly without quotes.
    -   **Nulls**: `null` or empty values are converted to `nil`.

---

### Requirements

-   Python 3.6+
-   PyYAML

---

### Setup

1.  **Clone or download the project files.**

2.  **Install the required `PyYAML` library:**
    ```bash
    pip install PyYAML
    ```

---

### Usage

Run the script from your terminal, providing the path to the input YAML file as the first argument. You can optionally specify an output file as the second argument.

**Syntax:**
```bash
python converter.py <input_yaml_file> [output_sexp_file]
```

-   `<input_yaml_file>`: (Required) The path to the source YAML file.
-   `[output_sexp_file]`: (Optional) The path to save the output. If omitted, the S-expression will be printed directly to the console.

---

### Example

1.  Create an example YAML file named `invoice.yaml`:

    ```yaml
    # invoice.yaml
    receipt: "Oz-Ware Purchase Invoice"
    date: 2012-08-06
    customer:
        first_name: "Dorothy"
        family_name: "Gale"
    items:
        - part_no: 'A4786'
          descrip: "Water Bucket (Filled)"
          price: 1.47
          quantity: 4
        - part_no: 'E1628'
          descrip: "High Heeled \"Ruby\" Slippers"
          size: 8
          price: 133.7
          quantity: 1
    special_delivery: null
    ```

2.  **Run the converter to print to the console:**

    ```bash
    python converter.py invoice.yaml
    ```

3.  **Run the converter to save to a file:**

    ```bash
    python converter.py invoice.yaml output.sx
    ```

**Expected Output (`output.sx` or console):**
```lisp
(
  (receipt "Oz-Ware Purchase Invoice")
  (date "2012-08-06")
  (customer
    (first_name "Dorothy")
    (family_name "Gale")
  )
  (items
    (item
      (part_no "A4786")
      (descrip "Water Bucket (Filled)")
      (price 1.47)
      (quantity 4)
    )
    (item
      (part_no "E1628")
      (descrip "High Heeled \"Ruby\" Slippers")
      (size 8)
      (price 133.7)
      (quantity 1)
    )
  )
  (special_delivery nil)
)
```
