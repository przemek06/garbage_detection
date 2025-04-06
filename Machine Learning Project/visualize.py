import cv2
import os


def draw_bboxes(image_path, label_path, output_path):
    img = cv2.imread(image_path)

    if img is None:
        print(f"Error loading image: {image_path}")
        return

    h, w, _ = img.shape

    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                print(f"Skipping malformed label: {label_path}")
                continue

            class_id, xmin, ymin, xmax, ymax = map(float, parts)
            xmin, ymin, xmax, ymax = int(xmin * w), int(ymin * h), int(xmax * w), int(ymax * h)

            cv2.rectangle(img, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
            cv2.putText(img, str(class_id), (xmin, ymin - 5),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, img)


def visualize_dataset(image_folder, label_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for image_name in os.listdir(image_folder):
        img_path = os.path.join(image_folder, image_name)
        label_name = os.path.splitext(image_name)[0] + ".txt"
        label_path = os.path.join(label_folder, label_name)
        output_path = os.path.join(output_folder, image_name)

        if os.path.exists(label_path):
            draw_bboxes(img_path, label_path, output_path)
        else:
            print(f"No label found for {image_name}, skipping...")