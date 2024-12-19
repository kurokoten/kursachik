import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
import random
import time
import pandas as pd  # Для экспорта в Excel

# Глобальная переменная для хранения текущего пользователя
current_user = None

# Глобальная переменная для хранения текущего языка
current_language = "ru"

# Словарь для текста на разных языках
translations = {
    "ru": {
        "welcome": "Добро пожаловать!",
        "register": "Зарегистрироваться",
        "login": "Войти",
        "username": "Имя пользователя:",
        "password": "Пароль:",
        "admin": "Администратор",
        "user": "Пользователь",
        "balance": "Ваш баланс: ",
        "view_horses": "Просмотреть лошадей",
        "add_horse": "Добавить лошадь",
        "delete_horse": "Удалить лошадь",
        "start_race": "Забег",
        "exit": "Выйти",
        "change_account": "Сменить аккаунт",
        "horse_info": "Информация о лошадях",
        "name": "Имя:",
        "age": "Возраст:",
        "trainer": "Тренер:",
        "owner": "Хозяин:",
        "description": "Описание:",
        "wins": "Победы:",
        "save": "Сохранить",
        "no_horses": "Для забега нужно минимум 2 лошади.",
        "race_started": "Забег начался!",
        "race_winner": "Победитель забега: {}",
        "winner": "Победитель",
        "admin_login_error": "Только администратор может войти с этой учетной записью.",
        "user_login_error": "Пользователь не может войти как администратор.",
        "edit_horse": "Редактировать лошадь",
        "race_history": "История забегов",
        "race_history_empty": "История забегов пуста.",
        "manage_employees": "Управление сотрудниками",
        "add_employee": "Добавить сотрудника",
        "edit_employee": "Редактировать сотрудника",
        "delete_employee": "Удалить сотрудника",
        "employee_name": "Имя сотрудника:",
        "employee_role": "Роль сотрудника:",
        "employee_salary": "Зарплата:",
        "employee_phone": "Номер телефона:",
        "employee_email": "Email:",
        "employee_address": "Адрес:",
        "employee_list": "Список сотрудников",
        "employee_list_empty": "Список сотрудников пуст.",
        "employee_details": "Детали сотрудника",
        "race_finished": "Забег завершен!",
        "race_saved": "Результаты забега сохранены.",
        "back": "Назад",
        "race_results": "Результаты забега",
        "participants": "Участники:",
        "buy_ticket": "Купить билет",
        "ticket_price": "Цена билета: 100 руб.",
        "ticket_bought": "Билет куплен!",
        "insufficient_balance": "Недостаточно средств на балансе.",
        "top_up_balance": "Пополнить баланс",
        "top_up_amount": "Сумма пополнения:",
        "balance_updated": "Баланс обновлен!",
        "horse_details": "Детали лошади",
        "employee_details": "Детали сотрудника",
        "manage_users": "Управление пользователями",
        "user_list": "Список пользователей",
        "user_list_empty": "Список пользователей пуст.",
        "add_balance": "Пополнить баланс",
        "delete_user": "Удалить пользователя",
        "grant_admin": "Сделать администратором",
        "revoke_admin": "Лишить прав администратора",
        "export_to_excel": "Экспорт в Excel",
    },
    "en": {
        "welcome": "Welcome!",
        "register": "Register",
        "login": "Login",
        "username": "Username:",
        "password": "Password:",
        "admin": "Admin",
        "user": "User",
        "balance": "Your balance: ",
        "view_horses": "View Horses",
        "add_horse": "Add Horse",
        "delete_horse": "Delete Horse",
        "start_race": "Race",
        "exit": "Exit",
        "change_account": "Change Account",
        "horse_info": "Horse Information",
        "name": "Name:",
        "age": "Age:",
        "trainer": "Trainer:",
        "owner": "Owner:",
        "description": "Description:",
        "wins": "Wins:",
        "save": "Save",
        "no_horses": "At least 2 horses are required for a race.",
        "race_started": "The race has started!",
        "race_winner": "The race winner is: {}",
        "winner": "Winner",
        "admin_login_error": "Only an admin can log in with this account.",
        "user_login_error": "A user cannot log in as an admin.",
        "edit_horse": "Edit Horse",
        "race_history": "Race History",
        "race_history_empty": "Race history is empty.",
        "manage_employees": "Manage Employees",
        "add_employee": "Add Employee",
        "edit_employee": "Edit Employee",
        "delete_employee": "Delete Employee",
        "employee_name": "Employee Name:",
        "employee_role": "Employee Role:",
        "employee_salary": "Salary:",
        "employee_phone": "Phone Number:",
        "employee_email": "Email:",
        "employee_address": "Address:",
        "employee_list": "Employee List",
        "employee_list_empty": "Employee list is empty.",
        "employee_details": "Employee Details",
        "race_finished": "Race finished!",
        "race_saved": "Race results saved.",
        "back": "Back",
        "race_results": "Race Results",
        "participants": "Participants:",
        "buy_ticket": "Buy Ticket",
        "ticket_price": "Ticket price: 100 rub.",
        "ticket_bought": "Ticket bought!",
        "insufficient_balance": "Insufficient balance.",
        "top_up_balance": "Top Up Balance",
        "top_up_amount": "Top Up Amount:",
        "balance_updated": "Balance updated!",
        "horse_details": "Horse Details",
        "employee_details": "Employee Details",
        "manage_users": "Manage Users",
        "user_list": "User List",
        "user_list_empty": "User list is empty.",
        "add_balance": "Add Balance",
        "delete_user": "Delete User",
        "grant_admin": "Grant Admin Rights",
        "revoke_admin": "Revoke Admin Rights",
        "export_to_excel": "Export to Excel",
    }
}

