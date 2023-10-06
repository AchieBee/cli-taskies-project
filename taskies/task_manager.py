# task_manager.py

def read_tasks(file_path):
    try:
        with open(file_path, 'r') as file:
            tasks = file.readlines()
        return [task.strip() for task in tasks]
    except FileNotFoundError:
        return []

def save_tasks(file_path, tasks):
    with open(file_path, 'w') as file:
        file.write('\n'.join(tasks))

def add_task(file_path, task):
    tasks = read_tasks(file_path)
    tasks.append(task)
    save_tasks(file_path, tasks)

def remove_task(file_path, task_index):
    tasks = read_tasks(file_path)
    if 0 <= task_index < len(tasks):
        removed_task = tasks.pop(task_index)
        save_tasks(file_path, tasks)
        return removed_task
    else:
        return None

# Function to remove a user from the database
def remove_user(session, user_id):
    user = session.query(User).filter_by(id=user_id).first()
    if user:
        removed_username = user.username
        session.delete(user)
        session.commit()
        return removed_username
    return None
