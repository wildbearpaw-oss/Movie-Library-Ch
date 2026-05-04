import json
import os
import tkinter as tk
from tkinter import ttk, messagebox

# Настройки
DATA_FILE = "movies.json"
movies = []
current_filter_genre = ""
current_filter_year = ""

def load_data():
    """Загрузить фильмы из JSON"""
    global movies
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                movies = json.load(f)
        else:
            movies = []
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить данные: {e}")

def save_data():
    """Сохранить фильмы в JSON"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(movies, f, ensure_ascii=False, indent=2)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось сохранить данные: {e}")

def validate_year(year):
    """Проверить год (1900–2026)"""
    try:
        year_num = int(year)
        return 1900 <= year_num <= 2026
    except ValueError:
        return False

def validate_rating(rating):
    """Проверить рейтинг (0–10)"""
    try:
        rating_num = float(rating)
        return 0 <= rating_num <= 10
    except ValueError:
        return False

def refresh_table():
    """Обновить таблицу с фильтрацией"""
    filtered = filter_movies()
    for item in tree.get_children():
        tree.delete(item)
    for movie in filtered:
        tree.insert("", "end", values=(
            movie["title"],
            movie["genre"],
            movie["year"],
            f"{movie['rating']:.1f}"
        ))

def filter_movies():
    """Отфильтровать фильмы"""
    global current_filter_genre, current_filter_year
    filtered = movies.copy()

    if current_filter_genre:
        filtered = [m for m in filtered if current_filter_genre.lower() in m["genre"].lower()]

    if current_filter_year:
        try:
            year_int = int(current_filter_year)
            filtered = [m for m in filtered if m["year"] == year_int]
        except ValueError:
            messagebox.showwarning("Ошибка", "Год для фильтрации должен быть числом!")
            current_filter_year = ""
    return filtered

def add_movie():
    """Добавить новый фильм"""
    title = title_entry.get().strip()
    genre = genre_entry.get().strip()
    year = year_entry.get().strip()
    rating = rating_entry.get().strip()

    # Валидация
    if not title:
        messagebox.showwarning("Внимание", "Введите название!")
        return
    if not genre:
        messagebox.showwarning("Внимание", "Введите жанр!")
        return
    if not validate_year(year):
        messagebox.showwarning("Внимание", "Год: 1900–2026!")
        return
    if not validate_rating(rating):
        messagebox.showwarning("Внимание", "Рейтинг: 0–10!")
        return

    # Добавление
    movie = {
        "title": title,
        "genre": genre,
        "year": int(year),
        "rating": float(rating)
    }
    movies.append(movie)
    save_data()
    clear_inputs()
    messagebox.showinfo("Успех", f"'{title}' добавлен!")
    refresh_table()

def delete_movie():
    """Удалить выбранный фильм"""
    selected = tree.selection()
    if selected:
        values = tree.item(selected[0])['values']
        title, genre, year, rating = values

        for i, movie in enumerate(movies):
            if (movie["title"] == title and
                movie["genre"] == genre and
                movie["year"] == int(year) and
                abs(movie["rating"] - float(rating)) < 0.01):
                del movies[i]
                save_data()
                refresh_table()
                messagebox.showinfo("Успех", f"'{title}' удалён!")
                return
        messagebox.showerror("Ошибка", "Фильм не найден!")
    else:
        messagebox.showwarning("Внимание", "Выберите фильм для удаления!")

def apply_genre_filter():
    """Применить фильтр по жанру"""
    global current_filter_genre
    current_filter_genre = genre_filter_entry.get().strip()
    refresh_table()
    status_label.config(text=f"Жанр: {current_filter_genre or 'Все'}", fg="blue")

def apply_year_filter():
    """Применить фильтр по году"""
    global current_filter_year
    current_filter_year = year_filter_entry.get().strip()
    refresh_table()
    status_label.config(text=f"Год: {current_filter_year or 'Все'}", fg="blue")

def reset_filters():
    """Сбросить фильтры"""
    global current_filter_genre, current_filter_year
    current_filter_genre = ""
    current_filter_year = ""
    genre_filter_entry.delete(0, tk.END)
    year_filter_entry.delete(0, tk.END)
    refresh_table()
    status_label.config(text="Фильтры сброшены", fg="blue")

def clear_inputs():
    """Очистить поля ввода"""
    title_entry.delete(0, tk.END)
    genre_entry.delete(0, tk.END)
    year_entry.delete(0, tk.END)
    rating_entry.delete(0, tk.END)

def main():
    global title_entry, genre_entry, year_entry, rating_entry
    global tree, status_label, genre_filter_entry, year_filter_entry

    root = tk.Tk()
    root.title("Movie Library — Кинотека")
    root.geometry("950x650")
    root.configure(bg="#2c3e50")

    load_data()

    # Стиль
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TFrame", background="#2c3e50")
    style.configure("TLabelframe", background="#2c3e50", foreground="white")
    style.configure("TLabel", background="#2c3e50", foreground="white")

    # Фрейм добавления
    input_frame = ttk.LabelFrame(root, text="Добавить фильм", padding=10)
    input_frame.pack(fill="x", padx=20, pady=10)

    ttk.Label(input_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    title_entry = ttk.Entry(input_frame, width=25)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Жанр:").grid(row=0, column=2, padx=5, pady=5, sticky="e")
    genre_entry = ttk.Entry(input_frame, width=20)
    genre_entry.grid(row=0, column=3, padx=5, pady=5)

    ttk.Label(input_frame, text="Год:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    year_entry = ttk.Entry(input_frame, width=15)
    year_entry.grid(row=1, column=1, padx=5, pady=5)

    ttk.Label(input_frame, text="Рейтинг (0-10):").grid(row=1, column=2, padx=5, pady=5, sticky="e")
    rating_entry = ttk.Entry(input_frame, width=15)
    rating_entry.grid(row=1, column=3, padx=5, pady=5)

    ttk.Button(input_frame, text="Добавить", command=add_movie).grid(
        row=2, column=0, columnspan=1, pady=15
    )

    # Фрейм фильтрации
    filter_frame = ttk.LabelFrame(root, text="Фильтрация", padding=10)
    filter_frame.pack(fill="x", padx=20, pady=5)

    ttk.Label(filter_frame, text="Жанр:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    genre_filter_entry = ttk.Entry(filter_frame, width=20)
    genre_filter_entry.grid(row=0, column=1, padx=5, pady=5)
    ttk.Button(filter_frame, text="Применить", command=apply_genre_filter).grid(
        row=0, column=2, padx=10
    )

    ttk.Label(filter_frame, text="Год:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    year_filter_entry = ttk.Entry(filter_frame, width=15)
    year_filter_entry.grid(row=1, column=1, padx=5, pady=5)
    ttk.Button(filter_frame, text="Применить", command=apply_year_filter).grid(
        row=1, column=2, padx=10
    )
    ttk.Button(filter_frame, text="Сбросить фильтры", command=reset_filters).grid(
        row=0, column=3, rowspan=2, padx=20
    )

    # Таблица фильмов
    tree_frame = ttk.Frame(root)
    tree_frame.pack(fill="both", expand=True, padx=20, pady=10)

    columns = ("Название", "Жанр", "Год", "Рейтинг")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=18)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180)

    tree.column("Название", width=200)
    tree.column("Жанр", width=200)
    tree.column("Год", width=80)
    tree.column("Рейтинг", width=20)

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    # Кнопки управления
    button_frame = ttk.Frame(root)
    button_frame.pack(fill="x", padx=20, pady=5)

    ttk.Button(button_frame, text="Удалить выбранный", command=delete_movie).pack(
        side="left", padx=5
    )

    # Статус-бар
    status_label = ttk.Label(
        root,
        text="Готов к работе",
        relief="sunken",
        anchor="w",
        background="#34495e",
        foreground="white"
    )
    status_label.pack(fill="x", side="bottom", padx=20, pady=5)

    # Инициализация таблицы
    refresh_table()

    root.mainloop()

if __name__ == "__main__":
    main()