# Подключение к базе данных SQLite
def connect_db():
    conn = sqlite3.connect("hippodrome.db")
    cursor = conn.cursor()
    # Создаем таблицы, если их нет
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL, -- 'admin' или 'user'
        balance INTEGER DEFAULT 0 -- Баланс пользователя в рублях
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS horses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        trainer TEXT NOT NULL,
        owner TEXT NOT NULL,
        description TEXT NOT NULL,
        wins INTEGER DEFAULT 0
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS races (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        winner_id INTEGER NOT NULL,
        participants TEXT NOT NULL,
        FOREIGN KEY (winner_id) REFERENCES horses (id)
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL, -- Роль: тренер, уборщик и т.д.
        salary INTEGER NOT NULL, -- Зарплата в рублях
        phone TEXT, -- Номер телефона
        email TEXT, -- Email
        address TEXT -- Адрес
    )
    """)
    conn.commit()
    return conn, cursor

# Функция для обработки регистрации
def register():
    username = entry_username.get()
    password = entry_password.get()
    role = "admin" if admin_var.get() else "user"  # Выбор роли через галочку
    if username and password:
        conn, cursor = connect_db()
        cursor.execute("INSERT INTO users (username, password, role, balance) VALUES (?, ?, ?, ?)", (username, password, role, 0))
        conn.commit()
        conn.close()
        messagebox.showinfo("Успех", f"Пользователь {username} зарегистрирован!")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

# Функция для обработки входа
def login():
    global current_user
    username = entry_username.get()
    password = entry_password.get()
    role = "admin" if admin_var.get() else "user"  # Роль, выбранная пользователем
    if username and password:
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            if user[3] == "admin" and role == "user":
                messagebox.showwarning("Ошибка", translations[current_language]["admin_login_error"])
            elif user[3] == "user" and role == "admin":
                messagebox.showwarning("Ошибка", translations[current_language]["user_login_error"])
            else:
                current_user = user  # Сохраняем текущего пользователя
                messagebox.showinfo("Успех", f"Добро пожаловать, {username}!")
                root.withdraw()  # Скрываем окно регистрации
                open_main_window()  # Открываем главное окно
        else:
            messagebox.showwarning("Ошибка", "Неверный логин или пароль.")
    else:
        messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

# Функция для открытия главного окна
def open_main_window():
    global balance_label, user_list  # Объявляем глобальные переменные

    main_window = tk.Toplevel()
    main_window.title("Главное окно")
    main_window.geometry("600x400")  # Уменьшаем размер окна

    # Приветственный текст
    welcome_label = tk.Label(main_window, text=translations[current_language]["welcome"], font=("Arial", 16, "bold"), fg="#2c3e50")
    welcome_label.pack(pady=10)

    # Кнопка для экспорта данных в Excel
    export_button = ttk.Button(main_window, text=translations[current_language]["export_to_excel"], command=export_to_excel)
    export_button.pack(pady=10)

    # Отображение баланса пользователя (только для обычных пользователей)
    if current_user and current_user[3] == "user":
        balance_label = tk.Label(main_window, text=f"{translations[current_language]['balance']} {current_user[4]} руб.", font=("Arial", 14))
        balance_label.pack(pady=5)

    # Запуск обновления баланса в реальном времени
    if current_user and current_user[3] == "user":
        update_balance_in_real_time(balance_label)

    # Создаем табуляцию для навигации
    notebook = ttk.Notebook(main_window)
    notebook.pack(fill=tk.BOTH, expand=True)

    # Вкладка "Лошади"
    horse_frame = tk.Frame(notebook)
    notebook.add(horse_frame, text=translations[current_language]["horse_info"])

    # Вкладка "Сотрудники"
    employee_frame = tk.Frame(notebook)
    notebook.add(employee_frame, text=translations[current_language]["manage_employees"])

    # Вкладка "История забегов"
    race_history_frame = tk.Frame(notebook)
    notebook.add(race_history_frame, text=translations[current_language]["race_history"])

    # Вкладка "Пользователь"
    user_frame = tk.Frame(notebook)
    notebook.add(user_frame, text=translations[current_language]["user"])

    # Вкладка "Управление пользователями" (только для админа)
    if current_user and current_user[3] == "admin":
        manage_users_frame = tk.Frame(notebook)
        notebook.add(manage_users_frame, text=translations[current_language]["manage_users"])
        fill_manage_users_frame(manage_users_frame)

    # Заполняем вкладку "Лошади"
    fill_horse_frame(horse_frame)

    # Заполняем вкладку "Сотрудники"
    fill_employee_frame(employee_frame)

    # Заполняем вкладку "История забегов"
    fill_race_history_frame(race_history_frame)

    # Заполняем вкладку "Пользователь"
    fill_user_frame(user_frame)

    # Кнопки "Выход" и "Сменить аккаунт"
    button_frame = tk.Frame(main_window)
    button_frame.pack(pady=10)

    button_exit = ttk.Button(button_frame, text=translations[current_language]["exit"], command=main_window.destroy)
    button_exit.pack(side=tk.LEFT, padx=10)

    button_change_account = ttk.Button(button_frame, text=translations[current_language]["change_account"], command=lambda: [main_window.destroy(), root.deiconify()])
    button_change_account.pack(side=tk.LEFT, padx=10)

    main_window.mainloop()

# Функция для обновления баланса в реальном времени
def update_balance_in_real_time(label):
    conn, cursor = connect_db()
    cursor.execute("SELECT balance FROM users WHERE id = ?", (current_user[0],))
    balance = cursor.fetchone()[0]
    conn.close()
    label.config(text=f"{translations[current_language]['balance']} {balance} руб.")
    # Повторяем обновление каждые 2 секунды
    label.after(2000, update_balance_in_real_time, label)

# Функция для заполнения вкладки "Лошади"
def fill_horse_frame(frame):
    global horse_list
    horse_list = tk.Listbox(frame, font=("Arial", 12))
    horse_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки для управления лошадями
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    button_add_horse = ttk.Button(button_frame, text=translations[current_language]["add_horse"], command=add_horse)
    button_add_horse.pack(side=tk.LEFT, padx=10)

    button_delete_horse = ttk.Button(button_frame, text=translations[current_language]["delete_horse"], command=delete_horse)
    button_delete_horse.pack(side=tk.LEFT, padx=10)

    button_edit_horse = ttk.Button(button_frame, text=translations[current_language]["edit_horse"], command=edit_horse)
    button_edit_horse.pack(side=tk.LEFT, padx=10)

    button_race = ttk.Button(button_frame, text=translations[current_language]["start_race"], command=start_race)
    button_race.pack(side=tk.LEFT, padx=10)

    # Обновление списка лошадей
    update_horse_list()

    # Обработчик события для отображения деталей лошади
    horse_list.bind("<<ListboxSelect>>", show_horse_details)

# Функция для заполнения вкладки "Сотрудники"
def fill_employee_frame(frame):
    global employee_list
    employee_list = tk.Listbox(frame, font=("Arial", 12))
    employee_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки для управления сотрудниками
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    button_add_employee = ttk.Button(button_frame, text=translations[current_language]["add_employee"], command=add_employee)
    button_add_employee.pack(side=tk.LEFT, padx=10)

    button_edit_employee = ttk.Button(button_frame, text=translations[current_language]["edit_employee"], command=edit_employee)
    button_edit_employee.pack(side=tk.LEFT, padx=10)

    button_delete_employee = ttk.Button(button_frame, text=translations[current_language]["delete_employee"], command=delete_employee)
    button_delete_employee.pack(side=tk.LEFT, padx=10)

    # Обновление списка сотрудников
    update_employee_list()

    # Обработчик события для отображения деталей сотрудника
    employee_list.bind("<<ListboxSelect>>", show_employee_details)

# Функция для заполнения вкладки "История забегов"
def fill_race_history_frame(frame):
    global race_history_list
    race_history_list = tk.Listbox(frame, font=("Arial", 12))
    race_history_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Обновление списка истории забегов
    update_race_history_list()

# Функция для заполнения вкладки "Пользователь"
def fill_user_frame(frame):
    if current_user and current_user[3] == "user":
        balance_label = tk.Label(frame, text=f"{translations[current_language]['balance']} {current_user[4]} руб.", font=("Arial", 14))
        balance_label.pack(pady=10)

        # Кнопка для покупки билета
        button_buy_ticket = ttk.Button(frame, text=translations[current_language]["buy_ticket"], command=buy_ticket)
        button_buy_ticket.pack(pady=10)

        # Кнопка для пополнения баланса
        button_top_up_balance = ttk.Button(frame, text=translations[current_language]["top_up_balance"], command=top_up_balance)
        button_top_up_balance.pack(pady=10)

# Функция для заполнения вкладки "Управление пользователями"
def fill_manage_users_frame(frame):
    global user_list
    user_list = tk.Listbox(frame, font=("Arial", 12))
    user_list.pack(pady=10, fill=tk.BOTH, expand=True)

    # Кнопки для управления пользователями
    button_frame = tk.Frame(frame)
    button_frame.pack(pady=10)

    button_add_balance = ttk.Button(button_frame, text=translations[current_language]["add_balance"], command=add_user_balance)
    button_add_balance.pack(side=tk.LEFT, padx=10)

    button_delete_user = ttk.Button(button_frame, text=translations[current_language]["delete_user"], command=delete_user)
    button_delete_user.pack(side=tk.LEFT, padx=10)

    button_grant_admin = ttk.Button(button_frame, text=translations[current_language]["grant_admin"], command=grant_admin_rights)
    button_grant_admin.pack(side=tk.LEFT, padx=10)

    button_revoke_admin = ttk.Button(button_frame, text=translations[current_language]["revoke_admin"], command=revoke_admin_rights)
    button_revoke_admin.pack(side=tk.LEFT, padx=10)

    # Обновление списка пользователей
    update_user_list()

# Функция для обновления списка лошадей
def update_horse_list():
    horse_list.delete(0, tk.END)
    conn, cursor = connect_db()
    cursor.execute("SELECT name FROM horses")
    horses = cursor.fetchall()
    conn.close()
    for horse in horses:
        horse_list.insert(tk.END, horse[0])

# Функция для обновления списка сотрудников
def update_employee_list():
    employee_list.delete(0, tk.END)
    conn, cursor = connect_db()
    cursor.execute("SELECT name FROM employees")
    employees = cursor.fetchall()
    conn.close()
    for employee in employees:
        employee_list.insert(tk.END, employee[0])

# Функция для обновления списка истории забегов
def update_race_history_list():
    race_history_list.delete(0, tk.END)
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM races")
    races = cursor.fetchall()
    conn.close()
    if not races:
        race_history_list.insert(tk.END, translations[current_language]["race_history_empty"])
    else:
        for race in races:
            cursor.execute("SELECT name FROM horses WHERE id = ?", (race[1],))
            winner_name = cursor.fetchone()[0]
            race_history_list.insert(tk.END, f"Забег ID: {race[0]}, Победитель: {winner_name}, Участники: {race[2]}")

# Функция для обновления списка пользователей
def update_user_list():
    user_list.delete(0, tk.END)
    conn, cursor = connect_db()
    cursor.execute("SELECT username, role, balance FROM users")
    users = cursor.fetchall()
    conn.close()
    if not users:
        user_list.insert(tk.END, translations[current_language]["user_list_empty"])
    else:
        for user in users:
            user_list.insert(tk.END, f"Имя: {user[0]}, Роль: {user[1]}, Баланс: {user[2]} руб.")

# Функция для добавления лошади
def add_horse():
    add_window = tk.Toplevel()
    add_window.title(translations[current_language]["add_horse"])
    add_window.geometry("400x400")

    label_name = tk.Label(add_window, text=translations[current_language]["name"], font=("Arial", 12))
    label_name.pack(pady=5)

    entry_name = tk.Entry(add_window, font=("Arial", 12))
    entry_name.pack(pady=5)

    label_age = tk.Label(add_window, text=translations[current_language]["age"], font=("Arial", 12))
    label_age.pack(pady=5)

    entry_age = tk.Entry(add_window, font=("Arial", 12))
    entry_age.pack(pady=5)

    label_trainer = tk.Label(add_window, text=translations[current_language]["trainer"], font=("Arial", 12))
    label_trainer.pack(pady=5)

    entry_trainer = tk.Entry(add_window, font=("Arial", 12))
    entry_trainer.pack(pady=5)

    label_owner = tk.Label(add_window, text=translations[current_language]["owner"], font=("Arial", 12))
    label_owner.pack(pady=5)

    entry_owner = tk.Entry(add_window, font=("Arial", 12))
    entry_owner.pack(pady=5)

    label_description = tk.Label(add_window, text=translations[current_language]["description"], font=("Arial", 12))
    label_description.pack(pady=5)

    entry_description = tk.Entry(add_window, font=("Arial", 12))
    entry_description.pack(pady=5)

    def save_horse():
        name = entry_name.get()
        age = entry_age.get()
        trainer = entry_trainer.get()
        owner = entry_owner.get()
        description = entry_description.get()
        if name and age and trainer and owner and description:
            conn, cursor = connect_db()
            cursor.execute("""
            INSERT INTO horses (name, age, trainer, owner, description)
            VALUES (?, ?, ?, ?, ?)
            """, (name, age, trainer, owner, description))
            conn.commit()
            conn.close()
            update_horse_list()
            add_window.destroy()
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    button_save = ttk.Button(add_window, text=translations[current_language]["save"], command=save_horse)
    button_save.pack(pady=10)

# Функция для удаления лошади
def delete_horse():
    selected_item = horse_list.curselection()
    if selected_item:
        horse_name = horse_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM horses WHERE name = ?", (horse_name,))
        conn.commit()
        conn.close()
        update_horse_list()
    else:
        messagebox.showwarning("Ошибка", "Выберите лошадь для удаления.")

# Функция для начала забега
def start_race():
    conn, cursor = connect_db()
    cursor.execute("SELECT * FROM horses")
    horses = cursor.fetchall()
    conn.close()
    if len(horses) < 2:
        messagebox.showwarning("Ошибка", translations[current_language]["no_horses"])
        return
    participants = random.sample(horses, min(3, len(horses)))  # Максимум 3 участника
    winner = random.choice(participants)  # Выбираем победителя случайным образом

    # Визуализация забега
    visualize_race(participants, winner)

    # Увеличиваем количество побед у победителя
    conn, cursor = connect_db()
    cursor.execute("UPDATE horses SET wins = wins + 1 WHERE id = ?", (winner[0],))
    conn.commit()

    # Сохраняем результаты забега в базе данных
    participants_names = ", ".join([horse[1] for horse in participants])
    cursor.execute("INSERT INTO races (winner_id, participants) VALUES (?, ?)", (winner[0], participants_names))
    conn.commit()
    conn.close()

    # Показываем результаты забега
    show_race_results(participants, winner)

# Функция для визуализации забега
def visualize_race(participants, winner):
    race_window = tk.Toplevel()
    race_window.title(translations[current_language]["race_started"])
    race_window.geometry("800x400")

    # Создаем полосу для каждой лошади
    horse_bars = []
    for i, horse in enumerate(participants):
        bar = tk.Canvas(race_window, width=600, height=50, bg="white", highlightthickness=0)
        bar.pack(pady=5)
        horse_bars.append(bar)

    # Функция для анимации движения лошади
    def animate_horse(bar, horse_name, speed):
        distance = 0
        def update_distance():
            nonlocal distance
            if distance < 600:
                bar.delete("all")
                bar.create_rectangle(0, 0, distance, 50, fill="blue")
                bar.create_text(distance - 20, 25, text=horse_name, anchor="e", font=("Arial", 12))
                distance += speed
                bar.after(50, update_distance)  # Плавное обновление
            else:
                # Победитель
                if horse_name == winner[1]:
                    bar.create_text(620, 25, text=translations[current_language]["winner"], font=("Arial", 14, "bold"), fill="green")
        update_distance()

    # Запускаем анимацию для каждой лошади
    for i, horse in enumerate(participants):
        speed = random.uniform(1, 5)  # Скорость лошади
        bar = horse_bars[i]
        animate_horse(bar, horse[1], speed)

    # Закрываем окно после завершения забега
    race_window.after(10000, race_window.destroy)

# Функция для отображения результатов забега
def show_race_results(participants, winner):
    results_window = tk.Toplevel()
    results_window.title(translations[current_language]["race_results"])
    results_window.geometry("400x400")

    label_participants = tk.Label(results_window, text=f"{translations[current_language]['participants']}\n{', '.join([horse[1] for horse in participants])}", font=("Arial", 12))
    label_participants.pack(pady=10)

    label_winner = tk.Label(results_window, text=f"{translations[current_language]['winner']}: {winner[1]}", font=("Arial", 14, "bold"), fg="green")
    label_winner.pack(pady=10)

    button_back = ttk.Button(results_window, text=translations[current_language]["back"], command=results_window.destroy)
    button_back.pack(pady=10)

# Функция для добавления сотрудника
def add_employee():
    add_window = tk.Toplevel()
    add_window.title(translations[current_language]["add_employee"])
    add_window.geometry("400x400")

    label_name = tk.Label(add_window, text=translations[current_language]["employee_name"], font=("Arial", 12))
    label_name.pack(pady=5)

    entry_name = tk.Entry(add_window, font=("Arial", 12))
    entry_name.pack(pady=5)

    label_role = tk.Label(add_window, text=translations[current_language]["employee_role"], font=("Arial", 12))
    label_role.pack(pady=5)

    entry_role = tk.Entry(add_window, font=("Arial", 12))
    entry_role.pack(pady=5)

    label_salary = tk.Label(add_window, text=translations[current_language]["employee_salary"], font=("Arial", 12))
    label_salary.pack(pady=5)

    entry_salary = tk.Entry(add_window, font=("Arial", 12))
    entry_salary.pack(pady=5)

    label_phone = tk.Label(add_window, text=translations[current_language]["employee_phone"], font=("Arial", 12))
    label_phone.pack(pady=5)

    entry_phone = tk.Entry(add_window, font=("Arial", 12))
    entry_phone.pack(pady=5)

    label_email = tk.Label(add_window, text=translations[current_language]["employee_email"], font=("Arial", 12))
    label_email.pack(pady=5)

    entry_email = tk.Entry(add_window, font=("Arial", 12))
    entry_email.pack(pady=5)

    label_address = tk.Label(add_window, text=translations[current_language]["employee_address"], font=("Arial", 12))
    label_address.pack(pady=5)

    entry_address = tk.Entry(add_window, font=("Arial", 12))
    entry_address.pack(pady=5)

    def save_employee():
        name = entry_name.get()
        role = entry_role.get()
        salary = entry_salary.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        if name and role and salary and phone and email and address:
            conn, cursor = connect_db()
            cursor.execute("""
            INSERT INTO employees (name, role, salary, phone, email, address)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (name, role, salary, phone, email, address))
            conn.commit()
            conn.close()
            update_employee_list()
            add_window.destroy()
        else:
            messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

    button_save = ttk.Button(add_window, text=translations[current_language]["save"], command=save_employee)
    button_save.pack(pady=10)

