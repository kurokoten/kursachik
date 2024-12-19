import sqlite3
from tkinter import *
from tkinter import ttk, messagebox

# Подключение к базе данных
conn = sqlite3.connect("company.db")
cursor = conn.cursor()

# Создание таблицы пользователей (для регистрации и входа)
cursor.execute("""
CREATE TABLE IF NOT EXISTS Users (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Username TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
)
""")

# Создание таблицы "Отделы"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Departments (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Наименование TEXT NOT NULL UNIQUE,
    РодительскийОтделID INTEGER,
    FOREIGN KEY (РодительскийОтделID) REFERENCES Departments(ID)
)
""")

# Создание таблицы "Сотрудники"
cursor.execute("""
CREATE TABLE IF NOT EXISTS Employees (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    ФИО TEXT NOT NULL UNIQUE,
    Должность TEXT NOT NULL,
    ОтделID INTEGER,
    ДатаНайма DATE,
    Телефон TEXT,
    FOREIGN KEY (ОтделID) REFERENCES Departments(ID)
)
""")

conn.commit()

# Окно регистрации
def register_window():
    def register():
        username = entry_username.get()
        password = entry_password.get()
        if username and password:
            try:
                cursor.execute("INSERT INTO Users (Username, Password) VALUES (?, ?)", (username, password))
                conn.commit()
                messagebox.showinfo("Успех", "Регистрация прошла успешно!")
                register_win.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Ошибка", "Пользователь с таким именем уже существует!")
        else:
            messagebox.showerror("Ошибка", "Заполните все поля!")

    register_win = Toplevel()
    register_win.title("Регистрация")
    register_win.geometry("300x200")

    label_username = Label(register_win, text="Имя пользователя:")
    label_username.pack(pady=5)
    entry_username = Entry(register_win)
    entry_username.pack(pady=5)

    label_password = Label(register_win, text="Пароль:")
    label_password.pack(pady=5)
    entry_password = Entry(register_win, show="*")
    entry_password.pack(pady=5)

    btn_register = ttk.Button(register_win, text="Зарегистрироваться", command=register)
    btn_register.pack(pady=10)

# Окно входа
def login_window():
    def login():
        username = entry_username.get()
        password = entry_password.get()
        cursor.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
        user = cursor.fetchone()
        if user:
            messagebox.showinfo("Успех", "Вход выполнен!")
            login_win.destroy()
            main_window()
        else:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль!")

    login_win = Toplevel()
    login_win.title("Вход")
    login_win.geometry("300x250")

    label_username = Label(login_win, text="Имя пользователя:")
    label_username.pack(pady=5)
    entry_username = Entry(login_win)
    entry_username.pack(pady=5)

    label_password = Label(login_win, text="Пароль:")
    label_password.pack(pady=5)
    entry_password = Entry(login_win, show="*")
    entry_password.pack(pady=5)

    btn_login = ttk.Button(login_win, text="Войти", command=login)
    btn_login.pack(pady=10)

    btn_register = ttk.Button(login_win, text="Регистрация", command=register_window)
    btn_register.pack(pady=10)

# Основное окно приложения
def main_window():
    def view_employees():
        def add_employee():
            def save_employee():
                fio = entry_fio.get()
                position = entry_position.get()
                department_id = entry_department.get()
                hire_date = entry_hire_date.get()
                phone = entry_phone.get()
                if fio and position and department_id:
                    try:
                        cursor.execute("""
                        INSERT INTO Employees (ФИО, Должность, ОтделID, ДатаНайма, Телефон) 
                        VALUES (?, ?, ?, ?, ?)
                        """, (fio, position, department_id, hire_date, phone))
                        conn.commit()
                        messagebox.showinfo("Успех", "Сотрудник добавлен!")
                        add_win.destroy()
                        view_employees()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Ошибка", "Сотрудник с таким ФИО уже существует!")
                else:
                    messagebox.showerror("Ошибка", "Заполните все обязательные поля!")

            add_win = Toplevel()
            add_win.title("Добавить сотрудника")
            add_win.geometry("400x300")

            Label(add_win, text="ФИО:").pack(pady=5)
            entry_fio = Entry(add_win)
            entry_fio.pack(pady=5)

            Label(add_win, text="Должность:").pack(pady=5)
            entry_position = Entry(add_win)
            entry_position.pack(pady=5)

            Label(add_win, text="ID отдела:").pack(pady=5)
            entry_department = Entry(add_win)
            entry_department.pack(pady=5)

            Label(add_win, text="Дата найма (ГГГГ-ММ-ДД):").pack(pady=5)
            entry_hire_date = Entry(add_win)
            entry_hire_date.pack(pady=5)

            Label(add_win, text="Телефон:").pack(pady=5)
            entry_phone = Entry(add_win)
            entry_phone.pack(pady=5)

            ttk.Button(add_win, text="Сохранить", command=save_employee).pack(pady=10)

        employees_win = Toplevel()
        employees_win.title("Список сотрудников")
        employees_win.geometry("600x400")

        tree = ttk.Treeview(employees_win, columns=("ID", "ФИО", "Должность", "Отдел", "Дата найма", "Телефон"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("ФИО", text="ФИО")
        tree.heading("Должность", text="Должность")
        tree.heading("Отдел", text="Отдел")
        tree.heading("Дата найма", text="Дата найма")
        tree.heading("Телефон", text="Телефон")
        tree.pack(fill=BOTH, expand=True)

        cursor.execute("""
        SELECT e.ID, e.ФИО, e.Должность, d.Наименование, e.ДатаНайма, e.Телефон
        FROM Employees e
        JOIN Departments d ON e.ОтделID = d.ID
        """)
        employees = cursor.fetchall()

        for employee in employees:
            tree.insert("", "end", values=employee)

        ttk.Button(employees_win, text="Добавить сотрудника", command=add_employee).pack(pady=10)

    def view_departments():
        def add_department():
            def save_department():
                name = entry_name.get()
                parent_id = entry_parent.get()
                if name:
                    try:
                        cursor.execute("""
                        INSERT INTO Departments (Наименование, РодительскийОтделID) 
                        VALUES (?, ?)
                        """, (name, parent_id))
                        conn.commit()
                        messagebox.showinfo("Успех", "Отдел добавлен!")
                        add_dep_win.destroy()
                        view_departments()
                    except sqlite3.IntegrityError:
                        messagebox.showerror("Ошибка", "Отдел с таким названием уже существует!")
                else:
                    messagebox.showerror("Ошибка", "Заполните название отдела!")

            add_dep_win = Toplevel()
            add_dep_win.title("Добавить отдел")
            add_dep_win.geometry("400x200")

            Label(add_dep_win, text="Наименование отдела:").pack(pady=5)
            entry_name = Entry(add_dep_win)
            entry_name.pack(pady=5)

            Label(add_dep_win, text="Родительский отдел ID (опционально):").pack(pady=5)
            entry_parent = Entry(add_dep_win)
            entry_parent.pack(pady=5)

            ttk.Button(add_dep_win, text="Сохранить", command=save_department).pack(pady=10)

        departments_win = Toplevel()
        departments_win.title("Список отделов")
        departments_win.geometry("600x400")

        tree = ttk.Treeview(departments_win, columns=("ID", "Наименование", "Родительский отдел ID"), show="headings")
        tree.heading("ID", text="ID")
        tree.heading("Наименование", text="Наименование")
        tree.heading("Родительский отдел ID", text="Родительский отдел ID")
        tree.pack(fill=BOTH, expand=True)

        cursor.execute("SELECT * FROM Departments")
        departments = cursor.fetchall()

        for department in departments:
            tree.insert("", "end", values=department)

        ttk.Button(departments_win, text="Добавить отдел", command=add_department).pack(pady=10)

    main_win = Tk()
    main_win.title("Главное окно")
    main_win.geometry("400x300")

    ttk.Button(main_win, text="Список сотрудников", command=view_employees).pack(pady=20)
    ttk.Button(main_win, text="Список отделов", command=view_departments).pack(pady=20)

    main_win.mainloop()

# Запуск приложения
if __name__ == "__main__":
    root = Tk()
    root.title("Приложение")
    root.geometry("300x150")

    ttk.Button(root, text="Войти", command=login_window).pack(pady=20)

    root.mainloop()