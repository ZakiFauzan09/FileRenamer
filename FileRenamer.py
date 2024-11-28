import os
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox

def auto_format_date(*args):
    date = date_var.get()
    formatted_date = ''.join(filter(lambda x: x.isdigit() or x == '-', date))

    if len(formatted_date) > 4 and formatted_date[4] != '-':
        formatted_date = formatted_date[:4] + '-' + formatted_date[4:]
    if len(formatted_date) > 7 and formatted_date[7] != '-':
        formatted_date = formatted_date[:7] + '-' + formatted_date[7:]
    if len(formatted_date) > 10:
        formatted_date = formatted_date[:10]

    date_var.set(formatted_date)
    date_entry.icursor(len(formatted_date))

def rename_files():
    directory = dir_path.get()
    target_date = date_var.get()
    file_types = file_types_entry.get().split(",")
    event_name = event_name_entry.get()

    if not directory or not os.path.isdir(directory):
        messagebox.showerror("Error", "Pilih direktori yang valid!")
        return
    try:
        datetime.strptime(target_date, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Error", "Format tanggal salah! Gunakan format YYYY-MM-DD.")
        return
    if not event_name:
        messagebox.showerror("Error", "Nama event tidak boleh kosong!")
        return

    file_types = [ftype.strip().lower() for ftype in file_types]
    counter = 1

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            modified_time = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_date = modified_time.strftime("%Y-%m-%d")
            file_extension = os.path.splitext(filename)[1][1:].lower()

            if file_date == target_date and file_extension in file_types:
                new_name = f"{event_name}{counter}.{file_extension}"
                new_path = os.path.join(directory, new_name)
                os.rename(filepath, new_path)
                counter += 1

    messagebox.showinfo("Selesai", f"{counter - 1} file berhasil diubah namanya.")

def browse_directory():
    path = filedialog.askdirectory()
    if path:
        dir_path.set(path)

def update_suggestions(event):
    typed = file_types_entry.get()
    if not typed:
        # Sembunyikan dropdown jika input kosong
        listbox_suggestions.place_forget()
        return

    suggestions = [ext for ext in all_extensions if ext.startswith(typed)]
    listbox_suggestions.delete(0, tk.END)
    for suggestion in suggestions:
        listbox_suggestions.insert(tk.END, suggestion)
    if suggestions:
        listbox_suggestions.place(x=file_types_entry.winfo_x(), y=file_types_entry.winfo_y() + 25, width=file_types_entry.winfo_width())
    else:
        listbox_suggestions.place_forget()

def select_suggestion(event):
    selected = listbox_suggestions.get(listbox_suggestions.curselection())
    file_types_entry.delete(0, tk.END)
    file_types_entry.insert(0, selected)
    listbox_suggestions.place_forget()

def hide_suggestions(event):
    if not (listbox_suggestions.winfo_containing(event.x_root, event.y_root) or 
            file_types_entry.winfo_containing(event.x_root, event.y_root)):
        listbox_suggestions.place_forget()

# Daftar ekstensi file umum
all_extensions = ["jpg", "jpeg", "png", "gif", "mp4", "mkv", "avi", "mov", "pdf", "docx", "xlsx", "txt", "csv", "zip", "rar"]

# Membuat UI dengan Tkinter
root = tk.Tk()
root.title("File Renamer")

tk.Label(root, text="Pilih Direktori:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
dir_path = tk.StringVar()
tk.Entry(root, textvariable=dir_path, width=40).grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_directory).grid(row=0, column=2, padx=10, pady=5)

tk.Label(root, text="Masukkan Tanggal (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=10, pady=5)
date_var = tk.StringVar()
date_var.trace("w", auto_format_date)
date_entry = tk.Entry(root, textvariable=date_var, width=20)
date_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Jenis File:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
file_types_entry = tk.Entry(root, width=40)
file_types_entry.grid(row=2, column=1, padx=10, pady=5)
file_types_entry.bind("<KeyRelease>", update_suggestions)

# Listbox untuk saran ekstensi
listbox_suggestions = tk.Listbox(root, height=5)
listbox_suggestions.bind("<<ListboxSelect>>", select_suggestion)

# Menangkap klik di luar input untuk menyembunyikan dropdown
root.bind("<Button-1>", hide_suggestions)

tk.Label(root, text="Nama Event:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
event_name_entry = tk.Entry(root, width=20)
event_name_entry.grid(row=3, column=1, padx=10, pady=5)

tk.Button(root, text="Ganti Nama File", command=rename_files, bg="lightblue").grid(row=4, column=1, pady=20)

root.mainloop()