# Функция для редактирования сотрудника
def edit_employee():
    selected_item = employee_list.curselection()
    if selected_item:
        employee_name = employee_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM employees WHERE name = ?", (employee_name,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            edit_window = tk.Toplevel()
            edit_window.title(translations[current_language]["edit_employee"])
            edit_window.geometry("400x400")

            label_name = tk.Label(edit_window, text=translations[current_language]["employee_name"], font=("Arial", 12))
            label_name.pack(pady=5)

            entry_name = tk.Entry(edit_window, font=("Arial", 12))
            entry_name.insert(0, employee[1])
            entry_name.pack(pady=5)

            label_role = tk.Label(edit_window, text=translations[current_language]["employee_role"], font=("Arial", 12))
            label_role.pack(pady=5)

            entry_role = tk.Entry(edit_window, font=("Arial", 12))
            entry_role.insert(0, employee[2])
            entry_role.pack(pady=5)

            label_salary = tk.Label(edit_window, text=translations[current_language]["employee_salary"], font=("Arial", 12))
            label_salary.pack(pady=5)

            entry_salary = tk.Entry(edit_window, font=("Arial", 12))
            entry_salary.insert(0, employee[3])
            entry_salary.pack(pady=5)

            label_phone = tk.Label(edit_window, text=translations[current_language]["employee_phone"], font=("Arial", 12))
            label_phone.pack(pady=5)

            entry_phone = tk.Entry(edit_window, font=("Arial", 12))
            entry_phone.insert(0, employee[4])
            entry_phone.pack(pady=5)

            label_email = tk.Label(edit_window, text=translations[current_language]["employee_email"], font=("Arial", 12))
            label_email.pack(pady=5)

            entry_email = tk.Entry(edit_window, font=("Arial", 12))
            entry_email.insert(0, employee[5] if len(employee) > 5 else "")  # Проверка на наличие элемента
            entry_email.pack(pady=5)

            label_address = tk.Label(edit_window, text=translations[current_language]["employee_address"], font=("Arial", 12))
            label_address.pack(pady=5)

            entry_address = tk.Entry(edit_window, font=("Arial", 12))
            entry_address.insert(0, employee[6] if len(employee) > 6 else "")  # Проверка на наличие элемента
            entry_address.pack(pady=5)

            def save_changes():
                name = entry_name.get()
                role = entry_role.get()
                salary = entry_salary.get()
                phone = entry_phone.get()
                email = entry_email.get()
                address = entry_address.get()
                if name and role and salary and phone and email and address:
                    conn, cursor = connect_db()
                    cursor.execute("""
                    UPDATE employees SET name = ?, role = ?, salary = ?, phone = ?, email = ?, address = ?
                    WHERE id = ?
                    """, (name, role, salary, phone, email, address, employee[0]))
                    conn.commit()
                    conn.close()
                    update_employee_list()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

            button_save = ttk.Button(edit_window, text=translations[current_language]["save"], command=save_changes)
            button_save.pack(pady=10)

