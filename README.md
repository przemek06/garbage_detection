# Garbage Detection
## Data Collection Instruction
1. Each team member finds one dataset.
2. Let's use the following classes and their integer representation in ():
   - Plastic (0)
   - Paper (1)
   - Glass (2)
   - Metal (3)
   - Other (4)
3. Directory structure:
   - /images
   - /labels
4. Each image should have the same name as its corresponding label
5. Rename each pair of image and label to:
   - [class_number]_[random_uuid].extension in case of single instance in the picture
   - multiclass_[random_uuid].extension otherwise
6. Let's use JPG image file extension and .txt label file extension
7. Labels should have a common standard:
   - Each instance of an object in the image corresponds to a single line in the label file
   - xmin means most leftwards pixel of the object, ymax means most bottom pixel of the object, etc.
   - We use integer representation for class_number
   - We use double/float representation for xmin, ymin, xmax, ymax between 0.0 and 1.0 so that each of them represents relative position of a pixel in the picutre. Then given the picture's width and height we can calculate an absoulute position of the pixel.
   - Each line has the following structure:
```
[class_number] [xmin] [ymin] [xmax] [ymax]
```
8. We also need to split work for the first 5 points of the report:
   - **Describe data you need** - each team member is responsible for their data
   - **Collect the data** - each team member should collectg data according to above specification. Next, one team member needs to write Python scripts to calculate some statistics about data + make some plots.
   - **Analyze relations and correlations within the data** - one team member should do this point
   - **Analyze noise and errors** - one team member should do this point
   - **Check if some data is "more difficult" or "more important" than the other** - one team member should do this point

 
