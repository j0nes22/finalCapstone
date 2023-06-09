# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.

import os
from datetime import datetime, date

# File names for storing user and task data
tasks_file = "tasks.txt"
users_file = "user.txt"
task_overview_file = "task_overview.txt"
user_overview_file = "user_overview.txt"

# Global variables to store user and task data
users = []
tasks = []

DATETIME_STRING_FORMAT = "%Y-%m-%d"

def main():
    # Prompt for admin login
    admin_username = input("Username: ")
    admin_password = input("Password: ")

    # Check if admin login is successful
    if admin_username == "admin" and admin_password == "password":
        # Load user and task data from files
        load_users()
        load_tasks()

        print("TASK MANAGER")

        while True:
            # Display the menu
            print_menu()
            choice = input("Please select an option:  (r, a, va, vm, gr, ds, e): ")

            # Perform actions based on user's choice
            if choice == "r":
                reg_user()
            elif choice == "a":
                add_task()
            elif choice == "va":
                view_all()
            elif choice == "vm":
                if admin_username == "admin":
                    view_all()
                else:
                    current_user = admin_username
                    view_mine(current_user)
            elif choice == "gr":
                # Check if the tasks file exists
                if os.path.exists(tasks_file):
                    generate_reports()
                    print("Successfully generated reports.")
                else:
                    print("There are no tasks available to generate reports.")
            elif choice == "ds":
                display_statistics()
            elif choice == "e":
                break
            else:
                print("Please try again.")

        # Save user and task data to files
        save_users()
        save_tasks()

    else:
        print("Invalid admin username or password. Exiting the program.")


def print_menu():
    # Print the menu options
    print("\nMenu:")
    print("r. Register User")
    print("a. Add Task")
    print("va. View All Tasks")
    print("vm. View My Tasks")
    print("gr. Generate Reports")
    print("ds. Display Statistics")
    print("e. Exit")


def load_users():
    # Load user data from the file
    global users
    users = []
    if os.path.exists(users_file):
        with open(users_file, "r") as file:
            for line in file:
                # Read each line in the file and extract username and password
                username, password = line.strip().split(";")
                users.append({"username": username, "password": password})


def save_users():
    # Save user data to the file
    with open(users_file, "w") as file:
        for user in users:
            file.write(f"{user['username']};{user['password']}\n")


def login():
    # Prompt the user for username and password and check if it matches any user
    username = input("Username: ")
    password = input("Password: ")

    for user in users:
        if user["username"] == username and user["password"] == password:
            print(f"Welcome, {username}!")
            return username

    print("User not found. Please try again.")
    return None


def reg_user():
    # Register a new user by prompting for username and password
    username = input("New username: ")
    while is_username_taken(username):
        print("Username already exists. Please choose a different username.")
        username = input("New username: ")

    password = input("New password: ")
    users.append({"username": username, "password": password})
    print("User registered successfully.")


def is_username_taken(username):
    # Check if the username is already taken
    for user in users:
        if user["username"] == username:
            return True
    return False


def reg_user():
    # Register a new user by prompting for username and password
    username = input("New username: ")
    while is_username_taken(username):
        print("Username already exists. Please choose a different username.")
        username = input("New username: ")

    password = input("New password: ")
    users.append({"username": username, "password": password})
    save_users()  # Add this line to save the updated user data
    print("User registered successfully.")


def load_tasks():
    # Load task data from the file
    global tasks
    tasks = []
    if os.path.exists(tasks_file):
        with open(tasks_file, "r") as file:
            for line in file:
                # Read each line in the file and extract task data
                task_data = line.strip().split(";")
                tasks.append(
                    {
                        "username": task_data[0],
                        "title": task_data[1],
                        "description": task_data[2],
                        "due_date": task_data[3],
                        "completed": task_data[4],
                    }
                )


def save_tasks():
    # Save task data to the file
    with open(tasks_file, "w") as file:
        for task in tasks:
            file.write(
                f"{task['username']};{task['title']};{task['description']};{task['due_date']};{task['completed']}\n"
            )


def add_task():
    # Add a new task by prompting for task details
    username = input("Username: ")
    title = input("Title of Task: ")
    description = input("Description of Task: ")
    due_date = input("Due date of task (YYYY-MM-DD): ")

    while not is_valid_date(due_date):
        print("Invalid date format. Please enter a valid date in the format YYYY-MM-DD.")
        due_date = input("Due date of task (YYYY-MM-DD): ")

    tasks.append(
        {
            "username": username,
            "title": title,
            "description": description,
            "due_date": due_date,
            "completed": False,
        }
    )
    save_tasks()
    print("Task added successfully.")

def is_valid_date(date_string):
    # Check if the given date string is a valid date in the format YYYY-MM-DD
    try:
        datetime.strptime(date_string, DATETIME_STRING_FORMAT)
        return True
    except ValueError:
        return False



def view_all():
    # View all tasks
    if len(tasks) == 0:
        print("No tasks available.")
    else:
        print("All Tasks:")
        for index, task in enumerate(tasks, start=1):
            print(f"{index}. {task['title']} assigned to {task['username']}")