# Функция для удаления сотрудника
def delete_employee():
    selected_item = employee_list.curselection()
    if selected_item:
        employee_name = employee_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM employees WHERE name = ?", (employee_name,))
        conn.commit()
        conn.close()
        update_employee_list()
    else:
        messagebox.showwarning("Ошибка", "Выберите сотрудника для удаления.")

# Функция для покупки билета
def buy_ticket():
    if current_user and current_user[3] == "user":
        conn, cursor = connect_db()
        cursor.execute("SELECT balance FROM users WHERE id = ?", (current_user[0],))
        balance = cursor.fetchone()[0]
        if balance >= 100:
            cursor.execute("UPDATE users SET balance = balance - 100 WHERE id = ?", (current_user[0],))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", translations[current_language]["ticket_bought"])
        else:
            messagebox.showwarning("Ошибка", translations[current_language]["insufficient_balance"])
    else:
        messagebox.showwarning("Ошибка", "Только пользователи могут покупать билеты.")

# Функция для пополнения баланса
def top_up_balance():
    if current_user and current_user[3] == "user":
        amount = simpledialog.askinteger(translations[current_language]["top_up_balance"], translations[current_language]["top_up_amount"])
        if amount:
            conn, cursor = connect_db()
            cursor.execute("UPDATE users SET balance = balance + ? WHERE id = ?", (amount, current_user[0]))
            conn.commit()
            conn.close()
            messagebox.showinfo("Успех", translations[current_language]["balance_updated"])
    else:
        messagebox.showwarning("Ошибка", "Только пользователи могут пополнять баланс.")

