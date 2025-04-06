import cv2
import os
import numpy as np
import shutil

WHITE_DOT_THRESHOLD = 500
BLACK_BORDER_THRESHOLD = 0.1


def has_black_borders(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

    black_pixels = np.sum(thresh == 0)
    total_pixels = img.shape[0] * img.shape[1]

    black_ratio = black_pixels / total_pixels
    return black_ratio > BLACK_BORDER_THRESHOLD


def contains_bottle_label(label_path):
    """
    Images with white bottle were not removed as part of noise augmented image removal,
    as they were the false positive due to high number of white pixels.
    """
    if not os.path.exists(label_path):
        return False

    with open(label_path, "r") as f:
        labels = f.readlines()

    for label in labels:
        parts = label.strip().split()
        if len(parts) > 0:
            class_id = int(parts[0])
            if class_id == 1:
                return True

    return False


def has_white_dots(image_path):
    img = cv2.imread(image_path)
    if img is None:
        return False

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)  # Detect white dots

    white_pixels = np.sum(thresh == 255)
    return white_pixels > WHITE_DOT_THRESHOLD


def remove_existing_augmented_files(image_folder, label_folder, augmented_folder):
    for filename in os.listdir(image_folder):
        if filename.endswith((".jpg", ".png", ".jpeg")):
            image_path = os.path.join(image_folder, filename)
            label_path = os.path.join(label_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt"))
            augmented_image_path = os.path.join(augmented_folder, filename)
            augmented_label_path = os.path.join(augmented_folder, filename.replace(".jpg", ".txt").replace(".png", ".txt").replace(".jpeg", ".txt"))

            is_bottle = contains_bottle_label(label_path)
            is_augmented = has_black_borders(image_path) or has_white_dots(image_path)

            if not is_bottle and is_augmented:
                shutil.move(image_path, augmented_image_path)
                if os.path.exists(label_path):
                    shutil.move(label_path, augmented_label_path)
                print(f"Moved Augmented Image: {image_path} -> {augmented_folder}")