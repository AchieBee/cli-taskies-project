# main.py
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import declarative_base  # Import declarative_base from the correct location

# Define the database engine and create a session
DATABASE_URL = "sqlite:///todo.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

# Define the SQLAlchemy base class
Base = declarative_base()  # Use declarative_base from sqlalchemy.orm

# Define the Task model
class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define a relationship with the User model
    user = relationship("User", back_populates="tasks")

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)

    # Define the one-to-many relationship
    tasks = relationship("Task", back_populates="user")

# Create the database tables
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

def add_task_to_db(session, task_description, user_id):
    new_task = Task(description=task_description, user_id=user_id)
    session.add(new_task)
    session.commit()

def add_user_to_db(session, username, phone_number):
    new_user = User(username=username, phone_number=phone_number)
    session.add(new_user)
    session.commit()

def main():
    session = Session()

    while True:
        print("\nOptions:")
        print("1. Show tasks")
        print("2. Add a task")
        print("3. Remove a task")
        print("4. Add a user")
        print("5. Quit")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_tasks(session)
        elif choice == '2':
            new_task = input("Enter the task: ")
            user_id = int(input("Enter the user ID for this task: "))
            add_task_to_db(session, new_task, user_id)
            print("Task added successfully.")
        elif choice == '3':
            show_tasks(session)
            task_index = int(input("Enter the task number to remove (or 0 to cancel): "))
            if task_index != 0:
                remove_task(session, task_index)
        elif choice == '4':
            username = input("Enter the username: ")
            phone_number = input("Enter the phone number: ")
            add_user_to_db(session, username, phone_number)
            print("User added successfully.")
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

def remove_task(session, task_index):
    tasks = session.query(Task).all()
    if 1 <= task_index <= len(tasks):
        task_to_remove = tasks[task_index - 1]
        session.delete(task_to_remove)
        session.commit()
        return task_to_remove.description
    else:
        return None

if __name__ == "__main__":
    main()
