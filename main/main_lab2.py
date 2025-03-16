import tkinter as tk
from tkinter import ttk
from tkinter import ttk, messagebox
import random
import numpy as np

# Функция для анализа данных (заглушка)
def analyze_data():
    try:
        # Проверка введенных данных
        n = entry.get()
        if not n.isdigit():
            raise ValueError("Размер матрицы должен быть числом.")
        
        limit_min = limit_entry_min.get()
        if not limit_min.replace(".", "").isdigit():
            raise ValueError("Предел генерации матрицы должен быть числом.")
        
        limit_max = limit_entry_max.get()
        if not limit_max.replace(".", "").isdigit():
            raise ValueError("Предел генерации матрицы должен быть числом.")
        
        if limit_min > limit_max:
            raise ValueError("Нижний предел генерации больше верхнего")
        
        ksi = ksi_entry.get()
        if not ksi.replace(".", "").isdigit() or float(ksi) < 0 or float(ksi) > 1:
            raise ValueError("Коэффициент кси должен быть числом от 0 до 1.")
        
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
        analyzed = True
    except ValueError as e:
        # Всплывающее окно с ошибкой
        messagebox.showerror("Ошибка", str(e))

def show_data():
    try:
        # Получаем размер матрицы
        n = entry.get()
        if not n.isdigit():
            raise ValueError("Размер матрицы должен быть числом.")
        n = int(n)
                
        # Генерация матрицы C, вектора x, матрицы D и матрицы G
        limit = float(limit_entry_min.get()) if limit_entry_max.get() else 10  # Предел генерации
        C = np.random.uniform(0, limit, (n, n))  # Матрица C
        x = np.random.uniform(0, limit, n)       # Вектор x
        D = np.random.uniform(0, limit, (n, n))  # Матрица D
        G = np.random.uniform(0, limit, (n, n))  # Матрица G
        
        # Создание всплывающего окна
        popup = tk.Toplevel(root)
        popup.title("Данные")
        popup.configure(bg='#2E2E2E')  # Темно-серый фон
        popup.resizable(False, False)  # Запрет изменения размера окна
        
        # Шрифт для всех элементов
        font = ("Arial", 14)
        
        # Отображение матрицы C
        tk.Label(popup, text="Матрица C:", bg='#2E2E2E', fg='white', font=font).grid(row=0, column=0, padx=10, pady=10)
        C_frame = tk.Frame(popup, bg="white")  # Фрейм для матрицы C с белыми границами
        C_frame.grid(row=0, column=1, padx=10, pady=10)
        for i in range(n):
            for j in range(n):
                label = tk.Label(C_frame, text=f"{C[i, j]:.2f}", bg='#2E2E2E', fg='white', font=font, borderwidth=1, relief="solid")
                label.grid(row=i, column=j, padx=1, pady=1)
        
        # Отображение вектора x
        tk.Label(popup, text="Вектор x:", bg='#2E2E2E', fg='white', font=font).grid(row=1, column=0, padx=10, pady=10)
        x_frame = tk.Frame(popup, bg="white")  # Фрейм для вектора x с белыми границами
        x_frame.grid(row=1, column=1, padx=10, pady=10)
        for i in range(n):
            label = tk.Label(x_frame, text=f"{x[i]:.2f}", bg='#2E2E2E', fg='white', font=font, borderwidth=1, relief="solid")
            label.grid(row=0, column=i, padx=1, pady=1)
        
        # Отображение матрицы D
        tk.Label(popup, text="Матрица D:", bg='#2E2E2E', fg='white', font=font).grid(row=2, column=0, padx=10, pady=10)
        D_frame = tk.Frame(popup, bg="white")  # Фрейм для матрицы D с белыми границами
        D_frame.grid(row=2, column=1, padx=10, pady=10)
        for i in range(n):
            for j in range(n):
                label = tk.Label(D_frame, text=f"{D[i, j]:.2f}", bg='#2E2E2E', fg='white', font=font, borderwidth=1, relief="solid")
                label.grid(row=i, column=j, padx=1, pady=1)
        
        # Отображение матрицы G
        tk.Label(popup, text="Матрица G:", bg='#2E2E2E', fg='white', font=font).grid(row=3, column=0, padx=10, pady=10)
        G_frame = tk.Frame(popup, bg="white")  # Фрейм для матрицы G с белыми границами
        G_frame.grid(row=3, column=1, padx=10, pady=10)
        for i in range(n):
            for j in range(n):
                label = tk.Label(G_frame, text=f"{G[i, j]:.2f}", bg='#2E2E2E', fg='white', font=font, borderwidth=1, relief="solid")
                label.grid(row=i, column=j, padx=1, pady=1)
    
    except ValueError as e:
        # Всплывающее окно с ошибкой
        messagebox.showerror("Ошибка", str(e))

