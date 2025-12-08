"""
Main CLI application for Python Quest Tracker.
Handles user input, menu navigation, and quest management.
"""

import sys
from tracker import QuestTracker
from utils import generate_quests
from quest import Quest

DATA_FILE = "data/users.json"

def print_menu():
    """Prints the main menu options."""
    print("\n=== Python Quest Tracker ===")
    print("1) Create or switch user")
    print("2) Add a quest manually")
    print("3) Generate quests with AI")
    print("4) List quests")
    print("5) Complete a quest")
    print("6) Save & exit")
    print("0) Exit without saving")

def input_choice(prompt="> "):
    """Safely takes user input and handles EOF/KeyboardInterrupt."""
    try:
        return input(prompt).strip()
    except (EOFError, KeyboardInterrupt):
        return "0"

def main():
    """Main program loop."""
    tracker = QuestTracker(data_file=DATA_FILE)
    current_user = None

    print("Welcome — start by creating or switching to a user.")
    while True:
        if current_user:
            print(f"\nCurrent user: {current_user.username}  |  Points: {current_user.points}")
        print_menu()
        choice = input_choice()

        if choice == "1":
            username = input_choice("Enter username: ")
            if not username:
                print("Username cannot be empty.")
                continue
            created = tracker.add_user(username)
            if created:
                print(f"Created user '{username}'.")
            else:
                print(f"Switched to existing user '{username}'.")
            current_user = tracker.get_user(username)

        elif choice == "2":
            if not current_user:
                print("Create or switch to a user first (option 1).")
                continue
            name = input_choice("Quest name: ")
            if not name:
                print("Quest name cannot be empty.")
                continue
            desc = input_choice("Short description: ")
            pts = input_choice("Points (default 10): ")
            try:
                pts = int(pts) if pts else 10
            except ValueError:
                pts = 10
            q = Quest(name, description=desc, points=pts)
            current_user.add_quest(q)
            print(f"Added quest '{name}'.")

        elif choice == "3":
            if not current_user:
                print("Create or switch to a user first (option 1).")
                continue
            goal = input_choice("Enter a short goal (e.g., 'improve morning routine'): ")
            if not goal:
                print("Goal cannot be empty.")
                continue
            n = input_choice("How many quests to generate? (default 5): ")
            try:
                n = int(n) if n else 5
            except ValueError:
                n = 5
            mode = input_choice("Choose generation mode — 'mock' or 'ai_sim' (default ai_sim): ").lower()
            if mode not in ["mock", "ai_sim"]:
                mode = "ai_sim"
            print(f"Generating quests... (mode={mode})")
            generated = generate_quests(goal, n=n, mode=mode)

            for i, gd in enumerate(generated, 1):
                print(f"\n[{i}] {gd['name']} ({gd['points']} pts)\n    {gd['description']}")

            add_all = input_choice("\nAdd all generated quests to your list? (y/n): ").lower()
            if add_all == "y":
                for gd in generated:
                    q = Quest(gd["name"], description=gd["description"], points=gd["points"])
                    current_user.add_quest(q)
                print(f"Added {len(generated)} quests to {current_user.username}.")
            else:
                pick = input_choice("Enter numbers to add (comma-separated), or press Enter to skip: ")
                if pick:
                    nums = [int(x.strip()) for x in pick.split(",") if x.strip().isdigit()]
                    for idx in nums:
                        if 1 <= idx <= len(generated):
                            gd = generated[idx - 1]
                            q = Quest(gd["name"], description=gd["description"], points=gd["points"])
                            current_user.add_quest(q)
                    print("Selected quests added.")

        elif choice == "4":
            if not current_user:
                print("Create or switch to a user first (option 1).")
                continue
            if not current_user.quests:
                print("No quests found.")
                continue
            print("\nYour quests:")
            for i, q in enumerate(current_user.quests, 1):
                status = "✓" if getattr(q, "completed", False) else " "
                print(f"[{i}] ({status}) {q.name} — {q.points} pts\n    {q.description}")

        elif choice == "5":
            if not current_user or not current_user.quests:
                print("No user or quests available.")
                continue
            idx = input_choice("Enter quest number to mark complete: ")
            if not idx.isdigit():
                print("Invalid input.")
                continue
            idx = int(idx)
            if 1 <= idx <= len(current_user.quests):
                quest = current_user.quests[idx - 1]
                if getattr(quest, "completed", False):
                    print("That quest is already completed.")
                else:
                    current_user.complete_quest(quest.name)
                    print(f"Marked '{quest.name}' complete. +{quest.points} pts")
            else:
                print("Number out of range.")

        elif choice == "6":
            tracker.save_users()
            print("Saved. Goodbye!")
            sys.exit(0)

        elif choice == "0":
            print("Exiting without saving.")
            sys.exit(0)

        else:
            print("Unknown choice — try again.")

if __name__ == "__main__":
    main()
