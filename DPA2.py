import networkx as nx  # type: ignore
import matplotlib.pyplot as plt
import json        #chatgpt explaining to me how to save the users and connections to txt between code usages
import os


class ConnectionsManager:
    def __init__(self, filename="network_data.txt"):
        self.filename = filename
        self.connections = {}
        self.load_data() 

    def save_data(self):
        with open(self.filename, "w") as file:
            json.dump(self.connections, file)
        print("✅ Data saved successfully.")

#props to :chatgpt,we3schools and codecademy for the json file assistance 
    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as file:
                try:
                    self.connections = json.load(file)
                    print(f"📂 Loaded {len(self.connections)} users from file.")
                except json.JSONDecodeError:
                    self.connections = {}
                    print("⚠️ File was empty or corrupted. Starting fresh.")
        else:
            print("📁 No saved data found. Starting new network.")

    def add_user(self, username):
        if username in self.connections:
            print(f"User '{username}' already exists.")
        else:
            self.connections[username] = []
            self.save_data()
            print(f"User '{username}' added successfully.")

    def add_connection(self, user1, user2):
        if user1 not in self.connections or user2 not in self.connections:
            print("Both users must exist before adding a connection.")
            return
        if user2 in self.connections[user1]:
            print(f"{user1} and {user2} are already connected.")
        else:
            self.connections[user1].append(user2)
            self.connections[user2].append(user1)
            self.save_data()
            print(f"Connection added between {user1} and {user2}.")

    def view_all_users(self):
        if not self.connections:
            print("No users in the network yet.")
        else:
            print("\n All Users ")
            for user in self.connections:
                print(f"- {user}")

    def view_all_connections(self):
        if not self.connections:
            print("No connections found.")
        else:
            print("\n All Connections ")
            for user, friends in self.connections.items():
                print(f"{user}: {', '.join(friends) if friends else 'No connections'}")

    def display_graph(self):
        if not self.connections:
            print("No data to display.")
            return

        G = nx.Graph()
        for user, friends in self.connections.items():
            for friend in friends:
                G.add_edge(user, friend)

        plt.figure(figsize=(8, 6))
        nx.draw_networkx(G, with_labels=True, node_color='lightgreen', node_size=2000, font_size=10)
        plt.title("Social Network Graph")
        plt.show()


def main():
    manager = ConnectionsManager()

    while True:
        print("\n====== SOCIAL MEDIA MANAGER =====")
        print("1. Add User")
        print("2. Add Connection")
        print("3. View All Users")
        print("4. View All Connections")
        print("5. Display Network Graph")
        print("6. Exit")

        choice = input("Enter your choice (1-6): ")

        if choice == "1":
            user = input("Enter username: ").strip()
            manager.add_user(user)

        elif choice == "2":
            user1 = input("Enter first username: ").strip()
            user2 = input("Enter second username: ").strip()
            manager.add_connection(user1, user2)

        elif choice == "3":
            manager.view_all_users()

        elif choice == "4":
            manager.view_all_connections()

        elif choice == "5":
            manager.display_graph()

        elif choice == "6":
            print("💾 Saving and exiting... Goodbye!")
            manager.save_data()
            break

        else:
            print("Invalid choice. Please select a valid option (1–6).")


if __name__ == "__main__":
    main()
