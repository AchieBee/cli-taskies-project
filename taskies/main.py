from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, DateTime, Float
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
    sales = relationship("Sale", back_populates="user")

class Sale(Base):
    __tablename__ = 'sales'

    id = Column(Integer, primary_key=True, index=True)
    business_name = Column(String)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="sales")
    amount = Column(Float)

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
    if not task_description or not user_id:
        print(Fore.RED + "Invalid input. Task description and user ID are required.")
        return

    new_task = Task(description=task_description, user_id=user_id, start_time=start_time, end_time=end_time)
    session.add(new_task)
    session.commit()
    print(Fore.GREEN + "Task added successfully.")

# Function to add a user to the database
def add_user_to_db(session, username, phone_number, location):
    if not username or not phone_number or not location:
        print(Fore.RED + "Invalid input. Username, phone number, and location are required.")
        return

    new_user = User(username=username, phone_number=phone_number, location=location)
    session.add(new_user)
    session.commit()
    print(Fore.GREEN + "User added successfully.")

# Function to add a sale to the database
def add_sale_to_db(session, business_name, user_id, amount):
    if not business_name or not user_id or not amount:
        print(Fore.RED + "Invalid input. Business name, user ID, and amount are required.")
        return

    new_sale = Sale(business_name=business_name, user_id=user_id, amount=amount)
    session.add(new_sale)
    session.commit()
    print(Fore.GREEN + "Sale added successfully.")

# Function to remove a user from the database
def remove_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        removed_username = user.username
        session.delete(user)
        session.commit()
        return removed_username
    return None

# Function to remove a task from the database
def remove_task(session, task_id):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        removed_task_description = task.description
        session.delete(task)
        session.commit()
        return removed_task_description
    return None

# Function to update a task in the database
def update_task(session, task_id, updated_description, updated_start_time, updated_end_time):
    task = session.query(Task).filter_by(id=task_id).first()
    if task:
        if updated_description:
            task.description = updated_description
        if updated_start_time:
            task.start_time = updated_start_time
        if updated_end_time:
            task.end_time = updated_end_time
        session.commit()
        return True
    return False

# Function to update a sale in the database
def update_sale(session, sale_id, updated_business_name, updated_amount):
    sale = session.query(Sale).filter_by(id=sale_id).first()
    if sale:
        if updated_business_name:
            sale.business_name = updated_business_name
        if updated_amount is not None:
            sale.amount = updated_amount
        session.commit()
        return True
    return False

# Function to display users
def show_users(session):
    users = session.query(User).all()
    if users:
        print(Fore.GREEN + "User List:")
        for i, user in enumerate(users):
            print(f"{i + 1}. {user.username}, Phone: {user.phone_number}, Location: {user.location}")
    else:
        print(Fore.YELLOW + "User list is empty.")

