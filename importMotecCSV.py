# importMotecCSV.py

import dearpygui.dearpygui as dpg
from motec_importer import MoTeCImporter
from pathlib import Path

def on_file_selected(sender, app_data):
    """
    Called automatically when the user picks a file in the file dialog.
    """

    # Full path to the file the user selected
    file_path = app_data["file_path_name"]

    try:
        # Use the existing class you were given
        importer = MoTeCImporter(file_path)

        # This runs load() + validations and returns the DataFrame
        df = importer.import_and_validate()

        # If we got here, it worked
        dpg.set_value("status", "Import successful")
        dpg.show_item("status")

        meta_lines = [f"{k}: {v}" for k, v in importer.metadata.items() if v]
        dpg.set_value("metadata_box", "\n".join(meta_lines))

        preview_text = df.to_string()
        dpg.set_value("preview", preview_text)

    except Exception as e:
        # If anything failed, show the error and clear preview
        dpg.set_value("status", f"Error: {e}")
        dpg.show_item("status")
        dpg.set_value("preview", "")
        dpg.set_value("metadata_box", "")

def verify_loader_integrity():
    """Verifies that the MoTeCImporter can load all CSV files in the debugging_files folder."""
    
    # Reset status and display loading message
    dpg.set_value("status", "Verifying loader integrity...")
    dpg.show_item("status")
    dpg.set_value("metadata_box", "")
    dpg.set_value("preview", "")
    
    GLOBAL_FOLDER = Path(__file__).resolve().parent / "debugging_files"
    files = [str(p) for p in GLOBAL_FOLDER.rglob("*.csv")]
    
    for file in files[:-4]: # The last 4 are intentionally broken files (for testing)
        try:
            file_importer = MoTeCImporter(file)
            file_importer.import_and_validate()
        except Exception as e:
            print(f"[DEBUG] Loader integrity check failed for {file}: {e}")
            dpg.set_value("status", f"Loader integrity check failed for {file}: {e}")
            dpg.show_item("status")
            return
    
    print("[DEBUG] Loader integrity check passed for all files.")
    dpg.set_value("status", "Loader integrity check passed for all files.")

def main():
    """Main function to set up the DearPyGui interface."""
    
    # Required DearPyGui setup
    dpg.create_context()

    # Main window
    with dpg.window(label="MoTeC CSV Importer", tag="main_window"):

        with dpg.group(horizontal=True):
            # Button to open file dialog
            dpg.add_button(
                label="Select CSV file",
                callback=lambda: dpg.configure_item("file_dialog", show=True)
            )
            
            # Button to verify that the loader is working
            dpg.add_button(
                label="Verify loader integrity",
                callback=verify_loader_integrity
            )
            
        # Status line (empty at start)
        dpg.add_text("", tag="status", wrap=750, show=False)
        
        # Metadata
        dpg.add_text("Metadata")
        dpg.add_input_text(
            tag="metadata_box",
            multiline=True,
            readonly=True,
            width=750,
            height=100
        )
        
        # Data preview
        dpg.add_text("Data")
        dpg.add_input_text(
            tag="preview",
            multiline=True,
            readonly=True,
            width=750,
            height=400
        )

    # Hidden file dialog (pops up when button is pressed)
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=on_file_selected,
        tag="file_dialog",
        width=750,
        height=400
    ):
        dpg.add_file_extension(".csv", custom_text="[CSV]")
        dpg.add_file_extension(".*")  # allow all files just in case

    # Standard DearPyGui boilerplate to show the window
    dpg.create_viewport(title="MoTeC CSV Importer", width=800, height=550)
    dpg.set_exit_callback(dpg.stop_dearpygui)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()