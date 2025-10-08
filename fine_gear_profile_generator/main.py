import argparse
import sys
import tkinter as tk
import os

# By using relative imports, we treat this project as a package.
# This script should be run as a module from the parent directory, e.g.:
# python -m fine_gear_profile_generator.main
try:
    from .gui.fgpg_gui import GearApp
    # In the future, headless mode would import from .core, .io, etc.
except ImportError:
    print("Error: Failed to import application modules.", file=sys.stderr)
    print("Please run this script as a module from the project's parent directory.", file=sys.stderr)
    print("Example: python -m fine_gear_profile_generator.main", file=sys.stderr)
    sys.exit(1)

def run_headless_mode():
    """
    Runs the gear generation process with a default set of parameters,
    saving the output files without launching the GUI.
    """
    print("Running in headless mode with default parameters...")

    # Default parameters, similar to the original script
    params = {
        'M': 1.0, 'Z': 18, 'ALPHA': 20.0, 'X': 0.2, 'B': 0.05, 'A': 1.0,
        'D': 1.25, 'C': 0.2, 'E': 0.1, 'X_0': 0.0, 'Y_0': 0.0,
        'SEG_INVOLUTE': 15, 'SEG_EDGE_R': 15, 'SEG_ROOT_R': 15,
        'SEG_OUTER': 5, 'SEG_ROOT': 5,
        'z2': 36, 'x2': 0.0
    }

    # Define the output directory relative to the project root
    working_dir = os.path.join(os.path.dirname(__file__), 'result')
    os.makedirs(working_dir, exist_ok=True)

    try:
        from .core import gear_math, geometry_generator
        from .io import dxf_exporter, image_exporter

        # --- Perform Calculations ---
        contact_ratio, center_dist = gear_math.calculate_contact_ratio(
            params['M'], params['Z'], params['z2'], params['X'], params['x2'], params['ALPHA'], params['A'])

        # --- Generate Geometry ---
        gear1_profile = geometry_generator.generate_tooth_profile(
            params['M'], params['Z'], params['ALPHA'], params['X'], params['B'],
            params['A'], params['D'], params['C'], params['E'],
            params['SEG_INVOLUTE'], params['SEG_EDGE_R'], params['SEG_ROOT_R'],
            params['SEG_OUTER'], params['SEG_ROOT'])

        gear2_profile = geometry_generator.generate_tooth_profile(
            params['M'], params['z2'], params['ALPHA'], params['x2'], params['B'],
            params['A'], params['D'], params['C'], params['E'],
            params['SEG_INVOLUTE'], params['SEG_EDGE_R'], params['SEG_ROOT_R'],
            params['SEG_OUTER'], params['SEG_ROOT'])

        # --- Export Files ---
        image_exporter.export_gear_pair_to_image(
            working_dir, gear1_profile, gear2_profile, center_dist,
            params['M'], params['Z'], params['z2'], params['X_0'], params['Y_0'])

        dxf_exporter.export_gear_pair_to_dxf(
            working_dir, gear1_profile, gear2_profile, center_dist,
            params['X_0'], params['Y_0'])

        print(f"Headless run complete. Files saved in {working_dir}")

    except Exception as e:
        print(f"An error occurred during the headless run: {e}", file=sys.stderr)
        sys.exit(1)

def main():
    """
    Main entry point for the application.
    Parses command-line arguments to decide whether to run the GUI
    or a command-line version of the tool.
    """
    parser = argparse.ArgumentParser(
        description="A fine gear profile generator for spur and internal gears."
    )
    parser.add_argument(
        '--headless',
        action='store_true',
        help='Run the application in headless mode without a GUI.'
    )
    # Future arguments for headless mode would be defined here.
    # e.g., parser.add_argument('--module', type=float, help='Set the gear module.')

    args = parser.parse_args()

    if args.headless:
        run_headless_mode()
    else:
        # Launch the GUI application
        try:
            app = GearApp()
            app.mainloop()
        except tk.TclError as e:
            print(f"Error: Could not start the GUI. This may be because no display is available.", file=sys.stderr)
            print(f"({e})", file=sys.stderr)
            print("You can try running in headless mode with the --headless flag.", file=sys.stderr)
            sys.exit(1)

if __name__ == '__main__':
    main()