from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base

DATABASE_URL = "sqlite:///todo.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship("User", back_populates="tasks")

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    location = Column(String)  # Add the "location" column
    tasks = relationship("Task", back_populates="user")

Base.metadata.create_all(bind=engine)

def show_tasks(session):
    tasks = session.query(Task).all()
    if tasks:
        print("Your todo list:")
        for i, task in enumerate(tasks):
            if task.user:
                owner_info = f" (Owner: {task.user.username})"
            else:
                owner_info = ""
            print(f"{i + 1}. {task.description}{owner_info}")
    else:
        print("Your todo list is empty.")

def show_users(session):
    users = session.query(User).all()
    if users:
        print("Users:")
        for user in users:
            print(f"Username: {user.username}, Phone Number: {user.phone_number}, Location: {user.location}")
    else:
        print("No users found.")

def add_task_to_db(session, task_description, user_id, location):
    new_task = Task(description=task_description, user_id=user_id)
    session.add(new_task)
    session.commit()

def add_user_to_db(session, username, phone_number, location):
    new_user = User(username=username, phone_number=phone_number, location=location)
    session.add(new_user)
    session.commit()

def remove_task(session, task_index):
    tasks = session.query(Task).all()
    if 1 <= task_index <= len(tasks):
        task_to_remove = tasks[task_index - 1]
        session.delete(task_to_remove)
        session.commit()
        return task_to_remove.description
    else:
        return None

def remove_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        username = user.username
        session.delete(user)
        session.commit()
        return username
    else:
        return None

def main():
    session = Session()

    while True:
        print("\nOptions:")
        print("1. Show tasks")
        print("2. Add a task")
        print("3. Remove a task")
        print("4. Add a user")
        print("5. Remove a user")
        print("6. Show users")  # Added option to show users
        print("7. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks(session)
        elif choice == '2':
            new_task = input("Enter the task: ")
            user_id = int(input("Enter the user ID for this task: "))
            add_task_to_db(session, new_task, user_id, "")  # Pass an empty location for tasks
            print("Task added successfully.")
        elif choice == '3':
            show_tasks(session)
            task_index = int(input("Enter the task number to remove (or 0 to cancel): "))
            if task_index != 0:
                removed_task_description = remove_task(session, task_index)
                if removed_task_description:
                    print(f"Task '{removed_task_description}' removed successfully.")
                else:
                    print("Invalid task number.")
        elif choice == '4':
            username = input("Enter the username: ")
            phone_number = input("Enter the phone number: ")
            location = input("Enter the location: ")  # Prompt for location
            add_user_to_db(session, username, phone_number, location)
            print("User added successfully.")
        elif choice == '5':
            user_id = int(input("Enter the user ID to remove: "))
            removed_username = remove_user(session, user_id)
            if removed_username:
                print(f"User '{removed_username}' removed successfully.")
            else:
                print("User not found.")
        elif choice == '6':
            show_users(session)  # Show users option
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
