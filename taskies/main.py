from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Database URL
DATABASE_URL = "sqlite:///todo.db"

# Create a database engine
engine = create_engine(DATABASE_URL)

# Create a session
Session = sessionmaker(bind=engine)

# Create a base class for declarative models
Base = declarative_base()

# Define the Task and User models
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")
    start_time = Column(DateTime)
    end_time = Column(DateTime)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    location = Column(String)
    tasks = relationship("Task", back_populates="user")

# Function to display tasks
def show_tasks(session):
    tasks = session.query(Task).all()
    if tasks:
        print(Fore.GREEN + "Your todo list:")
        for i, task in enumerate(tasks):
            if task.user:
                owner_info = f" (Owner: {task.user.username})"
            else:
                owner_info = ""
            start_time = task.start_time.strftime('%Y-%m-%d %H:%M:%S') if task.start_time else "Not started"
            end_time = task.end_time.strftime('%Y-%m-%d %H:%M:%S') if task.end_time else "Not completed"
            print(f"{i + 1}. {task.description}{owner_info}")
            print(f"   Start Time: {start_time}, End Time: {end_time}")
    else:
        print(Fore.YELLOW + "Your todo list is empty.")

# Function to add a task to the database
def add_task_to_db(session, task_description, user_id, location, start_time=None, end_time=None):
    new_task = Task(description=task_description, user_id=user_id, start_time=start_time, end_time=end_time)
    session.add(new_task)
    session.commit()

# Function to add a user to the database
def add_user_to_db(session, username, phone_number, location):
    new_user = User(username=username, phone_number=phone_number, location=location)
    session.add(new_user)
    session.commit()

# Function to remove a task from the database
def remove_task(session, task_index):
    tasks = session.query(Task).all()
    if 1 <= task_index <= len(tasks):
        task_to_remove = tasks[task_index - 1]
        session.delete(task_to_remove)
        session.commit()
        return task_to_remove.description
    else:
        return None

# Function to remove a user from the database
def remove_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        username = user.username
        session.delete(user)
        session.commit()
        return username
    else:
        return None

# Function to display users
def show_users(session):
    users = session.query(User).all()
    if users:
        print(Fore.CYAN + "List of Users:")
        for user in users:
            print(f"ID: {user.id}, Username: {user.username}, Phone Number: {user.phone_number}, Location: {user.location}")
    else:
        print(Fore.YELLOW + "No users found.")

# Create database tables
Base.metadata.create_all(bind=engine)

# Main session
def main():
    session = Session()

    # Welcome message
    print(Fore.CYAN + Style.BRIGHT + "Welcome to Taskies - Your Personal Task Manager\n")

    while True:
        print(Fore.RESET + Style.RESET_ALL)
        print("Options:")
        print("1. Show tasks")
        print("2. Add a task")
        print("3. Remove a task")
        print("4. Add a user")
        print("5. Remove a user")
        print("6. Show users")  # Added option to show users
        print("7. Quit")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == '1':
            show_tasks(session)
        elif choice == '2':
            new_task = input("Enter the task: ")
            user_id = int(input("Enter the user ID for this task: "))
            start_time = input("Enter the start time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("Enter the end time (YYYY-MM-DD HH:MM:SS): ")
            start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') if start_time else None
            end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else None
            add_task_to_db(session, new_task, user_id, "", start_time, end_time)
            print(Fore.GREEN + "Task added successfully.")
        elif choice == '3':
            show_tasks(session)
            task_index = int(input("Enter the task number to remove (or 0 to cancel): "))
            if task_index != 0:
                removed_task_description = remove_task(session, task_index)
                if removed_task_description:
                    print(Fore.GREEN + f"Task '{removed_task_description}' removed successfully.")
                else:
                    print(Fore.YELLOW + "Invalid task number.")
        elif choice == '4':
            username = input("Enter the username: ")
            phone_number = input("Enter the phone number: ")
            location = input("Enter the location: ")
            add_user_to_db(session, username, phone_number, location)
            print(Fore.GREEN + "User added successfully.")
        elif choice == '5':
            user_id = int(input("Enter the user ID to remove: "))
            removed_username = remove_user(session, user_id)
            if removed_username:
                print(Fore.GREEN + f"User '{removed_username}' removed successfully.")
            else:
                print(Fore.YELLOW + "User not found.")
        elif choice == '6':
            show_users(session)  # Show users when '6' is selected
        elif choice == '7':
            print(Fore.RESET + Style.RESET_ALL)
            print("Goodbye!")
            break
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