# Function to display sales
def show_sales(session):
    sales = session.query(Sale).all()
    if sales:
        print(Fore.GREEN + "Sales List:")
        for i, sale in enumerate(sales):
            user_info = f" (User: {sale.user.username})" if sale.user else ""
            print(f"{i + 1}. Business Name: {sale.business_name}{user_info}")
            print(f"   Amount: {sale.amount}")
    else:
        print(Fore.YELLOW + "Sales list is empty.")

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
        print("4. Update a task")
        print("5. Add a user")
        print("6. Remove a user")
        print("7. Update user information")
        print("8. Show users")
        print("9. Add a sale")
        print("10. Update a sale")
        print("11. Show sales")
        print("12. Quit")

        choice = input(Fore.CYAN + "Enter your choice: ")

        if choice == '1':
            show_tasks(session)
        elif choice == '2':
            new_task = input("Enter the task: ")
            user_id = input("Enter the user ID for this task: ")
            start_time = input("Enter the start time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("Enter the end time (YYYY-MM-DD HH:MM:SS): ")
            try:
                user_id = int(user_id)
            except ValueError:
                print(Fore.RED + "Invalid input. User ID must be an integer.")
                continue

            try:
                start_time = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S') if start_time else None
                end_time = datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S') if end_time else None
            except ValueError:
                print(Fore.RED + "Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")
                continue

            add_task_to_db(session, new_task, user_id, "", start_time, end_time)
        elif choice == '3':
            show_tasks(session)
            task_index = input("Enter the task number to remove (or 0 to cancel): ")
            try:
                task_index = int(task_index)
            except ValueError:
                print(Fore.RED + "Invalid input. Task number must be an integer.")
                continue

            removed_task_description = remove_task(session, task_index)
            if removed_task_description:
                print(Fore.GREEN + f"Task '{removed_task_description}' removed successfully.")
            else:
                print(Fore.YELLOW + "Invalid task number.")
        elif choice == '4':
            show_tasks(session)
            task_index = input("Enter the task number to update (or 0 to cancel): ")
            try:
                task_index = int(task_index)
            except ValueError:
                print(Fore.RED + "Invalid input. Task number must be an integer.")
                continue

            updated_description = input("Enter the updated task description: ")
            updated_start_time = input("Enter the updated start time (YYYY-MM-DD HH:MM:SS): ")
            updated_end_time = input("Enter the updated end time (YYYY-MM-DD HH:MM:SS): ")
            try:
                updated_start_time = datetime.strptime(updated_start_time, '%Y-%m-%d %H:%M:%S') if updated_start_time else None
                updated_end_time = datetime.strptime(updated_end_time, '%Y-%m-%d %H:%M:%S') if updated_end_time else None
            except ValueError:
                print(Fore.RED + "Invalid datetime format. Please use YYYY-MM-DD HH:MM:SS.")
                continue

            update_task(session, task_index, updated_description, updated_start_time, updated_end_time)
        elif choice == '5':
            username = input("Enter the username: ")
            phone_number = input("Enter the phone number: ")
            location = input("Enter the location: ")
            add_user_to_db(session, username, phone_number, location)
        elif choice == '6':
            show_users(session)
            user_id = input("Enter the user ID to remove: ")
            try:
                user_id = int(user_id)
            except ValueError:
                print(Fore.RED + "Invalid input. User ID must be an integer.")
                continue

            removed_username = remove_user(session, user_id)
            if removed_username:
                print(Fore.GREEN + f"User '{removed_username}' removed successfully.")
            else:
                print(Fore.YELLOW + "User not found.")
        elif choice == '7':
            show_users(session)
            user_id = input("Enter the user ID to update: ")
            try:
                user_id = int(user_id)
            except ValueError:
                print(Fore.RED + "Invalid input. User ID must be an integer.")
                continue

            updated_username = input("Enter the updated username (or leave blank to skip): ")
            updated_phone_number = input("Enter the updated phone number (or leave blank to skip): ")
            updated_location = input("Enter the updated location (or leave blank to skip): ")
            
            # Update user info
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                if updated_username:
                    user.username = updated_username
                if updated_phone_number:
                    user.phone_number = updated_phone_number
                if updated_location:
                    user.location = updated_location
                session.commit()
                print(Fore.GREEN + "User information updated successfully.")
            else:
                print(Fore.YELLOW + "User not found.")
        elif choice == '8':
            show_users(session)
        elif choice == '9':
            business_name = input("Enter the business name: ")
            user_id = input("Enter the user ID for this sale: ")
            amount = input("Enter the sale amount: ")
            try:
                user_id = int(user_id)
                amount = float(amount)
            except ValueError:
                print(Fore.RED + "Invalid input. User ID must be an integer, and amount must be a float.")
                continue

            add_sale_to_db(session, business_name, user_id, amount)
        elif choice == '10':
            show_sales(session)
            sale_id = input("Enter the sale ID to update: ")
            try:
                sale_id = int(sale_id)
            except ValueError:
                print(Fore.RED + "Invalid input. Sale ID must be an integer.")
                continue

            updated_business_name = input("Enter the updated business name (or leave blank to skip): ")
            updated_amount = input("Enter the updated sale amount (or leave blank to skip): ")
            try:
                updated_amount = float(updated_amount) if updated_amount else None
            except ValueError:
                print(Fore.RED + "Invalid input. Amount must be a float.")
                continue

            update_sale(session, sale_id, updated_business_name, updated_amount)
        elif choice == '11':
            show_sales(session)
        elif choice == '12':
            print(Fore.RESET + Style.RESET_ALL)
            print("Goodbye!")
            break
        else:
            print(Fore.YELLOW + "Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
