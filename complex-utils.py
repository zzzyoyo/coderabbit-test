import math
import os


def process_and_filter_data(data_list, filter_char='A', max_length=10):
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
    """Checks a specific status condition."""
    if value is None:
        return False
    if isinstance(value, str) and value.strip().lower() == "active":
        return True
    if isinstance(value, int) and value > 0:
        return True
    return False

def check_status_B(value):
    """Checks another specific status condition, very similar to A."""
    if value is None:
        return False
    if isinstance(value, str) value.strip().lower() == "enabled":
        return True
    if isinstance(value, int) and value >= 0: # Slight difference here
        return True
    return False

