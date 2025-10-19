import os
from tkinter import Tk, Frame, Label, Entry, Button, Text, Scrollbar, filedialog, messagebox, StringVar, END, W
from pathlib import Path

original_ascii = "cluster.retroroyale.xyz"
original_bytes = original_ascii.encode("utf-8")
OUTPUT_NAME = "libg_PATCHED.so"

class HexPatcherGUI:
    def __init__(self, root):
        self.root = root
        root.title("Server Patcher")

        self.file_path = StringVar(value="(no file selected)")

        top = Frame(root, padx=8, pady=8)
        top.pack(fill="both", expand=False)

        Label(top, text="Select binary file:").grid(row=0, column=0, sticky=W)
        Label(top, textvariable=self.file_path, anchor="w").grid(row=0, column=1, sticky="we", padx=(8,0))
        Button(top, text="Browse...", command=self.browse_file).grid(row=0, column=2, padx=6)

        Label(top, text="Original bytes:").grid(row=1, column=0, sticky=W, pady=(8,0))
        Label(top, text=original_ascii).grid(row=1, column=1, columnspan=2, sticky=W, pady=(8,0))
        Label(top, text=f"Max length: {len(original_bytes)}").grid(row=2, column=0, sticky=W, pady=(8,0))

        Label(top, text="Replacement:").grid(row=3, column=0, sticky=W, pady=(8,0))
        self.repl_entry = Entry(top, width=60)
        self.repl_entry.grid(row=3, column=1, columnspan=2, sticky="we", pady=(8,0))
        self.repl_entry.insert(0, "127.0.0.1")

        btn_frame = Frame(root, pady=8)
        btn_frame.pack(fill="both")
        Button(btn_frame, text="Patch!", command=self.do_patch, width=14).pack(side="left", padx=6)
        Button(btn_frame, text="Quit", command=root.quit, width=10).pack(side="right", padx=6)

        log_frame = Frame(root)
        log_frame.pack(fill="both", expand=True, padx=8, pady=6)
        self.log = Text(log_frame, height=8, wrap="word")
        self.log.pack(side="left", fill="both", expand=True)
        Scrollbar(log_frame, command=self.log.yview).pack(side="right", fill="y")
        self.log.config(yscrollcommand=lambda *args: None)
        self.log_message(f"Original bytes length: {len(original_bytes)}")

    def log_message(self, msg):
        self.log.insert(END, msg + "\n")
        self.log.see(END)

    def browse_file(self):
        path = filedialog.askopenfilename(filetypes=[("All files", "*.*")])
        if path:
            self.file_path.set(path)
            self.log_message(f"Selected: {path}")

    def do_patch(self):
        path = self.file_path.get()
        if not os.path.isfile(path):
            messagebox.showerror("Error", "File not found.")
            return

        replacement = self.repl_entry.get() or ""
        replacement_bytes = replacement.encode("utf-8")
        if len(replacement_bytes) > len(original_bytes):
            messagebox.showerror("Error", f"Replacement too long. Max {len(original_bytes)}")
            return

        data = Path(path).read_bytes()
        idx = data.find(original_bytes)
        if idx == -1:
            messagebox.showerror("Error", "Original bytes not found.")
            return

        padded = replacement_bytes + b'\x00' * (len(original_bytes) - len(replacement_bytes))
        patched = data[:idx] + padded + data[idx + len(original_bytes):]

        bak = Path(path).with_suffix(Path(path).suffix + ".bak")
        if not bak.exists():
            bak.write_bytes(data)

        selected_dir = os.path.dirname(path)
        output_path = os.path.join(selected_dir, OUTPUT_NAME)
        Path(output_path).write_bytes(patched)

        self.log_message(f"Patched file: {output_path}")
        messagebox.showinfo("Success", f"Patched file created:\n{output_path}")

def main():
    root = Tk()
    root.geometry("720x300")
    HexPatcherGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()

