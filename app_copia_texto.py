# py -3.11 app_copia_texto.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk

import json
import os
import pyperclip

DATA_FILE = "textos.json"
data = {}

def load_data():
    global data
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
    else:
        data = {"Exemplo": "Este é um texto de exemplo."}
        save_data()

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def populate_listbox():
    listbox.delete(0, tk.END)
    for title in sorted(data.keys()):
        listbox.insert(tk.END, title)

def copy_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        content = data.get(selected_title, "")
        text_to_copy = "\n".join(content) if isinstance(content, list) else content
        pyperclip.copy(text_to_copy)
        status_label.config(text=f'"{selected_title}" copiado!', bootstyle="success")
        root.after(2000, lambda: status_label.config(text=""))
    except tk.TclError:
        # Este erro acontece se nada estiver selecionado
        status_label.config(text="Selecione um item para copiar!", bootstyle="warning")
    except Exception as e:
        status_label.config(text=f"Erro: {e}", bootstyle="danger")

def show_add_edit_window(title_to_edit=None):
    # ATUALIZADO: Usando widgets ttk para consistência visual
    if title_to_edit:
        window_title = "Editar Item"
        initial_title = title_to_edit
        content = data.get(title_to_edit, "")
        initial_content = "\n".join(content) if isinstance(content, list) else content
    else:
        window_title = "Adicionar Novo Item"
        initial_title, initial_content = "", ""

    win = ttk.Toplevel(title=window_title, transient=root)
    win.grab_set()

    ttk.Label(win, text="Título:").pack(padx=10, pady=(10, 2), anchor='w')
    title_entry = ttk.Entry(win)
    title_entry.pack(padx=10, fill='x')
    title_entry.insert(0, initial_title)

    ttk.Label(win, text="Texto Completo:").pack(padx=10, pady=(10, 2), anchor='w')
    
    # Text não tem um equivalente no ttk, então usamos tk.Text, mas podemos estilizá-lo
    text_frame = ttk.Frame(win, padding=1)
    content_text = tk.Text(text_frame, wrap=tk.WORD, height=15)
    content_text.pack(expand=True, fill='both')
    text_frame.pack(padx=10, expand=True, fill='both')
    content_text.insert("1.0", initial_content)

    def on_save():
        new_title = title_entry.get().strip()
        new_content = content_text.get("1.0", tk.END).strip()
        if not new_title or not new_content: return

        if title_to_edit and title_to_edit != new_title:
            del data[title_to_edit]
        
        data[new_title] = new_content.split('\n')
        save_data()
        populate_listbox()
        win.destroy()

    ttk.Button(win, text="Salvar", command=on_save, bootstyle="success").pack(pady=10, padx=10, fill='x')

def edit_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        show_add_edit_window(selected_title)
    except tk.TclError:
        status_label.config(text="Selecione um item para editar!", bootstyle="warning")

def remove_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        if messagebox.askyesno("Confirmar Remoção", f'Tem certeza que deseja remover "{selected_title}"?'):
            del data[selected_title]
            save_data()
            populate_listbox()
    except tk.TclError:
        status_label.config(text="Selecione um item para remover!", bootstyle="warning")

# --- INTERFACE GRÁFICA PRINCIPAL (GUI) ---

root = ttk.Window(themename="superhero") 
root.title("Copiador de Textos Rápidos")
root.geometry("600x450")

list_frame = ttk.Frame(root)
list_frame.pack(pady=10, padx=10, fill='both', expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL)
scrollbar.pack(side='right', fill='y')

# CORREÇÃO PRINCIPAL AQUI: de ttk.Listbox para tk.Listbox
listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Segoe UI", 12))
listbox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=listbox.yview)

copy_button = ttk.Button(root, text="Copiar Texto Selecionado", command=copy_selected, bootstyle="primary")
copy_button.pack(pady=(0, 10), padx=10, fill='x', ipady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=(0, 10), padx=6, fill='x')

add_button = ttk.Button(button_frame, text="Adicionar", command=show_add_edit_window, bootstyle="success")
edit_button = ttk.Button(button_frame, text="Editar", command=edit_selected, bootstyle="warning")
remove_button = ttk.Button(button_frame, text="Remover", command=remove_selected, bootstyle="danger")

add_button.pack(side='left', expand=True, fill='x', padx=4)
edit_button.pack(side='left', expand=True, fill='x', padx=4)
remove_button.pack(side='left', expand=True, fill='x', padx=4)

status_label = ttk.Label(root, text="", font=("Segoe UI", 10))
status_label.pack(pady=(0, 5))

load_data()
populate_listbox()
root.mainloop()