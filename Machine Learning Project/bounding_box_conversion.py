import os


def convert_to_aabb(input_path, output_path):
    with open(input_path, "r") as infile, open(output_path, "w") as outfile:
        for line in infile:
            parts = line.strip().split()
            print(f"DEBUG: {parts}")

            if len(parts) != 9:
                print(f"line: {line}")
                continue

            class_id = parts[0]
            try:
                x1, y1, x2, y2, x3, y3, x4, y4 = map(float, parts[1:])
            except ValueError:
                print(f"invalid line: {line}")
                continue

            xmin = min(x1, x2, x3, x4)
            ymin = min(y1, y2, y3, y4)
            xmax = max(x1, x2, x3, x4)
            ymax = max(y1, y2, y3, y4)

            outfile.write(f"{class_id} {xmin} {ymin} {xmax} {ymax}\n")


def process_dataset(input_folder, output_folder):
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(input_folder):
        if filename.endswith(".txt"):
            input_path = os.path.join(input_folder, filename)
            output_path = os.path.join(output_folder, filename)
            convert_to_aabb(input_path, output_path)