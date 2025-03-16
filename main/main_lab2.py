import tkinter as tk
from tkinter import ttk
import random

# Функция для анализа данных (заглушка)
def analyze_data():
    # Очистка таблицы перед заполнением новыми данными
    for row in table.get_children():
        table.delete(row)
    
    # Заполнение таблицы случайными значениями
    for i in range(5):
        strategy = f"Стратегия {i+1}"
        assignments = random.randint(1, 100)
        s1 = random.randint(1, 100)
        s2 = random.randint(1, 100)
        losses = random.randint(1, 100)
        table.insert("", "end", values=(strategy, assignments, s1, s2, losses))

# Функция для отображения данных (заглушка)
def show_data():
    # Здесь можно добавить логику отображения данных
    print("Данные показаны")

# Создание основного окна
root = tk.Tk()
root.title("Анализ матрицы")
root.configure(bg='#2E2E2E')  # Темно-серый фон

# Поле для ввода размера матрицы
tk.Label(root, text="Введите размер матрицы (n):", bg='#2E2E2E', fg='white').grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10)

# Настройки генерации матрицы
tk.Label(root, text="Режим генерации матрицы С:", bg='#2E2E2E', fg='white').grid(row=1, column=0, padx=10, pady=10)
mode_options = ["Случайная", "Возрастающая", "Убывающая"]
mode_var = tk.StringVar(value=mode_options[0])
mode_menu = ttk.Combobox(root, textvariable=mode_var, values=mode_options, state="readonly")
mode_menu.grid(row=1, column=1, padx=10, pady=10, sticky='ew')

# Настройки изменения строк
tk.Label(root, text="Изменение строк:", bg='#2E2E2E', fg='white').grid(row=2, column=0, padx=10, pady=10)
row_options = ["Случайная", "Возрастающая", "Убывающая"]
row_var = tk.StringVar(value=row_options[0])
row_menu = ttk.Combobox(root, textvariable=row_var, values=row_options, state="readonly")
row_menu.grid(row=2, column=1, padx=10, pady=10, sticky='ew')

# Настройки изменения столбцов
tk.Label(root, text="Изменение столбцов:", bg='#2E2E2E', fg='white').grid(row=3, column=0, padx=10, pady=10)
col_options = ["Случайная", "Возрастающая", "Убывающая"]
col_var = tk.StringVar(value=col_options[0])
col_menu = ttk.Combobox(root, textvariable=col_var, values=col_options, state="readonly")
col_menu.grid(row=3, column=1, padx=10, pady=10, sticky='ew')

# Кнопка "Анализировать"
analyze_button = tk.Button(root, text="Анализировать", command=analyze_data, bg='white', fg='black')
analyze_button.grid(row=4, column=0, columnspan=2, pady=10)

# Кнопка "Показать данные"
show_data_button = tk.Button(root, text="Показать данные", command=show_data, bg='white', fg='black')
show_data_button.grid(row=5, column=0, columnspan=2, pady=10)

# Настройка стиля для таблицы
style = ttk.Style()
style.theme_use("default")

# Настройка фона и текста для таблицы
style.configure("Treeview",
                background="#2E2E2E",  # Темно-серый фон
                foreground="white",     # Белый текст
                fieldbackground="#2E2E2E",  # Фон ячеек
                borderwidth=1,          # Ширина границы
                relief="solid")        # Стиль границы (solid для белых границ)

# Настройка заголовков таблицы
style.configure("Treeview.Heading",
                background="#2E2E2E",  # Темно-серый фон
                foreground="white",    # Белый текст
                font=('Arial', 10, 'bold'),  # Шрифт заголовков
                relief="solid")        # Стиль границы

# Настройка выделенной строки
style.map("Treeview",
          background=[('selected', '#4A4A4A')],  # Цвет выделенной строки
          foreground=[('selected', 'white')])    # Цвет текста выделенной строки

# Таблица для отображения результатов
columns = ("Стратегия", "Назначения", "S1", "S2", "Потери")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col)
table.grid(row=0, column=2, rowspan=6, padx=10, pady=10)

# Запуск основного цикла
root.mainloop()