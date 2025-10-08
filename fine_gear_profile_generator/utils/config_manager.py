import json
import os

def save_params(working_dir, params_dict):
    """
    Saves a dictionary of parameters to Inputs.dat in the specified directory.

    Args:
        working_dir (str): The directory where the file will be saved.
        params_dict (dict): A dictionary containing the parameters to save.
                            Keys are parameter names, values are the values.
    """
    os.makedirs(working_dir, exist_ok=True)
    filepath = os.path.join(working_dir, 'Inputs.dat')
    try:
        with open(filepath, 'w') as f:
            json.dump(params_dict, f, indent=4)
        return True, f"Parameters saved to {filepath}"
    except Exception as e:
        return False, f"Error saving parameters: {e}"

def load_params(working_dir):
    """
    Loads parameters from Inputs.dat in the specified directory.

    Args:
        working_dir (str): The directory from which to load the file.

    Returns:
        A tuple (success, data_or_error_message).
        If successful, (True, dict_of_parameters).
        If failed, (False, error_message_string).
    """
    filepath = os.path.join(working_dir, 'Inputs.dat')
    if not os.path.exists(filepath):
        return False, f"File not found: {filepath}"

    try:
        with open(filepath, 'r') as f:
            loaded_data = json.load(f)
        return True, loaded_data
    except json.JSONDecodeError:
        return False, f"Error: The file {filepath} is not a valid JSON file."
    except Exception as e:
        return False, f"Failed to load parameters: {e}"