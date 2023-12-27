






with open("keywords.txt", "r") as file:
    for line in file:
        print(line.strip())  # Remove any trailing newline characters
        input("Press Enter to continue...")
