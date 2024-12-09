# /USER IMPORT/ BEGIN
import strategies
import generate_data as generator
# /USER IMPORT/ END

# /THIRD PARTY/ BEGIN
import tkinter as tk
from tkinter import ttk
# /THIRD PARTY/ END

class DecisionSupportSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Система поддержки принятия решений")
        
        # Ввод данных
        self.setup_input_frame()
        
        # Вывод интерпретации
        self.setup_output_frame()
        
    def setup_input_frame(self):
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(side=tk.LEFT, fill=tk.Y)
        
        # Количество партий
        tk.Label(input_frame, text="Кол-во партий:").grid(row=0, column=0, sticky="w")
        self.batches = tk.Entry(input_frame, width=10)
        self.batches.grid(row=0, column=1)

        # Длительность этапа
        tk.Label(input_frame, text="Длительность этапа: 7 дней").grid(row=1, column=0, sticky="w")

        # Суточная масса
        tk.Label(input_frame, text="Суточная масса:").grid(row=2, column=0, sticky="w")
        self.daily_mass = tk.Entry(input_frame, width=10)
        self.daily_mass.grid(row=2, column=1)

        # Диапазон отклонений сахаристости
        tk.Label(input_frame, text="Диапазон отклонений сахаристости:").grid(row=3, column=0, sticky="w")
        self.deviation_min = tk.Entry(input_frame, width=10)
        self.deviation_min.grid(row=3, column=1)
        self.deviation_max = tk.Entry(input_frame, width=10)
        self.deviation_max.grid(row=3, column=2)

        # Диапазон отклонений
        tk.Label(input_frame, text="Диапазон отклонений:").grid(row=4, column=0, sticky="w")
        self.deviation_min = tk.Entry(input_frame, width=10)
        self.deviation_min.grid(row=4, column=1)
        self.deviation_max = tk.Entry(input_frame, width=10)
        self.deviation_max.grid(row=4, column=2)

        # Учет дополнительных условий
        tk.Label(input_frame, text="Учитывать доп. условия:").grid(row=5, column=0, sticky="w")
        self.extra_conditions = tk.BooleanVar()
        tk.Checkbutton(input_frame, variable=self.extra_conditions).grid(row=5, column=1, sticky="w")

        # Количество экспериметров
        tk.Label(input_frame, text="Количество экспериментров:").grid(row=6, column=0, sticky="w")
        self.daily_mass = tk.Entry(input_frame, width=10)
        self.daily_mass.grid(row=6, column=1)

        # Кнопка запуска
        tk.Button(input_frame, text="Запуск", command=self.calculate).grid(row=7, column=0, columnspan=3)

    def setup_output_frame(self):
        self.output_frame = tk.Frame(self.root, padx=10, pady=10)
        self.output_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.output_text = tk.Text(self.output_frame, wrap="word", height=20, width=50)
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
    def runtime(self):
        try:
            input_example = generator.input_example()
            result = strategies.output_example(input_example)

            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)
        except ValueError:
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, "Ошибка ввода данных!")

if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionSupportSystem(root)
    root.mainloop()