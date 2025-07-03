from ttkbootstrap.constants import *
from tkinter import messagebox
import ttkbootstrap as ttk
import tkinter as tk
import pyperclip
import threading
import json
import os
import sys

from pystray import MenuItem as item
import pystray
from PIL import Image

# --- CONFIGURAÇÃO ---
DATA_FILE = "textos.json"
ICON_FILE = "icone.ico" 
data_list = []

# --- Variáveis Globais para o novo sistema de seleção ---
selected_item_frame = None
selected_item_data = None

# --- FUNÇÕES DE DADOS E UTILITÁRIOS ---

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def load_data():
    global data_list
    if not os.path.exists(DATA_FILE):
        data_list = [{"titulo": "Exemplo", "texto": ["Clique em 'Adicionar' para criar um novo item!"]}]
        save_data()
        return
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data_list = json.load(f)
            if not isinstance(data_list, list):
                raise TypeError("Formato de dados inválido.")
    except (json.JSONDecodeError, TypeError) as e:
        messagebox.showerror("Erro de Dados", f"Arquivo 'textos.json' corrompido ou em formato antigo. Erro: {e}")
        data_list = []

def save_data():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data_list, f, indent=4, ensure_ascii=False)

def find_item_index_by_title(title):
    return next((i for i, item in enumerate(data_list) if item['titulo'] == title), None)

# --- FUNÇÕES DA INTERFACE (Refatoradas) ---

def on_item_select(event, item_frame, item_data):
    """Lida com a seleção de um item na lista."""
    global selected_item_frame, selected_item_data

    # Desseleciona o item antigo
    if selected_item_frame:
        selected_item_frame.configure(bootstyle="default")

    # Seleciona o novo item
    selected_item_frame = item_frame
    selected_item_frame.configure(bootstyle="primary")
    selected_item_data = item_data
    
def on_copy_button_click(item_data):
    text_to_copy = "\n".join(item_data['texto'])
    pyperclip.copy(text_to_copy)
    status_label.config(text=f'"{item_data["titulo"]}" copiado!', bootstyle="success")
    root.after(2000, lambda: status_label.config(text=""))

def create_list_item(parent, item_data):
    """Cria um frame para cada item da lista com título e botões."""
    item_frame = ttk.Frame(parent, padding=5)
    item_frame.pack(fill='x', padx=2, pady=1)

    title_label = ttk.Label(item_frame, text=item_data['titulo'], anchor='w', font=("Segoe UI", 11))
    title_label.pack(side='left', fill='x', expand=True)

    copy_button = ttk.Button(item_frame, text="Copiar", bootstyle="primary-outline", width=8, 
                             command=lambda data=item_data: on_copy_button_click(data))
    copy_button.pack(side='right')

    # Vincula o evento de clique para seleção
    item_frame.bind("<Button-1>", lambda event, frame=item_frame, data=item_data: on_item_select(event, frame, data))
    title_label.bind("<Button-1>", lambda event, frame=item_frame, data=item_data: on_item_select(event, frame, data))

def populate_listbox(filter_query=""):
    """Recria a lista de itens, aplicando o filtro de busca."""
    global selected_item_frame, selected_item_data
    selected_item_frame = None
    selected_item_data = None
    
    for widget in list_items_frame.winfo_children():
        widget.destroy()
    
    query = filter_query.lower()
    for item_data in data_list:
        if query in item_data['titulo'].lower():
            create_list_item(list_items_frame, item_data)

def on_search(event):
    search_query = search_var.get()
    populate_listbox(search_query)

def add_new_item():
    show_add_edit_window()

def edit_selected():
    if not selected_item_data:
        status_label.config(text="Selecione um item para editar!", bootstyle="warning")
        return
    item_index = find_item_index_by_title(selected_item_data['titulo'])
    if item_index is not None:
        show_add_edit_window(item_index)

def remove_selected():
    if not selected_item_data:
        status_label.config(text="Selecione um item para remover!", bootstyle="warning")
        return
    
    title_to_remove = selected_item_data['titulo']
    if messagebox.askyesno("Confirmar Remoção", f'Tem certeza que deseja remover "{title_to_remove}"?'):
        item_index = find_item_index_by_title(title_to_remove)
        if item_index is not None:
            del data_list[item_index]
            save_data()
            populate_listbox(search_var.get())

def move_item(direction):
    if not selected_item_data:
        status_label.config(text="Selecione um item para mover!", bootstyle="warning")
        return

    original_index = find_item_index_by_title(selected_item_data['titulo'])
    if original_index is None: return

    swap_with = original_index - 1 if direction == "up" else original_index + 1
    if 0 <= swap_with < len(data_list):
        # Lógica de troca correta
        data_list[original_index], data_list[swap_with] = data_list[swap_with], data_list[original_index]
        save_data()
        populate_listbox(search_var.get())

