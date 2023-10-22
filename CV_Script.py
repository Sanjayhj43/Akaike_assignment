# Importing required libraries
import cv2
import numpy as np

def enhance_image(image):
    # Converting the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Enhance the color of the grayscale image using histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_image = clahe.apply(gray_image)

    return enhanced_image

def get_output_image(original_image_path, fully_annotated_image_path, output_image_path):
    # Load the original image and the fully annotated image
    original_image = cv2.imread(original_image_path)
    fully_annotated_image = cv2.imread(fully_annotated_image_path)

    print("Original Image Shape:", original_image.shape)
    print("Fully Annotated Image Shape:", fully_annotated_image.shape)

    # Resize the fully annotated image to match the size of the original image
    fully_annotated_image_resized = cv2.resize(fully_annotated_image, (original_image.shape[1], original_image.shape[0]))

    # Convert the images to multidimensional arrays
    original_image_array = np.array(original_image)
    fully_annotated_image_array = np.array(fully_annotated_image_resized)

    # Separate the left half and right half of the fully annotated image
    width = fully_annotated_image_array.shape[1]
    left_half = fully_annotated_image_array[:, :width // 2, :]
    right_half = fully_annotated_image_array[:, width // 2:, :]

    # Calculate the rate of foreground (ROF) for the fully annotated image
    total_pixels = fully_annotated_image_array.shape[0] * fully_annotated_image_array.shape[1]
    foreground_pixels = np.count_nonzero(fully_annotated_image_array)
    rof = foreground_pixels / total_pixels
    print("Rate of Foreground (ROF):", rof)

    # Copy the annotated region (cat) to the original image
    annotated_part = right_half if rof <= 0.5 else left_half
    original_image_array[:, width // 2:, :] = annotated_part

    # Save the output image
    output_image = cv2.cvtColor(original_image_array, cv2.COLOR_BGR2RGB)
    cv2.imwrite(output_image_path, output_image)

original_image_path = "Path\to\original\image"
fully_annotated_image_path = "path\to\fully\annotated\image"
output_image_path = "path\to\save\partially\annotated\image"

get_output_image(original_image_path, fully_annotated_image_path, output_image_path)