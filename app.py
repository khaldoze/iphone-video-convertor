import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def get_ffmpeg_path():
    if getattr(sys, 'frozen', False):
        return os.path.join(sys._MEIPASS, "ffmpeg.exe")
    return "ffmpeg"

def convert_video(input_path, progress_bar, status_label, convert_btn):
    try:
        base, _ = os.path.splitext(input_path)
        output_path = f"{base}_converted.mp4"
        ffmpeg_bin = get_ffmpeg_path()

        cmd = [
            ffmpeg_bin, "-y",
            "-i", input_path,
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "medium",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "192k",
            "-movflags", "+faststart",
            output_path
        ]

        creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

        process = subprocess.run(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            creationflags=creationflags
        )

        if process.returncode == 0:
            status_label.config(text="Conversion completed successfully!", fg="green")
            messagebox.showinfo("Success", f"High-quality MP4 saved to:\n{output_path}")
        else:
            status_label.config(text="Error during conversion", fg="red")
            messagebox.showerror("Error", "Failed to convert video. Please check the file.")

    except Exception as e:
        status_label.config(text=f"Error: {str(e)}", fg="red")
    finally:
        progress_bar.stop()
        convert_btn.config(state="normal")

def start_conversion(file_path_var, progress_bar, status_label, convert_btn):
    input_path = file_path_var.get()
    if not input_path or not os.path.isfile(input_path):
        messagebox.showwarning("Warning", "Please select a video file first.")
        return

    convert_btn.config(state="disabled")
    status_label.config(text="Converting... Please wait", fg="blue")
    progress_bar.start(10)

    threading.Thread(
        target=convert_video,
        args=(input_path, progress_bar, status_label, convert_btn),
        daemon=True
    ).start()

def choose_file(file_path_var, status_label):
    path = filedialog.askopenfilename(
        title="Select iPhone Video",
        filetypes=[("Video Files", "*.mov *.MOV *.mp4 *.MP4 *.m4v"), ("All Files", "*.*")]
    )
    if path:
        file_path_var.set(path)
        status_label.config(text="Ready to convert", fg="black")

root = tk.Tk()
root.title("khaldoze converter")
root.geometry("460x250")
root.resizable(False, False)

file_path = tk.StringVar()

tk.Label(root, text="khaldoze converter", font=("Segoe UI", 15, "bold")).pack(pady=12)

frame = tk.Frame(root)
frame.pack(pady=5, padx=15, fill="x")

entry = tk.Entry(frame, textvariable=file_path, width=36)
entry.pack(side="left", padx=5, ipady=3)

browse_btn = tk.Button(frame, text="Browse...", command=lambda: choose_file(file_path, status_lbl))
browse_btn.pack(side="left", padx=5)

progress = ttk.Progressbar(root, mode="indeterminate", length=400)
progress.pack(pady=15)

convert_button = tk.Button(
    root,
    text="Convert to High-Quality MP4",
    bg="#28a745",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    padx=10,
    pady=4,
    command=lambda: start_conversion(file_path, progress, status_lbl, convert_button)
)
convert_button.pack(pady=5)

status_lbl = tk.Label(root, text="Select a MOV file to start", fg="gray")
status_lbl.pack(pady=5)

root.mainloop()