# --- JANELA DE ADICIONAR/EDITAR ---
def show_add_edit_window(item_index_to_edit=None):
    if item_index_to_edit is not None:
        item_data = data_list[item_index_to_edit]
        window_title = "Editar Item"
        initial_title = item_data.get("titulo", "")
        initial_content = "\n".join(item_data.get("texto", []))
    else:
        window_title = "Adicionar Novo Item"
        initial_title, initial_content = "", ""

    win = ttk.Toplevel(title=window_title, transient=root)
    win.grab_set()

    ttk.Label(win, text="Título:").pack(padx=10, pady=(10, 2), anchor='w')
    title_entry = ttk.Entry(win, width=60)
    title_entry.pack(padx=10, fill='x')
    title_entry.insert(0, initial_title)

    ttk.Label(win, text="Texto Completo:").pack(padx=10, pady=(10, 2), anchor='w')
    text_frame = ttk.Frame(win, padding=1)
    content_text = tk.Text(text_frame, wrap=tk.WORD, height=15)
    content_text.pack(expand=True, fill='both')
    text_frame.pack(padx=10, pady=5, expand=True, fill='both')
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

# --- BANDEJA DO SISTEMA ---
def quit_app(icon, item):
    icon.stop()  # Para a thread do ícone
    root.destroy()

def show_app(icon, item):
    icon.stop()  # Para a thread do ícone
    root.after(0, root.deiconify) # Traz a janela de volta

def hide_window():
    """Esconde a janela e mostra o ícone na bandeja usando uma thread."""
    root.withdraw()
    image = Image.open(resource_path(ICON_FILE))
    menu = (item('Mostrar', show_app), item('Sair', quit_app))
    icon = pystray.Icon("Copiador", image, "Copiador de Textos Rápidos", menu)

    thread = threading.Thread(target=icon.run)
    thread.daemon = True
    thread.start()

# --- INTERFACE GRÁFICA PRINCIPAL ---

root = ttk.Window(themename="superhero")
root.title("Copiador de Textos Rápidos")
root.geometry("700x550")

search_var = tk.StringVar()
search_entry = ttk.Entry(root, textvariable=search_var, font=("Segoe UI", 12))
search_entry.pack(pady=10, padx=10, fill='x')
search_entry.bind("<KeyRelease>", on_search)

# --- Frame com a lista e os botões de ordenação ---
main_list_frame = ttk.Frame(root)
main_list_frame.pack(pady=5, padx=10, fill='both', expand=True)

# Canvas para a lista rolável
canvas = tk.Canvas(main_list_frame, highlightthickness=0)
canvas.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(main_list_frame, orient="vertical", command=canvas.yview)
scrollbar.pack(side="right", fill="y")
canvas.configure(yscrollcommand=scrollbar.set)

list_items_frame = ttk.Frame(canvas, padding=5)
canvas.create_window((0, 0), window=list_items_frame, anchor="nw")

def on_frame_configure(event):
    canvas.configure(scrollregion=canvas.bbox("all"))
list_items_frame.bind("<Configure>", on_frame_configure)

# Frame para os botões de ordenação
order_frame = ttk.Frame(root)
order_frame.pack(pady=5, padx=10, fill='x')
up_button = ttk.Button(order_frame, text="▲ Mover para Cima", command=lambda: move_item("up"), bootstyle="secondary")
up_button.pack(side='left', expand=True, fill='x', padx=4)
down_button = ttk.Button(order_frame, text="▼ Mover para Baixo", command=lambda: move_item("down"), bootstyle="secondary")
down_button.pack(side='left', expand=True, fill='x', padx=4)

# Frame para os botões de ação
button_frame = ttk.Frame(root)
button_frame.pack(pady=10, padx=10, fill='x')
add_button = ttk.Button(button_frame, text="Adicionar", command=add_new_item, bootstyle="success")
edit_button = ttk.Button(button_frame, text="Editar Selecionado", command=edit_selected, bootstyle="warning")
remove_button = ttk.Button(button_frame, text="Remover Selecionado", command=remove_selected, bootstyle="danger")

add_button.pack(side='left', expand=True, fill='x', padx=4)
edit_button.pack(side='left', expand=True, fill='x', padx=4)
remove_button.pack(side='left', expand=True, fill='x', padx=4)

status_label = ttk.Label(root, text="Selecione um item clicando em seu título.", font=("Segoe UI", 10))
status_label.pack(pady=(0, 5))

# --- INICIALIZAÇÃO ---
load_data()
populate_listbox()

root.protocol('WM_DELETE_WINDOW', hide_window)
root.mainloop()