import tkinter as tk
from tkinter import ttk, messagebox
import json, os

# --- ФАЙЛ README.MD (в комментариях) ---
# Автор: [Ваше Имя и Фамилия]
# Описание: Компактное приложение для учета фильмов с сохранением в JSON.
# Тест: Введите "Inception", "Sci-Fi", "2010", "8.8" и нажмите Добавить.

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie DB")
        self.db = "movies.json"
        self.data = json.load(open(self.db)) if os.path.exists(self.db) else []

        # Поля ввода
        params = [("Название", 0), ("Жанр", 1), ("Год", 2), ("Рейтинг", 3)]
        self.entries = {}
        for text, row in params:
            tk.Label(root, text=text).grid(row=row, column=0)
            e = tk.Entry(root)
            e.grid(row=row, column=1)
            self.entries[text] = e

        tk.Button(root, text="Добавить", command=self.add).grid(row=4, column=0, columnspan=2)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("T", "G", "Y", "R"), show="headings", height=8)
        for c, h in zip(("T", "G", "Y", "R"), ("Название", "Жанр", "Год", "Рейтинг")):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=100)
        self.tree.grid(row=5, column=0, columnspan=2)
        
        self.refresh()

    def add(self):
        try:
            m = {k: v.get() for k, v in self.entries.items()}
            if not m["Название"] or not (0 <= float(m["Рейтинг"]) <= 10): raise ValueError
            int(m["Год"])
            self.data.append(m)
            with open(self.db, "w") as f: json.dump(self.data, f)
            self.refresh()
        except:
            messagebox.showerror("Ошибка", "Неверный формат данных (Год - число, Рейтинг 0-10)")

    def refresh(self):
        self.tree.delete(*self.tree.get_children())
        for m in self.data: self.tree.insert("", "end", values=list(m.values()))

if __name__ == "__main__":
    root = tk.Tk()
    MovieApp(root)
    root.mainloop()

