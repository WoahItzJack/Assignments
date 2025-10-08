import heapq
import os
from datetime import datetime

class Task:
    def __init__(self, description, due_date, priority, est_time):
        self.description = description
        self.due_date = due_date  
        self.priority = priority
        self.est_time = est_time

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.due_date < other.due_date
        return self.priority < other.priority

    def display(self):
        print(f"Task: {self.description}")
        print(f"Due Date: {self.due_date.isoformat()}")
        print(f"Priority: {self.priority}")
        print(f"Estimated Time: {self.est_time} hours")
        print("-" * 40)

    def __str__(self):
        return f"{self.description} | {self.due_date.isoformat()} | {self.priority} | {self.est_time}h"


class Scheduler:
    def __init__(self, filename="tasks.txt"):
        self.tasks = []
        self.filename = filename
        self.load_tasks()  

    def add_task(self, task):
        heapq.heappush(self.tasks, task)
        self.save_tasks()

    def get_next_task(self):
        if self.tasks:
            task = heapq.heappop(self.tasks)
            self.save_tasks()
            return task
        else:
            print("No tasks available.")
            return None

    def print_tasks(self):
        if not self.tasks:
            print("No tasks in the scheduler.")
        else:
            print("\n--- Task List (by priority, then due date) ---")
            for task in sorted(self.tasks):
                task.display()

    def save_tasks(self):
        with open(self.filename, "w") as f:
            for task in sorted(self.tasks):
                f.write(str(task) + "\n")

    def load_tasks(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                for line in f:
                    parts = line.strip().split(" | ")
                    if len(parts) == 4:
                        desc, due, priority, est_time = parts
                        try:
                            due_date = datetime.strptime(due, "%Y-%m-%d").date()
                        except ValueError:
                            continue
                        priority = int(priority)
                        est_time = float(est_time.replace("h", ""))
                        task = Task(desc, due_date, priority, est_time)
                        heapq.heappush(self.tasks, task)


def main():
    scheduler = Scheduler()
    while True:
        print("\n--- Task Scheduler Menu ---")
        print("1. Add Task")
        print("2. View Next Task")
        print("3. Print All Tasks")
        print("4. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            desc = input("Enter task description: ")
            due_date_input = input("Enter due date (YYYY-MM-DD): ")
            try:
                due_date = datetime.strptime(due_date_input, "%Y-%m-%d").date()
            except ValueError:
                print("Invalid date format! Use YYYY-MM-DD.")
                continue

            try:
                priority = int(input("Enter priority (smaller number = higher priority): "))
                est_time = float(input("Enter estimated time to complete (hours): "))
            except ValueError:
                print("Priority must be an integer, and time must be a number.")
                continue

            task = Task(desc, due_date, priority, est_time)
            scheduler.add_task(task)

        elif choice == "2":
            task = scheduler.get_next_task()
            if task:
                print("\n--- Next Task ---")
                task.display()

        elif choice == "3":
            scheduler.print_tasks()

        elif choice == "4":
            print("Exiting. Cheers Mate!")
            break

        else:
            print("Invalid choice. Please try again.")
if __name__ == "__main__":
    main()
