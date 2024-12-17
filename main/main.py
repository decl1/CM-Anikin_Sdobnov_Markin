# /USER IMPORT/ BEGIN
import strategies
import generate_data as generator
# /USER IMPORT/ END

# /THIRD PARTY/ BEGIN
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# /THIRD PARTY/ END

def show_warning(best_strategy):
    """Вывод предупреждения."""
    messagebox.showwarning("Лучшая стратегия", "Лучшая стратегия: " + best_strategy)

def add_new_bars(datasets,categories,values, label, color, ax, canvas):
        bar_width = 0.2
        datasets.append((values, label, color))  # Добавляем новый набор данных
        ax.clear()  # Очищаем график для перерисовки
        # Строим все столбцы
        num_datasets = len(datasets)
        for i, (values, label, color) in enumerate(datasets):
            x_offsets = [
                x - (num_datasets / 2 - i) * bar_width for x in range(len(categories))
            ]
            bars = ax.bar(
                x_offsets,
                values,
                width=bar_width,
                label=label,
                color=color,
                edgecolor="black"
            )
            # Добавляем метки значений
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    height + 0.1,
                    f"{height}",
                    ha="center",
                    va="bottom"
                )
        # Настройки осей
        ax.set_title("Количество накопленого сахара")
        ax.set_xlabel("Стратегии")
        ax.set_ylabel("Значения")
        ax.set_xticks(range(len(categories)))
        ax.set_xticklabels(categories)
        ax.legend()
        # Обновляем график
        canvas.draw()

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
        tk.Label(input_frame, text="Кол-во партий, Этапов: ").grid(row=0, column=0, sticky="w")
        self.partiiandetapi = tk.Entry(input_frame, width=10)
        self.partiiandetapi.grid(row=0, column=1)

        # Длительность этапа
        tk.Label(input_frame, text="Длительность этапа: 7 дней").grid(row=1, column=0, sticky="w")

        # Суточная масса
        tk.Label(input_frame, text="Суточная масса:").grid(row=2, column=0, sticky="w")
        self.daily_mass = tk.Entry(input_frame, width=10)
        self.daily_mass.grid(row=2, column=1)

        # Диапазон отклонений сахаристости
        tk.Label(input_frame, text="Диапазон отклонений сахаристости:").grid(row=3, column=0, sticky="w")
        self.sugar_deviation_min = tk.Entry(input_frame, width=10)
        self.sugar_deviation_min.grid(row=3, column=1)
        self.sugar_deviation_max = tk.Entry(input_frame, width=10)
        self.sugar_deviation_max.grid(row=3, column=2)

        # Диапазон отклонений
        tk.Label(input_frame, text="Диапазон отклонений:").grid(row=4, column=0, sticky="w")
        self.deviation_min = tk.Entry(input_frame, width=10)
        self.deviation_min.grid(row=4, column=1)
        self.deviation_max = tk.Entry(input_frame, width=10)
        self.deviation_max.grid(row=4, column=2)

        # Учет дополнительных условий
        tk.Label(input_frame, text="Учитывать неорганику?:").grid(row=5, column=0, sticky="w")
        self.extra_conditions = tk.BooleanVar()
        tk.Checkbutton(input_frame, variable=self.extra_conditions).grid(row=5, column=1, sticky="w")

        # Количество этапов дозаривания
        tk.Label(input_frame, text="Количество этапов дозаривания:").grid(row=6, column=0, sticky="w")
        self.ripening_number = tk.Entry(input_frame, width=10)
        self.ripening_number.grid(row=6, column=1)

        self.selected_option = False
        tk.Radiobutton(input_frame, text="Концентрированное распределение", variable=self.selected_option, value=True).grid(row=7,column=0,sticky="w")
        tk.Radiobutton(input_frame, text="Нормальное распределение", variable=self.selected_option, value=False).grid(row=8,column=0,sticky="w")

        # Количество экспериметров
        tk.Label(input_frame, text="Количество экспериментов:").grid(row=9, column=0, sticky="w")
        self.exp_number = tk.Entry(input_frame, width=10)
        self.exp_number.grid(row=9, column=1)

        # Кнопка запуска
        tk.Button(input_frame, text="Запуск", command=self.runtime).grid(row=10, column=0, columnspan=3)

    def setup_output_frame(self):
        # Создаем контейнер для графика
        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=True)

        # Создаем график с помощью matplotlib
        fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = fig.add_subplot(111)
        # Исходные данные
        self.categories = ["Greedy", "Thrifty", "Thrifty/Greedy", "Greedy/Thrifty", "T(k)G",  "Average"]
        self.datasets = []  # Список для хранения всех наборов данных
        # Настройки осей
        self.ax.set_title("Количество накопленого сахара")
        self.ax.set_xlabel("Стратегии")
        self.ax.set_ylabel("Значения")
        self.ax.set_xticks(range(len(self.categories)))
        self.ax.set_xticklabels(self.categories)
        # Отображаем график в Tkinter
        self.canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas_widget = self.canvas.get_tk_widget()
        canvas_widget.pack(fill=tk.BOTH, expand=True)
        
    def runtime(self):
        # очистка графика
        self.ax.clear()
        self.datasets.clear()
        #добавление графиков
        total_results = strategies.run_virtual_experiments(int(self.exp_number.get()),int(self.daily_mass.get()),7,int(self.partiiandetapi.get()),
                                                           int(self.partiiandetapi.get()), 1,
                                                           float(self.sugar_deviation_min.get()),float(self.sugar_deviation_max.get()),
                                                           float(self.deviation_min.get()),float(self.deviation_max.get()),
                                                           self.selected_option, int(self.ripening_number.get()), bool(self.extra_conditions.get()))
        values_sugar = []
        values_losses = []
        for strategy in total_results:
            values_sugar.append(total_results[strategy]['sugar'])
            values_losses.append(total_results[strategy]['losses'])
        values_sugar = [round(num, 3) for num in values_sugar]
        values_losses = [round(num, 3) for num in values_losses]
        max_sugar = 0
        max_index = 0
        i = -1
        for sugar in values_sugar:
            i += 1
            if sugar > max_sugar:
                max_sugar = sugar
                max_index = i
        add_new_bars(self.datasets,self.categories, values_sugar, "Sugar", "blue", self.ax, self.canvas)
        add_new_bars(self.datasets,self.categories, values_losses, "Losses", "red", self.ax, self.canvas)
        show_warning(self.categories[max_index])


if __name__ == "__main__":
    root = tk.Tk()
    app = DecisionSupportSystem(root)
    root.mainloop()