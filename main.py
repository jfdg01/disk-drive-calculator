import cv2
import pytesseract
import os
from disk import Disk

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def parse_disk_image(image_path):
    """
    Parse a disk image to extract text.

    :param image_path: Path to the image file.
    :return: Extracted text.
    """
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale for better OCR accuracy
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Optionally apply thresholding or other preprocessing
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

    # Use Tesseract to extract text
    text = pytesseract.image_to_string(binary)
    return text


def parse_all_images(folder_path):
    """
    Parse all images in a folder.

    :param folder_path: Path to the folder containing images.
    :return: Dictionary of filenames and their extracted text.
    """
    parsed_disks = {}
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)
            print(f"Parsing {filename}...")
            text = parse_disk_image(image_path)
            parsed_disks[filename] = text
    return parsed_disks


def main():
    print("Welcome to the Disk CLI!")
    while True:
        print("1. Generate Disk")
        print("2. Parse Disk Image")
        print("3. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            disk = Disk()
            disk.display()
        elif choice == "2":
            folder = "images"
            if os.path.isdir(folder):
                parsed_disks = parse_all_images(folder)
                for file, text in parsed_disks.items():
                    print(f"\n{file}:\n{text}")
        elif choice == "3":
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
    main()
    # generate_best_disk()