# Функция для редактирования лошади
def edit_horse():
    selected_item = horse_list.curselection()
    if selected_item:
        horse_name = horse_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM horses WHERE name = ?", (horse_name,))
        horse = cursor.fetchone()
        conn.close()
        if horse:
            edit_window = tk.Toplevel()
            edit_window.title(translations[current_language]["edit_horse"])
            edit_window.geometry("400x400")

            label_name = tk.Label(edit_window, text=translations[current_language]["name"], font=("Arial", 12))
            label_name.pack(pady=5)

            entry_name = tk.Entry(edit_window, font=("Arial", 12))
            entry_name.insert(0, horse[1])
            entry_name.pack(pady=5)

            label_age = tk.Label(edit_window, text=translations[current_language]["age"], font=("Arial", 12))
            label_age.pack(pady=5)

            entry_age = tk.Entry(edit_window, font=("Arial", 12))
            entry_age.insert(0, horse[2])
            entry_age.pack(pady=5)

            label_trainer = tk.Label(edit_window, text=translations[current_language]["trainer"], font=("Arial", 12))
            label_trainer.pack(pady=5)

            entry_trainer = tk.Entry(edit_window, font=("Arial", 12))
            entry_trainer.insert(0, horse[3])
            entry_trainer.pack(pady=5)

            label_owner = tk.Label(edit_window, text=translations[current_language]["owner"], font=("Arial", 12))
            label_owner.pack(pady=5)

            entry_owner = tk.Entry(edit_window, font=("Arial", 12))
            entry_owner.insert(0, horse[4])
            entry_owner.pack(pady=5)

            label_description = tk.Label(edit_window, text=translations[current_language]["description"], font=("Arial", 12))
            label_description.pack(pady=5)

            entry_description = tk.Entry(edit_window, font=("Arial", 12))
            entry_description.insert(0, horse[5])
            entry_description.pack(pady=5)

            def save_changes():
                name = entry_name.get()
                age = entry_age.get()
                trainer = entry_trainer.get()
                owner = entry_owner.get()
                description = entry_description.get()
                if name and age and trainer and owner and description:
                    conn, cursor = connect_db()
                    cursor.execute("""
                    UPDATE horses SET name = ?, age = ?, trainer = ?, owner = ?, description = ?
                    WHERE id = ?
                    """, (name, age, trainer, owner, description, horse[0]))
                    conn.commit()
                    conn.close()
                    update_horse_list()
                    edit_window.destroy()
                else:
                    messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля.")

            button_save = ttk.Button(edit_window, text=translations[current_language]["save"], command=save_changes)
            button_save.pack(pady=10)

