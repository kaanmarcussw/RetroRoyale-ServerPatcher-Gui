# Retro Royale libg.so Patcher GUI

This tool provides a simple Tkinter GUI to patch the `libg.so` file from the Retro Royale APK.  
It replaces the built-in server address `cluster.retroroyale.xyz` with your own IP or domain, allowing you to connect to your private server.  
The patched file is automatically saved as `libg_PATCHED.so` in the directory from which you run the GUI.

---

## How it works

- Scans the `libg.so` binary for the original server string `cluster.retroroyale.xyz`.  
- Replaces the found string with your custom IP address or domain.  
- Fills any remaining space with null bytes (`00`) to maintain the original file size.  
- Saves the patched file as `libg_PATCHED.so` in the current working directory, while showing logs and status messages in the GUI.

---

## Requirements

- Python 3.x or higher

---

## How to use

1. Run the GUI script:
2. Click Browse... and select the libg.so file from your system.
3. Enter your custom IP address or domain in the Replacement field.
4. Click the "Patch!" button.
5. The patched file libg_PATCHED.so will be created in the directory where you selected libg.so file

---

## Backup & restore (.bak file)

- The tool automatically creates a backup of the original libg.so in the same folder as the original file with the .bak extension (e.g. libg.so.bak).

- To restore the original: delete the patched file, then rename libg.so.bak back to libg.so.

---

## Disclaimer

- Don't forget to delete the `x86` folder inside the APK's `lib` directory.
