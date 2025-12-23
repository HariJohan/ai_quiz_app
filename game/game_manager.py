class GameManager:
    def choose_topic(self):
        print("Enter 1 for SQL Quiz")
        print("Enter 2 for Java Quiz")

        choice = input().strip()

        if choice == "1":
            return "SQL"
        elif choice == "2":
            return "JAVA"
        else:
            print("Invalid choice")
            return None
