import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import customtkinter as ctk
from CTkColorPicker import AskColor, CTkColorPicker


def open_modal_picker():
    picker = AskColor()
    color = picker.get()
    if color:
        modal_swatch.configure(fg_color=color)


def update_embedded_picker(color: str):
    embedded_swatch.configure(fg_color=color)


if __name__ == "__main__":
    ctk.set_appearance_mode("system")

    root = ctk.CTk()
    root.title("CTkColorPicker Demo")

    # Modal color picker demo
    modal_frame = ctk.CTkFrame(root)
    modal_frame.pack(padx=20, pady=10, fill="x")

    modal_swatch = ctk.CTkFrame(modal_frame, width=30, height=30, fg_color="#ffffff")
    modal_swatch.pack(side="left")
    modal_swatch.pack_propagate(False)

    modal_button = ctk.CTkButton(
        modal_frame, text="Open Modal Picker", command=open_modal_picker
    )
    modal_button.pack(side="left", padx=10)

    # Embedded color picker demo
    embedded_frame = ctk.CTkFrame(root)
    embedded_frame.pack(padx=20, pady=10, fill="both", expand=True)

    embedded_picker = CTkColorPicker(
        embedded_frame, width=250, command=update_embedded_picker
    )
    embedded_picker.pack(side="left")

    embedded_swatch = ctk.CTkFrame(embedded_frame, width=30, height=30, fg_color="#ffffff")
    embedded_swatch.pack(side="left", padx=10)
    embedded_swatch.pack_propagate(False)

    root.mainloop()
