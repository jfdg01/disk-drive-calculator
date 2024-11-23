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

def generate_best_disk(num_disks=100):
    best_disk = None
    best_score = -float('inf')  # Start with a very low score

    # Generate 'num_disks' number of disks and evaluate each one
    for _ in range(num_disks):
        disk = Disk()  # Generate a new disk
        # disk.display()  # Display the disk details (optional, for debugging)

        # Evaluate the disk
        evaluation = disk.evaluate()
        total_score = evaluation["Total Score"]

        # Update the best disk if the current one has a higher total score
        if total_score > best_score:
            best_score = total_score
            best_disk = disk

    # After generating and evaluating all disks, display the best one
    print("\nBest Disk:")
    best_disk.display()  # Display the best disk's details

if __name__ == "__main__":
    # main()
    generate_best_disk()