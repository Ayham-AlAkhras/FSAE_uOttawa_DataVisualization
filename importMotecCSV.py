# importMotecCSV.py

import dearpygui.dearpygui as dpg
from motec_importer import MoTeCImporter


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

        # Show the first 5 rows in the text box
        preview_text = df.head().to_string()
        dpg.set_value("preview", preview_text)

    except Exception as e:
        # If anything failed, show the error and clear preview
        dpg.set_value("status", f"Error: {e}")
        dpg.set_value("preview", "")


def main():
    # Required DearPyGui setup
    dpg.create_context()

    # Main window
    with dpg.window(label="MoTeC CSV Importer", tag="main_window"):
        # Button to open file dialog
        dpg.add_button(
            label="Select CSV file",
            callback=lambda: dpg.configure_item("file_dialog", show=True)
        )

        # Status line (empty at start)
        dpg.add_text("", tag="status")

        # Multi-line read-only text box for preview
        dpg.add_input_text(
            tag="preview",
            multiline=True,
            readonly=True,
            width=700,
            height=400
        )

    # Hidden file dialog (pops up when button is pressed)
    with dpg.file_dialog(
        directory_selector=False,
        show=False,
        callback=on_file_selected,
        tag="file_dialog",
        width=600,
        height=400
    ):
        dpg.add_file_extension(".csv", custom_text="[CSV]")
        dpg.add_file_extension(".*")  # allow all files just in case

    # Standard DearPyGui boilerplate to show the window
    dpg.create_viewport(title="MoTeC CSV Importer", width=750, height=550)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.set_primary_window("main_window", True)
    dpg.start_dearpygui()
    dpg.destroy_context()


if __name__ == "__main__":
    main()
