import json
import os
import sys

# Store tasks next to this package file to avoid cluttering the repo root
TASKS_FILE = os.path.join(os.path.dirname(__file__), 'tasks.json')


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file)


def add_task(title, description):
    tasks = load_tasks()
    task_id = len(tasks) + 1
    task = {
        'id': task_id,
        'title': title,
        'description': description
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f'Task added: {task}')


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print('No tasks found.')
        return
    for task in tasks:
        print(f"ID: {task['id']}, Title: {task['title']}, Description: {task['description']}")


def main() -> None:
    print("Hello from final!")
    # Allow calling functions programmatically in tests
    if len(sys.argv) < 2:
        print('Usage: python -m final [add|list] [title] [description]')
        return

    command = sys.argv[1]

    if command == 'add':
        if len(sys.argv) != 4:
            print('Usage: python -m final add [title] [description]')
            return
        title = sys.argv[2]
        description = sys.argv[3]
        add_task(title, description)
    elif command == 'list':
        list_tasks()
    else:
        print('Unknown command. Use "add" or "list".')


if __name__ == '__main__':
    main()
