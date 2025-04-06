import bounding_box_conversion as bboxx_conversion
import visualize as v
import remove_augmentation as ra
import augmentation as a


# Converting oriented bounding boxes into axis-aligned bounding boxes
WORKING_DIRECTORY = "E:/Gdansk University/Smester 2/Systems with Machine Learning/Project/Dataset"

input_labels = f"{WORKING_DIRECTORY}/Trash Detection.v14i.yolov8-obb/train/labels"
output_labels = f"{WORKING_DIRECTORY}/Trash Detection.v14i.yolov8-obb/train/labelout"
bboxx_conversion.process_dataset(input_labels, output_labels)

image_folder = f"{WORKING_DIRECTORY}/Trash Detection.v14i.yolov8-obb/train/images"
output_folder = f"{WORKING_DIRECTORY}/Trash Detection.v14i.yolov8-obb/train/imagesout"
v.visualize_dataset(image_folder, output_labels, output_folder)


# Remove existing augmented images from the datasets
image_folder = f"{WORKING_DIRECTORY}/train/images"
label_folder = f"{WORKING_DIRECTORY}/train/labels"
augmented_folder = f"{WORKING_DIRECTORY}/train/Augmented"
ra.remove_existing_augmented_files(image_folder, label_folder, augmented_folder)


# Adding Data augmentation
augmented_folder = f"${WORKING_DIRECTORY}/working folder/Augmentation experiment"
image_dir = f"{augmented_folder}/image"
out_image_dir = f"{augmented_folder}/annotated_image"
out_label_dir = f"{augmented_folder}/annotated_labels"
a.augment_images(image_dir, out_image_dir, out_label_dir)
