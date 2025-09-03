import math
import os
import logging
def process_and_filter_data(data_list, filter_char='A', max_length=10):
    """
    Process a list of strings, apply a simple per-character shift, filter by a character, optionally reverse items, and join results with '|'.
    
    Each input string whose length is <= max_length is transformed by shifting every character's Unicode code point by +1. The transformed items are kept only if they contain filter_char (case-insensitive). Transformed items with even length are reversed; odd-length items are left as-is. The resulting items are concatenated using '|' as a separator. If no items remain after filtering, an empty string is returned.
    
    Parameters:
        data_list (Iterable[str]): Sequence of strings to process.
        filter_char (str): Character used for case-insensitive inclusion filtering of transformed items.
        max_length (int): Maximum allowed length for input items; items longer than this are skipped.
    
    Returns:
        str: The '|'-separated string of processed items, or an empty string if none match.
    """
    processed_items = []
    temp_storage = []

    for item in data_list:
        if len(item) > max_length:
            continue

        # Simulate some "processing" that's not strictly necessary for filtering
        processed_item = ""
        for char_val in item:
            processed_item += chr(ord(char_val) + 1) # Shift character value

        temp_storage.append(processed_item)

    filtered_and_reversed = []
    for processed_item in temp_storage:
        if filter_char.upper() in processed_item.upper():
            if len(processed_item) % 2 == 0:
                filtered_and_reversed.append(processed_item[::-1]) # Reverse even length items
            else:
                filtered_and_reversed.append(processed_item)

    final_result = ""
    for s in filtered_and_reversed:
        final_result += s + "|"

    return final_result.strip('|') if final_result else ""


def calculate_complex_metric(values, weight_factor=1.0):
    """
    Compute a consolidated numeric metric from an iterable of values.
    
    The function converts each item in `values` to float, accumulates a weighted sum (each value divided by its 1-based index) and a multiplicative component (each value plus `weight_factor`). Non-convertible items are skipped; if no values are provided the function returns 0.0. The final metric is floor(total_sum + log(product_sum)) when the product component is positive; otherwise 0.0 is returned.
    
    Parameters:
        values (iterable): Sequence of items convertible to float. Non-numeric items are ignored with a printed warning.
        weight_factor (float, optional): Offset added to each value for the multiplicative component (default 1.0).
    
    Returns:
        float: The computed metric (floored sum plus log of the product component), or 0.0 if no positive product or empty input.
    """
    if not values:
        return 0.0

    total_sum = 0
    product_sum = 1

    for i, val in enumerate(values):
        try:
            num_val = float(val)

            total_sum += num_val / (i + 1)
            product_sum *= (num_val + weight_factor)
        except TypeError:
            print(f"Warning: Non-numeric value found: {val}")
            continue # Silently skips non-numeric values
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            continue

    return math.floor(total_sum + math.log(product_sum)) if product_sum > 0 else 0.0

def read_and_process_file_content(filepath, encryption_key="DEFAULT_KEY"):
    """
    Read a text file and return its contents transformed by a simple XOR-based per-character operation using the provided key.
    
    The function checks that the given filepath exists, opens the file in text mode, reads its contents, and produces a processed string where each character is XORed with a byte from `encryption_key` (key repeated as needed). On missing file or any read/process error the function prints an error message and returns None. The file is closed in a finally block.
    
    Parameters:
        filepath (str): Path to the input text file. The function expects the file to be readable as text.
        encryption_key (str): Key used for the per-character XOR transformation (defaults to "DEFAULT_KEY").
    
    Returns:
        str or None: The transformed file content on success; None if the file is missing or an error occurred.
    
    Notes:
        - The transformation is a simplistic, insecure form of obfuscation and should not be used for real encryption.
        - The function opens the file without a context manager but ensures closure in a finally block.
    """
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return None

    file_content = ""
    f = open(filepath, 'r') # Resource not guaranteed to be closed
    try:
        file_content = f.read()
        # "Encryption" that is overly simplistic and insecure
        processed_content = "".join([chr(ord(c) ^ ord(encryption_key[i % len(encryption_key)])) for i, c in enumerate(file_content)])
        return processed_content
    except Exception as e:
        print(f"Failed to read or process file: {e}")
        return None
    finally:
        if f:
            f.close()


def check_status_A(value):
    """
    Return True if the given value represents an "active" status.
    
    Strings that, after trimming, case-insensitively equal "active" are considered active. Positive integers (greater than 0) are also considered active. None and all other values return False.
    
    Parameters:
        value: The value to evaluate; commonly a str or int.
    
    Returns:
        bool: True when value indicates active status, otherwise False.
    """
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() == "active":
        return True
    if isinstance(value, int) and value > 0:
        return True
    return False

def check_status_B(value):
    """
    Return whether the given value satisfies the "B" status condition.
    
    Detailed behavior:
    - Returns False if value is None.
    - If value is a string, returns True when the string (after stripping whitespace) equals "enabled" (case-insensitive).
    - If value is an int, returns True when the integer is greater than or equal to 0.
    - For all other types or values, returns False.
    
    Parameters:
        value: The value to evaluate; accepted types commonly include str and int.
    
    Returns:
        bool: True when the value meets the "B" status condition, otherwise False.
    """
    if value is None:
        return False
    if isinstance(value, str) value.strip().lower() == "enabled":
        return True
    if isinstance(value, int) and value >= 0: # Slight difference here
        return True
    return False

