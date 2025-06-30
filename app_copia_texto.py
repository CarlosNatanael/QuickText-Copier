# py -3.11 app_copia_texto_final_v2.py

import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import tkinter as tk
from tkinter import messagebox

import json
import os
import pyperclip

# Importações para a bandeja do sistema
from pystray import MenuItem as item
import pystray
from PIL import Image

# --- CONFIGURAÇÃO ---
DATA_FILE = "textos.json"
ICON_FILE = "icon.png" # Certifique-se que este arquivo existe na pasta
data_list = [] # A fonte da verdade agora é uma lista de dicionários

# --- FUNÇÕES DE DADOS ---

def load_data():
    global data_list
    if not os.path.exists(DATA_FILE):
        data_list = [{"titulo": "Exemplo", "texto": ["Este é um texto de exemplo."]}]
        save_data()
        return

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            # Garante que o arquivo carregado é uma lista
            if not isinstance(data_list, list):
                raise TypeError("O formato dos dados não é uma lista.")
    except (json.JSONDecodeError, TypeError) as e:
        messagebox.showerror("Erro de Dados", f"O arquivo 'textos.json' parece estar corrompido ou em um formato antigo. Por favor, apague-o e reinicie o programa. Erro: {e}")
        data_list = [{"titulo": "Exemplo", "texto": ["Este é um texto de exemplo."]}]
        
def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

# --- FUNÇÕES DA INTERFACE ---

def populate_listbox(filter_query=""):
    listbox.delete(0, tk.END)
    query = filter_query.lower()
    for item_data in data_list:
        if query in item_data['titulo'].lower():
            listbox.insert(tk.END, item_data['titulo'])

def on_search(event):
    search_query = search_var.get()
    populate_listbox(search_query)

def find_item_index_by_title(title):
    """Encontra o índice de um item na lista de dados principal pelo título."""
    return next((i for i, item in enumerate(data_list) if item['titulo'] == title), None)

def copy_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        item_index = find_item_index_by_title(selected_title)
        if item_index is not None:
            content = data_list[item_index]['texto']
            text_to_copy = "\n".join(content)
            pyperclip.copy(text_to_copy)
            status_label.config(text=f'"{selected_title}" copiado!', bootstyle="success")
            root.after(2000, lambda: status_label.config(text=""))
    except tk.TclError:
        status_label.config(text="Selecione um item para copiar!", bootstyle="warning")

def move_item(direction):
    try:
        selected_index_listbox = listbox.curselection()[0]
        selected_title = listbox.get(selected_index_listbox)
        original_index = find_item_index_by_title(selected_title)

        if original_index is None: return

        if (direction == "up" and original_index == 0) or \
           (direction == "down" and original_index == len(data_list) - 1):
            return

        swap_with = original_index - 1 if direction == "up" else original_index + 1
        data_list[original_index], data_list[swap_with] = data_list[swap_with], data_list[original_index]
        save_data()
        
        current_filter = search_var.get()
        populate_listbox(current_filter)

        new_listbox_index = listbox.get(0, "end").index(selected_title)
        listbox.selection_set(new_listbox_index)
        listbox.activate(new_listbox_index)
    except tk.TclError:
        status_label.config(text="Selecione um item para mover!", bootstyle="warning")


# --- JANELA DE ADICIONAR/EDITAR (COMPLETA) ---

def show_add_edit_window(item_index_to_edit=None):
    if item_index_to_edit is not None:
        item_data = data_list[item_index_to_edit]
        window_title = "Editar Item"
        initial_title = item_data.get("titulo", "")
        initial_content = "\n".join(item_data.get("texto", []))
    else:
        window_title = "Adicionar Novo Item"
        initial_title, initial_content = "", ""

    win = ttk.Toplevel(title=window_title)
    win.transient(root)
    win.grab_set()

    ttk.Label(win, text="Título:").pack(padx=10, pady=(10, 2), anchor='w')
    title_entry = ttk.Entry(win)
    title_entry.pack(padx=10, fill='x')
    title_entry.insert(0, initial_title)

    ttk.Label(win, text="Texto Completo:").pack(padx=10, pady=(10, 2), anchor='w')
    text_frame = ttk.Frame(win, padding=1)
    content_text = tk.Text(text_frame, wrap=tk.WORD, height=15)
    content_text.pack(expand=True, fill='both')
    text_frame.pack(padx=10, expand=True, fill='both')
    content_text.insert("1.0", initial_content)

    def on_save():
        new_title = title_entry.get().strip()
        new_content = content_text.get("1.0", tk.END).strip()
        if not new_title or not new_content:
            messagebox.showwarning("Campos Vazios", "Título e Texto não podem estar vazios.", parent=win)
            return

        new_item = {"titulo": new_title, "texto": new_content.split('\n')}

        if item_index_to_edit is not None:
            data_list[item_index_to_edit] = new_item
        else:
            data_list.append(new_item)
        
        save_data()
        populate_listbox(search_var.get())
        win.destroy()

    ttk.Button(win, text="Salvar", command=on_save, bootstyle="success").pack(pady=10, padx=10, fill='x')