# Функция для пополнения баланса пользователя
def add_user_balance():
    selected_item = user_list.curselection()
    if selected_item:
        user_info = user_list.get(selected_item)
        username = user_info.split(",")[0].split(":")[1].strip()
        amount = simpledialog.askinteger(translations[current_language]["add_balance"], translations[current_language]["top_up_amount"])
        if amount:
            conn, cursor = connect_db()
            cursor.execute("UPDATE users SET balance = balance + ? WHERE username = ?", (amount, username))
            conn.commit()
            conn.close()
            update_user_list()
            messagebox.showinfo("Успех", translations[current_language]["balance_updated"])
    else:
        messagebox.showwarning("Ошибка", "Выберите пользователя для пополнения баланса.")

# Функция для удаления пользователя
def delete_user():
    selected_item = user_list.curselection()
    if selected_item:
        user_info = user_list.get(selected_item)
        username = user_info.split(",")[0].split(":")[1].strip()
        conn, cursor = connect_db()
        cursor.execute("DELETE FROM users WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        update_user_list()
        messagebox.showinfo("Успех", f"Пользователь {username} удален.")
    else:
        messagebox.showwarning("Ошибка", "Выберите пользователя для удаления.")

# Функция для предоставления прав администратора
def grant_admin_rights():
    selected_item = user_list.curselection()
    if selected_item:
        user_info = user_list.get(selected_item)
        username = user_info.split(",")[0].split(":")[1].strip()
        conn, cursor = connect_db()
        cursor.execute("UPDATE users SET role = 'admin' WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        update_user_list()
        messagebox.showinfo("Успех", f"Пользователь {username} теперь администратор.")
    else:
        messagebox.showwarning("Ошибка", "Выберите пользователя для предоставления прав администратора.")

# Функция для лишения прав администратора
def revoke_admin_rights():
    selected_item = user_list.curselection()
    if selected_item:
        user_info = user_list.get(selected_item)
        username = user_info.split(",")[0].split(":")[1].strip()
        conn, cursor = connect_db()
        cursor.execute("UPDATE users SET role = 'user' WHERE username = ?", (username,))
        conn.commit()
        conn.close()
        update_user_list()
        messagebox.showinfo("Успех", f"Пользователь {username} лишен прав администратора.")
    else:
        messagebox.showwarning("Ошибка", "Выберите пользователя для лишения прав администратора.")

# Функция для отображения деталей лошади
def show_horse_details(event):
    selected_item = horse_list.curselection()
    if selected_item:
        horse_name = horse_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM horses WHERE name = ?", (horse_name,))
        horse = cursor.fetchone()
        conn.close()
        if horse:
            details_window = tk.Toplevel()
            details_window.title(translations[current_language]["horse_details"])
            details_window.geometry("400x400")

            label_name = tk.Label(details_window, text=f"{translations[current_language]['name']}: {horse[1]}", font=("Arial", 12))
            label_name.pack(pady=5)

            label_age = tk.Label(details_window, text=f"{translations[current_language]['age']}: {horse[2]}", font=("Arial", 12))
            label_age.pack(pady=5)

            label_trainer = tk.Label(details_window, text=f"{translations[current_language]['trainer']}: {horse[3]}", font=("Arial", 12))
            label_trainer.pack(pady=5)

            label_owner = tk.Label(details_window, text=f"{translations[current_language]['owner']}: {horse[4]}", font=("Arial", 12))
            label_owner.pack(pady=5)

            label_description = tk.Label(details_window, text=f"{translations[current_language]['description']}: {horse[5]}", font=("Arial", 12))
            label_description.pack(pady=5)

            label_wins = tk.Label(details_window, text=f"{translations[current_language]['wins']}: {horse[6]}", font=("Arial", 12))
            label_wins.pack(pady=5)

# Функция для отображения деталей сотрудника
def show_employee_details(event):
    selected_item = employee_list.curselection()
    if selected_item:
        employee_name = employee_list.get(selected_item)
        conn, cursor = connect_db()
        cursor.execute("SELECT * FROM employees WHERE name = ?", (employee_name,))
        employee = cursor.fetchone()
        conn.close()
        if employee:
            details_window = tk.Toplevel()
            details_window.title(translations[current_language]["employee_details"])
            details_window.geometry("400x400")

            label_name = tk.Label(details_window, text=f"{translations[current_language]['employee_name']}: {employee[1]}", font=("Arial", 12))
            label_name.pack(pady=5)

            label_role = tk.Label(details_window, text=f"{translations[current_language]['employee_role']}: {employee[2]}", font=("Arial", 12))
            label_role.pack(pady=5)

            label_salary = tk.Label(details_window, text=f"{translations[current_language]['employee_salary']}: {employee[3]}", font=("Arial", 12))
            label_salary.pack(pady=5)

            label_phone = tk.Label(details_window, text=f"{translations[current_language]['employee_phone']}: {employee[4]}", font=("Arial", 12))
            label_phone.pack(pady=5)

            label_email = tk.Label(details_window, text=f"{translations[current_language]['employee_email']}: {employee[5]}", font=("Arial", 12))
            label_email.pack(pady=5)

            label_address = tk.Label(details_window, text=f"{translations[current_language]['employee_address']}: {employee[6]}", font=("Arial", 12))
            label_address.pack(pady=5)

# Функция для экспорта данных в Excel
def export_to_excel():
    conn, cursor = connect_db()

    # Экспорт данных из таблицы лошадей
    cursor.execute("SELECT * FROM horses")
    horses_data = cursor.fetchall()
    horses_columns = [description[0] for description in cursor.description]
    horses_df = pd.DataFrame(horses_data, columns=horses_columns)

    # Экспорт данных из таблицы сотрудников
    cursor.execute("SELECT * FROM employees")
    employees_data = cursor.fetchall()
    employees_columns = [description[0] for description in cursor.description]
    employees_df = pd.DataFrame(employees_data, columns=employees_columns)

    # Экспорт данных из таблицы забегов
    cursor.execute("SELECT * FROM races")
    races_data = cursor.fetchall()
    races_columns = [description[0] for description in cursor.description]
    races_df = pd.DataFrame(races_data, columns=races_columns)

    # Экспорт данных из таблицы пользователей
    cursor.execute("SELECT * FROM users")
    users_data = cursor.fetchall()
    users_columns = [description[0] for description in cursor.description]
    users_df = pd.DataFrame(users_data, columns=users_columns)

    conn.close()

    # Создаем Excel-файл
    with pd.ExcelWriter("hippodrome_data.xlsx") as writer:
        horses_df.to_excel(writer, sheet_name="Horses", index=False)
        employees_df.to_excel(writer, sheet_name="Employees", index=False)
        races_df.to_excel(writer, sheet_name="Races", index=False)
        users_df.to_excel(writer, sheet_name="Users", index=False)

    messagebox.showinfo("Успех", "Данные успешно экспортированы в файл hippodrome_data.xlsx")

# Создание главного окна регистрации
root = tk.Tk()
root.title("Регистрационная стойка")
root.geometry("400x450")

# Приветственный текст
welcome_label = tk.Label(root, text=translations[current_language]["welcome"], font=("Arial", 16, "bold"), fg="#2c3e50")
welcome_label.pack(pady=10)

# Поля для ввода
label_username = tk.Label(root, text=translations[current_language]["username"], font=("Arial", 12))
label_username.pack(pady=5)

entry_username = tk.Entry(root, font=("Arial", 12))
entry_username.pack(pady=5)

label_password = tk.Label(root, text=translations[current_language]["password"], font=("Arial", 12))
label_password.pack(pady=5)

entry_password = tk.Entry(root, font=("Arial", 12), show="*")
entry_password.pack(pady=5)

# Галочка для выбора роли
admin_var = tk.BooleanVar()
admin_checkbox = tk.Checkbutton(root, text=translations[current_language]["admin"], variable=admin_var)
admin_checkbox.pack(pady=10)

# Кнопки
button_frame = tk.Frame(root)
button_frame.pack(pady=20)

button_register = ttk.Button(button_frame, text=translations[current_language]["register"], command=register)
button_register.pack(side=tk.LEFT, padx=10)

button_login = ttk.Button(button_frame, text=translations[current_language]["login"], command=login)
button_login.pack(side=tk.LEFT, padx=10)

# Кнопки для переключения языка
language_frame = tk.Frame(root)
language_frame.pack(side=tk.RIGHT, padx=10)

language_button_en = ttk.Button(language_frame, text="EN", command=lambda: change_language("en"))
language_button_en.pack(side=tk.LEFT, padx=5)

language_button_ru = ttk.Button(language_frame, text="RU", command=lambda: change_language("ru"))
language_button_ru.pack(side=tk.LEFT, padx=5)

# Запуск приложения
root.mainloop()