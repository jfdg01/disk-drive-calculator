from disk import Disk

def main():
    print("Welcome to the Disk CLI!")
    while True:
        print("1. Generate Disk")
        print("2. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            disk = Disk()
            disk.display()
        elif choice == "2":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()