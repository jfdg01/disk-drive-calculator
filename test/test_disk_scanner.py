import unittest
import os
import json
import itertools
from automated_disk_scanner import AutomatedDiskScanner
import numpy as np
from typing import Dict, List, Tuple
import cv2
import pytesseract
from dataclasses import dataclass
import csv
from datetime import datetime
from tqdm import tqdm


@dataclass
class TestConfig:
    gray_threshold: int
    max_gray_value: int
    psm_value: int
    accuracy: float
    failures: List[str]


class OCRConfigurationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Set up test fixtures before running tests."""
        cls.test_dir = os.path.dirname(os.path.abspath(__file__))
        cls.test_images_dir = os.path.join(cls.test_dir, "test_images")
        cls.reference_data_path = os.path.join(cls.test_dir, "test_disk_data.json")
        cls.results_dir = os.path.join(cls.test_dir, "test_results")
        os.makedirs(cls.results_dir, exist_ok=True)

        # Load reference data
        with open(cls.reference_data_path, 'r') as f:
            cls.reference_data = json.load(f)

        # Pre-load all test images to memory
        cls.test_images = {}
        print("Loading test images...")
        for disk_number in range(1, 15):
            main_path = os.path.join(cls.test_images_dir, f"disk_{disk_number}_main.png")
            sub_path = os.path.join(cls.test_images_dir, f"disk_{disk_number}_sub.png")
            cls.test_images[f"disk_{disk_number}_main"] = cv2.imread(main_path)
            cls.test_images[f"disk_{disk_number}_sub"] = cv2.imread(sub_path)

        # Reduced test configuration ranges for faster testing
        # You can adjust these based on your needs
        cls.gray_thresholds = [75, 100, 125, 150, 175, 200]  # Reduced range
        cls.max_gray_values = [200, 225, 250]  # Reduced range
        cls.psm_values = [6, 7, 8, 11, 12]  # Most commonly useful PSM values

        # Calculate total iterations for progress bar
        cls.total_iterations = (
                len(cls.gray_thresholds) *
                len(cls.max_gray_values) *
                len(cls.psm_values)
        )
        print(f"Will test {cls.total_iterations} configurations...")

    def preprocess_image(self, image: np.ndarray, gray_threshold: int, max_gray_value: int) -> np.ndarray:
        """Preprocess the image with given parameters."""
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, gray_threshold, max_gray_value, cv2.THRESH_BINARY)
        return binary

    def process_disk_images(self, disk_number: int, gray_threshold: int,
                            max_gray_value: int, psm_value: int) -> Dict:
        """Process a single disk's images with given configuration."""
        # Get pre-loaded images
        main_img = self.test_images[f"disk_{disk_number}_main"]
        sub_img = self.test_images[f"disk_{disk_number}_sub"]

        # Process images
        main_binary = self.preprocess_image(main_img, gray_threshold, max_gray_value)
        sub_binary = self.preprocess_image(sub_img, gray_threshold, max_gray_value)

        # OCR processing
        main_text = pytesseract.image_to_string(main_binary, config=f'--psm {psm_value}')
        sub_text = pytesseract.image_to_string(sub_binary, config=f'--psm {psm_value}')

        # Combine and process
        combined_text = main_text + "\n" + sub_text
        return AutomatedDiskScanner.beautify_stats(combined_text)

    def test_configurations(self):
        """Test configurations with progress feedback."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = os.path.join(self.results_dir, f"ocr_results_{timestamp}.csv")
        best_accuracy = 0
        best_config = None

        print("\nStarting configuration tests...")

        with open(results_file, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Gray Threshold', 'Max Gray Value', 'PSM Value',
                             'Accuracy', 'Failed Disks', 'Failure Details'])

            # Create configuration combinations with progress bar
            configs = list(itertools.product(
                self.gray_thresholds,
                self.max_gray_values,
                self.psm_values
            ))

            # Progress bar for configurations
            for gray_threshold, max_gray_value, psm_value in tqdm(configs,
                                                                  desc="Testing configurations", unit="config"):

                successful_disks = 0
                all_failures = []

                # Test each disk with current configuration
                for disk_number in range(1, 15):
                    try:
                        actual_data = self.process_disk_images(
                            disk_number, gray_threshold, max_gray_value, psm_value
                        )
                        expected_data = self.reference_data[f"disk_{disk_number}"]

                        # Simple comparison for speed
                        if (actual_data.get('main_stat', {}).get('value') ==
                                expected_data.get('main_stat', {}).get('value')):
                            successful_disks += 1
                        else:
                            all_failures.append(f"Disk {disk_number}")

                    except Exception as e:
                        all_failures.append(f"Disk {disk_number}: Error")

                # Calculate accuracy
                accuracy = (successful_disks / 14) * 100

                # Update best configuration if needed
                if accuracy > best_accuracy:
                    best_accuracy = accuracy
                    best_config = (gray_threshold, max_gray_value, psm_value, accuracy)
                    print(f"\nNew best configuration found!")
                    print(f"Gray Threshold: {gray_threshold}")
                    print(f"Max Gray Value: {max_gray_value}")
                    print(f"PSM Value: {psm_value}")
                    print(f"Accuracy: {accuracy:.2f}%")

                # Write results
                writer.writerow([
                    gray_threshold,
                    max_gray_value,
                    psm_value,
                    f"{accuracy:.2f}%",
                    14 - successful_disks,
                    '; '.join(all_failures) if all_failures else 'None'
                ])

        # Print final results
        print("\nTesting completed!")
        print(f"Results saved to: {results_file}")
        if best_config:
            print("\nBest configuration found:")
            print(f"Gray Threshold: {best_config[0]}")
            print(f"Max Gray Value: {best_config[1]}")
            print(f"PSM Value: {best_config[2]}")
            print(f"Accuracy: {best_config[3]:.2f}%")


if __name__ == '__main__':
    unittest.main(verbosity=2)