def add_new_item():
    show_add_edit_window()

def edit_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        item_index = find_item_index_by_title(selected_title)
        if item_index is not None:
            show_add_edit_window(item_index)
    except tk.TclError:
        status_label.config(text="Selecione um item para editar!", bootstyle="warning")

def remove_selected():
    try:
        selected_title = listbox.get(listbox.curselection())
        if messagebox.askyesno("Confirmar Remoção", f'Tem certeza que deseja remover "{selected_title}"?'):
            item_index = find_item_index_by_title(selected_title)
            if item_index is not None:
                del data_list[item_index]
                save_data()
                populate_listbox(search_var.get())
    except tk.TclError:
        status_label.config(text="Selecione um item para remover!", bootstyle="warning")


# --- BANDEJA DO SISTEMA (System Tray) ---

def quit_app(icon, item):
    icon.stop()
    root.destroy()

def show_app(icon, item):
    icon.stop()
    root.after(0, root.deiconify)

def hide_window():
    root.withdraw()
    image = Image.open(ICON_FILE)
    menu = (item('Mostrar', show_app), item('Sair', quit_app))
    icon = pystray.Icon("Copiador", image, "Copiador de Textos", menu)
    icon.run()

# --- INTERFACE GRÁFICA PRINCIPAL ---

root = ttk.Window(themename="superhero")
root.title("Copiador de Textos Rápidos")
root.geometry("700x600")

search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var, font=("Segoe UI", 12))
search_entry.pack(pady=10, padx=10, fill='x')
search_entry.bind("<KeyRelease>", on_search)

main_frame = ttk.Frame(root)
main_frame.pack(pady=5, padx=10, fill='both', expand=True)

list_frame = ttk.Frame(main_frame)
list_frame.pack(side='left', fill='both', expand=True)

scrollbar = ttk.Scrollbar(list_frame, orient=VERTICAL)
scrollbar.pack(side='right', fill='y')

listbox = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, font=("Segoe UI", 12), height=15)
listbox.pack(side='left', fill='both', expand=True)
scrollbar.config(command=listbox.yview)

order_frame = ttk.Frame(main_frame)
order_frame.pack(side='left', fill='y', padx=(5, 0))
up_button = ttk.Button(order_frame, text="▲", command=lambda: move_item("up"), bootstyle="secondary")
up_button.pack(pady=5, padx=5, fill='x')
down_button = ttk.Button(order_frame, text="▼", command=lambda: move_item("down"), bootstyle="secondary")
down_button.pack(pady=5, padx=5, fill='x')

copy_button = ttk.Button(root, text="Copiar Texto Selecionado", command=copy_selected, bootstyle="primary")
copy_button.pack(pady=(0, 10), padx=10, fill='x', ipady=5)

button_frame = ttk.Frame(root)
button_frame.pack(pady=(0, 10), padx=6, fill='x')

# Botões de ação agora com os comandos corretos
add_button = ttk.Button(button_frame, text="Adicionar", command=add_new_item, bootstyle="success")
edit_button = ttk.Button(button_frame, text="Editar", command=edit_selected, bootstyle="warning")
remove_button = ttk.Button(button_frame, text="Remover", command=remove_selected, bootstyle="danger")

add_button.pack(side='left', expand=True, fill='x', padx=4)
edit_button.pack(side='left', expand=True, fill='x', padx=4)
remove_button.pack(side='left', expand=True, fill='x', padx=4)

status_label = ttk.Label(root, text="", font=("Segoe UI", 10))
status_label.pack(pady=(0, 5))

# --- INICIALIZAÇÃO ---
load_data()
populate_listbox()

root.protocol('WM_DELETE_WINDOW', hide_window)
root.mainloop()