import os
import cv2
import albumentations as A


transform_rotation_1 = A.Compose([
    A.Rotate(limit=180, border_mode=cv2.BORDER_REFLECT, p=1.0)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['category_ids'], min_visibility=0.1))

transform_rotation_2 = A.Compose([
    A.Rotate(limit=90, border_mode=cv2.BORDER_REFLECT, p=1.0)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['category_ids'], min_visibility=0.1))

transform_noise = A.Compose([
    A.ISONoise(color_shift=(0.01, 0.05), intensity=(0.1, 0.5), p=1.0)
], bbox_params=A.BboxParams(format='pascal_voc', label_fields=['category_ids'], min_visibility=0.1))


def read_aabb_labels(label_path):
    bboxes, labels = [], []
    with open(label_path, "r") as f:
        for line in f:
            parts = line.strip().split()
            if len(parts) != 5:
                continue
            class_id, xmin, ymin, xmax, ymax = parts
            bboxes.append([float(xmin), float(ymin), float(xmax), float(ymax)])
            labels.append(class_id)
    return bboxes, labels


def save_labels(label_path, bboxes, labels):
    with open(label_path, "w") as f:
        for bbox, label in zip(bboxes, labels):
            f.write(f"{label} {bbox[0]} {bbox[1]} {bbox[2]} {bbox[3]}\n")


def normalize_bounding_box(im_height, im_width, im_bboxes):
    return [
        [x1 / im_width, y1 / im_height, x2 / im_width, y2 / im_height]
        for x1, y1, x2, y2 in im_bboxes
    ]


def augment_images(image_dir, out_image_dir, out_label_dir):
    for filename in os.listdir(image_dir):
        if not filename.endswith(".jpg"):
            continue

        image_path = os.path.join(image_dir, filename)
        label_path = os.path.join(image_dir, filename.replace(".jpg", ".txt"))

        if not os.path.exists(label_path):
            print(f"Label not found for {filename}")
            continue

        bboxes, class_ids = read_aabb_labels(label_path)

        image = cv2.imread(image_path)
        height, width = image.shape[:2]

        bboxes_pixels = [
            [x1 * width, y1 * height, x2 * width, y2 * height]
            for x1, y1, x2, y2 in bboxes
        ]

        # Save original image and label
        cv2.imwrite(os.path.join(out_image_dir, filename), image)
        save_labels(os.path.join(out_label_dir, filename.replace(".jpg", ".txt")), bboxes, class_ids)

        # Augmentation 1: Rotate 180
        aug1 = transform_rotation_1(image=image, bboxes=bboxes_pixels, category_ids=class_ids)
        fname1 = filename.replace(".jpg", "_rot1.jpg")
        cv2.imwrite(os.path.join(out_image_dir, fname1), aug1['image'])
        save_labels(os.path.join(out_label_dir, fname1.replace(".jpg", ".txt")), normalize_bounding_box(height, width, aug1['bboxes']), aug1['category_ids'])

        # Augmentation 2: Rotate 90
        aug2 = transform_rotation_2(image=image, bboxes=bboxes_pixels, category_ids=class_ids)
        fname2 = filename.replace(".jpg", "_rot2.jpg")
        cv2.imwrite(os.path.join(out_image_dir, fname2), aug2['image'])
        save_labels(os.path.join(out_label_dir, fname2.replace(".jpg", ".txt")), normalize_bounding_box(height, width, aug2['bboxes']), aug2['category_ids'])

        # Augmentation 3: ISO Noise
        aug3 = transform_noise(image=image, bboxes=bboxes_pixels, category_ids=class_ids)
        fname3 = filename.replace(".jpg", "_noise.jpg")
        cv2.imwrite(os.path.join(out_image_dir, fname3), aug3['image'])
        save_labels(os.path.join(out_label_dir, fname3.replace(".jpg", ".txt")), normalize_bounding_box(height, width, aug3['bboxes']), aug3['category_ids'])

    print("Augmentation complete.")
