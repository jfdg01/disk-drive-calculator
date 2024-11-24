import pytesseract

from automated_disk_scanner import AutomatedDiskScanner
from constants import START_POS, CELL_SIZE, ROWS, COLS, TESSERACT_PATH

def main():
    # Create and run the automated scanner
    scanner = AutomatedDiskScanner()
    pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH

    print(f"Scanner Parameters:")
    print(f"Starting Position: {START_POS}")
    print(f"Cell Size: {CELL_SIZE}")
    print(f"Grid: {ROWS}x{COLS}")

    # Start scanning sequence
    disk_data = scanner.scan_all_disks()

    print("\nScanning sequence complete!")
    print(f"Total disks scanned: {len(disk_data)}")


if __name__ == "__main__":
    main()