# Создание основного окна
root = tk.Tk()
root.title("Анализ матрицы")
root.configure(bg='#2E2E2E')  # Темно-серый фон
root.resizable(False, False)  # Запрет изменения размера окна

# Поле для ввода размера матрицы
tk.Label(root, text="Введите размер матрицы (n):", bg='#2E2E2E', fg='white',font=('Arial', 14, 'bold')).grid(row=0, column=0, padx=10, pady=10)
entry = tk.Entry(root)
entry.grid(row=0, column=1, padx=10, pady=10, columnspan=2)

# Поле для ввода предела генерации матрицы С
tk.Label(root, text="Предел генерации матрицы С:", bg='#2E2E2E', fg='white',font=('Arial', 14, 'bold')).grid(row=1, column=0, padx=10, pady=10)
limit_entry_min = tk.Entry(root, width=8)
limit_entry_min.grid(row=1, column=1)
limit_entry_max = tk.Entry(root,width=8)
limit_entry_max.grid(row=1, column=2)

# Поле для ввода коэффициента кси (от 0 до 1)
tk.Label(root, text="Коэффициент ξ (от 0 до 1):", bg='#2E2E2E', fg='white',font=('Arial', 14, 'bold')).grid(row=2, column=0, padx=10, pady=10)
ksi_entry = tk.Entry(root)
ksi_entry.grid(row=2, column=1, padx=10, pady=10, columnspan=2)

# Кнопка "Анализировать"
analyze_button = tk.Button(root, text="Анализировать", command=analyze_data, bg='white', fg='black',font=('Arial', 14, 'bold'),width=35)
analyze_button.grid(row=3, column=0, columnspan=3, pady=10)

# Кнопка "Показать данные"
show_data_button = tk.Button(root, text="Показать данные", command=show_data, bg='white', fg='black',font=('Arial', 14, 'bold'),width=35)
show_data_button.grid(row=4, column=0, columnspan=3, pady=10)

# Настройка стиля для таблицы
style = ttk.Style()
style.theme_use("default")

# Настройка фона и текста для таблицы
style.configure("Treeview",
                background="#2E2E2E",  # Темно-серый фон
                foreground="white",   # Белый текст
                fieldbackground="#2E2E2E",  # Фон ячеек
                borderwidth=1,        # Ширина границы
                relief="solid",       # Стиль границы (solid для белых границ)
                font=('Arial', 14),   # Шрифт данных в таблице (размер 14)
                rowheight=30)         # Высота строки (для видимости границ)

# Настройка заголовков таблицы
style.configure("Treeview.Heading",
                background="#2E2E2E",  # Темно-серый фон
                foreground="white",   # Белый текст
                font=('Arial', 14, 'bold'),  # Шрифт заголовков (размер 14, жирный)
                relief="solid")        # Стиль границы

# Настройка выделенной строки
style.map("Treeview",
          background=[('selected', '#4A4A4A')],  # Цвет выделенной строки
          foreground=[('selected', 'white')])    # Цвет текста выделенной строки

# Создание тега для белых границ
style.configure("white_border.Treeview",
                background="#2E2E2E",  # Темно-серый фон
                foreground="white",    # Белый текст
                fieldbackground="#2E2E2E",  # Фон ячеек
                bordercolor="white",   # Цвет границ
                padding=(0, 5))       # Отступы для создания эффекта границ

# Таблица для отображения результатов
columns = ("Стратегия", "Назначения", "S1", "S2", "Потери")
table = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    table.heading(col, text=col, anchor="center")  # Выравнивание заголовков по центру
    table.column(col, anchor="center")  # Выравнивание данных по центру
table.grid(row=0, column=3, rowspan=6, padx=10, pady=10)

# Применение тега к строкам таблицы
table.tag_configure("white_border", background="#2E2E2E", foreground="white")

# Запуск основного цикла
root.mainloop()