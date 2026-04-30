import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

DATA_FILE = "task_history.json"

predefined_tasks = [
    {"text": "Прочитать статью", "type": "учёба"},
    {"text": "Сделать зарядку", "type": "спорт"},
    {"text": "Написать отчёт", "type": "работа"},
    {"text": "Изучить новый фреймворк", "type": "учёба"},
    {"text": "Пробежка 5 км", "type": "спорт"},
    {"text": "Провести встречу", "type": "работа"},
    {"text": "Посмотреть лекцию", "type": "учёба"},
    {"text": "Отжимания", "type": "спорт"},
    {"text": "Сделать бэкап", "type": "работа"}
]

history = []

def load_history():
    global history
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []

def save_history():
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def add_to_history(task_text, task_type):
    history.append({"text": task_text, "type": task_type, "type_display": get_type_display(task_type)})
    save_history()
    update_history_display()

def get_type_display(task_type):
    types = {"учёба": "📚 Учёба", "спорт": "🏃 Спорт", "работа": "💼 Работа"}
    return types.get(task_type, task_type)

def generate_task():
    if not predefined_tasks:
        messagebox.showwarning("Предупреждение", "Нет доступных задач")
        return
    
    task = random.choice(predefined_tasks)
    add_to_history(task["text"], task["type"])
    result_label.config(text=f"🎲 Задача: {task['text']}")

def update_history_display():
    for item in history_tree.get_children():
        history_tree.delete(item)
    
    filter_type = filter_var.get()
    
    for entry in history:
        if filter_type == "Все" or entry["type_display"] == filter_type or entry["type"] == filter_type:
            history_tree.insert("", "end", values=(entry["text"], entry["type_display"]))

def add_custom_task():
    task_text = entry_task.get().strip()
    task_type = type_var.get()
    
    if not task_text:
        messagebox.showerror("Ошибка", "Задача не может быть пустой!")
        return
    
    type_map = {"📚 Учёба": "учёба", "🏃 Спорт": "спорт", "💼 Работа": "работа"}
    type_key = type_map.get(task_type, "учёба")
    
    predefined_tasks.append({"text": task_text, "type": type_key})
    add_to_history(task_text, type_key)
    entry_task.delete(0, tk.END)
    messagebox.showinfo("Успех", f"Задача '{task_text}' добавлена!")

def filter_history():
    update_history_display()

def clear_history():
    if messagebox.askyesno("Подтверждение", "Очистить всю историю?"):
        global history
        history = []
        save_history()
        update_history_display()

root = tk.Tk()
root.title("Random Task Generator - Хрусталёва Маргарита Андреевна")
root.geometry("700x550")
root.resizable(True, True)

main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(main_frame, text="🎯 Генератор случайных задач", font=('Arial', 16, 'bold')).grid(row=0, column=0, columnspan=3, pady=10)

generate_btn = ttk.Button(main_frame, text="🎲 Сгенерировать задачу", command=generate_task, width=30)
generate_btn.grid(row=1, column=0, columnspan=3, pady=10)

result_label = ttk.Label(main_frame, text="Нажмите кнопку для генерации", font=('Arial', 12))
result_label.grid(row=2, column=0, columnspan=3, pady=10)

ttk.Separator(main_frame, orient='horizontal').grid(row=3, column=0, columnspan=3, sticky='ew', pady=10)

ttk.Label(main_frame, text="➕ Добавить новую задачу:", font=('Arial', 10, 'bold')).grid(row=4, column=0, columnspan=3, pady=(10,5))

ttk.Label(main_frame, text="Задача:").grid(row=5, column=0, sticky=tk.W, padx=5)
entry_task = ttk.Entry(main_frame, width=40)
entry_task.grid(row=5, column=1, padx=5, pady=5)

ttk.Label(main_frame, text="Тип:").grid(row=6, column=0, sticky=tk.W, padx=5)
type_var = tk.StringVar(value="📚 Учёба")
type_combo = ttk.Combobox(main_frame, textvariable=type_var, values=["📚 Учёба", "🏃 Спорт", "💼 Работа"], state="readonly", width=37)
type_combo.grid(row=6, column=1, padx=5, pady=5)

add_btn = ttk.Button(main_frame, text="Добавить задачу", command=add_custom_task, width=20)
add_btn.grid(row=7, column=0, columnspan=2, pady=5)

ttk.Separator(main_frame, orient='horizontal').grid(row=8, column=0, columnspan=3, sticky='ew', pady=10)

ttk.Label(main_frame, text="📜 История задач:", font=('Arial', 10, 'bold')).grid(row=9, column=0, sticky=tk.W)

filter_frame = ttk.Frame(main_frame)
filter_frame.grid(row=10, column=0, columnspan=3, pady=5, sticky=tk.W)

ttk.Label(filter_frame, text="Фильтр:").pack(side=tk.LEFT, padx=5)
filter_var = tk.StringVar(value="Все")
filter_combo = ttk.Combobox(filter_frame, textvariable=filter_var, values=["Все", "📚 Учёба", "🏃 Спорт", "💼 Работа"], state="readonly", width=15)
filter_combo.pack(side=tk.LEFT, padx=5)
filter_combo.bind("<<ComboboxSelected>>", lambda e: filter_history())

clear_btn = ttk.Button(filter_frame, text="Очистить историю", command=clear_history, width=15)
clear_btn.pack(side=tk.LEFT, padx=10)

columns = ("Задача", "Тип")
history_tree = ttk.Treeview(main_frame, columns=columns, show="headings", height=12)
history_tree.heading("Задача", text="Задача")
history_tree.heading("Тип", text="Тип")
history_tree.column("Задача", width=350)
history_tree.column("Тип", width=150)
history_tree.grid(row=11, column=0, columnspan=3, pady=10, sticky=(tk.W, tk.E))

scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=history_tree.yview)
scrollbar.grid(row=11, column=3, sticky=(tk.N, tk.S))
history_tree.configure(yscrollcommand=scrollbar.set)

load_history()
update_history_display()

root.mainloop()