def view_mine(current_user):
    # View tasks assigned to the admin user
    admin_tasks = [task for task in tasks if task["username"] == "admin"]
    if len(admin_tasks) == 0:
        print("No tasks assigned to the admin.")
    else:
        print("Admin Tasks:")
        for index, task in enumerate(admin_tasks, start=1):
            print(f"{index}. {task['title']}, Due: {task['due_date']}, Completed: {task['completed']}")

        task_choice = input("Select a task number to mark as complete or edit (-1 to return to the main menu): ")
        if task_choice.isdigit():
            task_index = int(task_choice) - 1
            if task_index >= 0 and task_index < len(admin_tasks):
                selected_task = admin_tasks[task_index]
                mark_or_edit_task(selected_task)
            elif task_index == -1:
                return
            else:
                print("Invalid task number.")
        else:
            print("Invalid input.")


def mark_or_edit_task(task):
    # Mark a task as complete or edit the task
    if task["completed"] == "Yes":
        print("This task is already completed.")
        return

    print("Select an option:")
    print("1. Mark task as complete")
    print("2. Edit task")
    choice = input("Enter your choice: ")

    if choice == "1":
        task["completed"] = True

        save_tasks()
        print("Task marked as complete.")
    elif choice == "2":
        if task["completed"] == "No":
            new_username = input("Enter new username (or press Enter to keep current username): ")
            new_due_date = input("Enter new due date (YYYY-MM-DD) (or press Enter to keep current due date): ")

            if new_username:
                task["username"] = new_username
            if new_due_date:
                task["due_date"] = new_due_date

            save_tasks()
            print("Task edited successfully.")
        else:
            print("Cannot edit a completed task.")
    else:
        print("Invalid choice.")


def generate_reports():
    # generate reports and display statistics
    total_tasks = len(tasks)
    completed_tasks = sum(task.get("completed") == "Yes" or task.get("completed") == 1 for task in tasks)
    uncompleted_tasks = total_tasks - completed_tasks
    overdue_tasks = sum(
        (
            (task.get("completed") is False)
            and task.get("due_date")
            and datetime.strptime(task.get("due_date"), DATETIME_STRING_FORMAT).date() < date.today()
        )
        for task in tasks
    )

    incomplete_percentage = (uncompleted_tasks / total_tasks) * 100 if total_tasks > 0 else 0
    overdue_percentage = (overdue_tasks / total_tasks) * 100 if total_tasks > 0 else 0

    task_overview = f"Task Overview:\n" \
                    f"Total tasks: {total_tasks}\n" \
                    f"Completed tasks: {completed_tasks}\n" \
                    f"Uncompleted tasks: {uncompleted_tasks}\n" \
                    f"Overdue tasks: {overdue_tasks}\n" \
                    f"Incomplete task percentage: {incomplete_percentage:.2f}%\n" \
                    f"Overdue task percentage: {overdue_percentage:.2f}%"

    with open(task_overview_file, "w") as file:
        file.write(task_overview)

    users_overview = "Users Overview:\n\n"
    for user in users:
        user_tasks = [task for task in tasks if task.get("username") == user.get("username")]
        user_total_tasks = len(user_tasks)
        user_completed_tasks = sum(task.get("completed") in [True, 1, "Yes"] for task in user_tasks)
        user_uncompleted_tasks = user_total_tasks - user_completed_tasks
        user_overdue_tasks = sum(
            (
                (task.get("completed") is False)
                and task.get("due_date")
                and task.get("due_date") != ''
                and datetime.strptime(task.get("due_date"), DATETIME_STRING_FORMAT).date() < date.today()
            )
            for task in user_tasks
        )

        user_assigned_tasks_percentage = (user_total_tasks / total_tasks) * 100 if total_tasks > 0 else 0
        user_completed_tasks_percentage = (user_completed_tasks / user_total_tasks) * 100 if user_total_tasks > 0 else 0
        user_uncompleted_tasks_percentage = (
            user_uncompleted_tasks / user_total_tasks
        ) * 100 if user_total_tasks > 0 else 0
        user_overdue_tasks_percentage = (user_overdue_tasks / user_total_tasks) * 100 if user_total_tasks > 0 else 0

        user_report = f"Username: {user.get('username')}\n" \
                      f"Total tasks assigned: {user_total_tasks}\n" \
                      f"Percentage of total tasks assigned: {user_assigned_tasks_percentage:.2f}%\n" \
                      f"Percentage of completed tasks: {user_completed_tasks_percentage:.2f}%\n" \
                      f"Percentage of uncompleted tasks: {user_uncompleted_tasks_percentage:.2f}%\n" \
                      f"Percentage of overdue tasks: {user_overdue_tasks_percentage:.2f}%\n\n"

        users_overview += user_report

    with open(user_overview_file, "w") as file:
        file.write(users_overview)


def display_statistics():
    if os.path.exists(task_overview_file):
        with open(task_overview_file, "r") as file:
            task_overview = file.read()
            print(task_overview)
    else:
        print("No task overview available.")

    if os.path.exists(user_overview_file):
        with open(user_overview_file, "r") as file:
            users_overview = file.read()
            print(users_overview)
    else:
        print("No user overview available.")


# Run the main function to start the program
if __name__ == "__main__":
    main()


