import json
import os

DEFAULT_CONFIG_FILENAME = 'config.json'

FALLBACK_DEFAULTS = {
    'module_m': 1.0,
    'teeth_number_z': 18,
    'pressure_angle_alpha': 20.0,
    'offset_factor_x': 0.2,
    'backlash_factor_b': 0.05,
    'addendum_factor_a': 1.0,
    'dedendum_factor_d': 1.25,
    'hob_edge_radius_c': 0.2,
    'tooth_edge_radius_e': 0.1,
    'teeth_number_z2': 36,
    'offset_factor_x2': 0.0,
    'x_0': 0.0,
    'y_0': 0.0,
    'seg_involute': 15,
    'seg_edge_r': 15,
    'seg_root_r': 15,
    'seg_outer': 5,
    'seg_root': 5,
    'working_directory': './result/',
    'current_image_path': 'Result1.png'
}

UI_TO_CALCULATION_MAP = {
    'module_m': 'M',
    'teeth_number_z': 'Z',
    'pressure_angle_alpha': 'ALPHA',
    'offset_factor_x': 'X',
    'backlash_factor_b': 'B',
    'addendum_factor_a': 'A',
    'dedendum_factor_d': 'D',
    'hob_edge_radius_c': 'C',
    'tooth_edge_radius_e': 'E',
    'x_0': 'X_0',
    'y_0': 'Y_0',
    'seg_involute': 'SEG_INVOLUTE',
    'seg_edge_r': 'SEG_EDGE_R',
    'seg_root_r': 'SEG_ROOT_R',
    'seg_outer': 'SEG_OUTER',
    'seg_root': 'SEG_ROOT',
    'teeth_number_z2': 'z2',
    'offset_factor_x2': 'x2'
}

INT_PARAM_KEYS = {
    'Z', 'SEG_INVOLUTE', 'SEG_EDGE_R', 'SEG_ROOT_R', 'SEG_OUTER',
    'SEG_ROOT', 'z2'
}


def get_config_path(filename: str = DEFAULT_CONFIG_FILENAME):
    """Return the absolute path to the application configuration file."""
    package_root = os.path.dirname(os.path.dirname(__file__))
    project_root = os.path.dirname(package_root)
    return os.path.join(project_root, filename)


def load_app_config(path: str = None):
    """Load application configuration data from JSON."""
    config_path = path or get_config_path()
    if not os.path.exists(config_path):
        return {}
    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except (OSError, json.JSONDecodeError):
        return {}


def get_defaults(config_data: dict = None):
    """Return merged default values using configuration data with fallbacks."""
    config = config_data or load_app_config()
    defaults = dict(FALLBACK_DEFAULTS)
    defaults.update(config.get('defaults', {}))
    return defaults


def get_default_calculation_params(config_data: dict = None):
    """Map UI default values to the calculation parameter schema."""
    defaults = get_defaults(config_data)
    calculation_params = {}
    for ui_key, calc_key in UI_TO_CALCULATION_MAP.items():
        if ui_key in defaults:
            calculation_params[calc_key] = defaults[ui_key]

    for key in INT_PARAM_KEYS:
        if key in calculation_params:
            calculation_params[key] = int(calculation_params[key])

    return calculation_params


def get_default_working_directory(config_data: dict = None):
    """Return the default working directory specified in the configuration."""
    defaults = get_defaults(config_data)
    return defaults.get('working_directory', FALLBACK_DEFAULTS['working_directory'])


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