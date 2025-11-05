import unittest
from simple_task_cli.cli import add_task, list_tasks
import json
import os

class TestCLI(unittest.TestCase):

    def setUp(self):
        self.test_file = 'test_tasks.json'
        self.original_file = 'tasks.json'
        # Create a test tasks file
        if os.path.exists(self.original_file):
            os.rename(self.original_file, self.test_file)

    def tearDown(self):
        # Restore the original tasks file if it exists
        if os.path.exists(self.test_file):
            os.rename(self.test_file, self.original_file)

    def test_add_task(self):
        task_title = "Test Task"
        task_description = "This is a test task."
        add_task(task_title, task_description)

        with open(self.original_file, 'r') as f:
            tasks = json.load(f)

        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0]['title'], task_title)
        self.assertEqual(tasks[0]['description'], task_description)

    def test_list_tasks(self):
        add_task("Task 1", "Description 1")
        add_task("Task 2", "Description 2")

        tasks = list_tasks()

        self.assertEqual(len(tasks), 2)
        self.assertEqual(tasks[0]['title'], "Task 1")
        self.assertEqual(tasks[1]['title'], "Task 2")

if __name__ == '__main__':
    unittest.main()