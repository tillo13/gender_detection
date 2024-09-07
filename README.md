# Face and Gender Detection Project

This project focuses on detecting faces from images and determining their gender and age using machine learning models. Additional scripts are provided to anonymize image filenames and gather details of all Python files within the project directory.

## Project Structure

```
.
│
├── gender_detect
│   ├── opencv_face_detector.pbtxt
│   ├── opencv_face_detector_uint8.pb
│   ├── age_deploy.prototxt
│   ├── age_net.caffemodel
│   ├── gender_deploy.prototxt
│   ├── gender_net.caffemodel
│
├── persons
│   ├── image1.jpg
│   ├── image2.png
│   └── ...
│
├── anonymize_users.py
├── gather_pythons.py
├── gender_detect.py
└── README.md
```

- **Number of Python files:** 3
- **Number of directories:** 3

## Python Scripts

### `anonymize_users.py`

This script anonymizes the filenames of images within the `persons` folder by renaming them to a consistent format (e.g., `person1`, `person2`, etc.), while retaining their original file extensions (e.g., `.jpeg`, `.png`, `.jpg`).

- **Usage:**
  - Place your image files in the `persons` folder.
  - Run the script to rename the image files in a sequence format while keeping the extensions intact.

### `gather_pythons.py`

This script recursively scans the project directory and its subdirectories to gather details of all Python files, excluding specified directories. It outputs the following information into a timestamped file:
- Total number of Python files.
- Total number of directories.
- Directory structure.
- List of all Python file paths.

- **Usage:**
  - Adjust the `DIRECTORIES_TO_EXCLUDE` variable to specify any directories you wish to exclude from the scan.
  - Run `gather_pythons.py` to generate a report of the Python files in the project directory.

### `gender_detect.py`

This script detects faces in the images within the `persons` folder, predicts their gender and age using pre-trained machine learning models, and logs the results to a timestamped CSV file. Key functionalities include:
- Face detection from images.
- Gender prediction with confidence levels.
- Age prediction with confidence levels.
- Logging results into a CSV file named with a timestamp for easy tracking.

- **Usage:**
  - Ensure the `gender_detect` folder contains the required model files.
  - Place your images into the `persons` folder.
  - Run `gender_detect.py` to detect faces, predict age and gender, and generate a CSV report of the results.

### Summary

- **Total Males Detected:**
  - The script counts and outputs the number of male faces detected.
- **Total Females Detected:**
  - The script counts and outputs the number of female faces detected.
- **Image Processing:**
  - Logs the number of images processed from the `persons` folder.
- **CSV Output:**
  - The detailed results, including image name, number of faces detected, gender, and age predictions with confidence levels, are stored in a CSV file with the current timestamp.

## Notes

- To change the image folder location, update the `person_images_folder` variable in the scripts.
- Ensure all required model files are in the appropriate locations as specified in the `gender_detect.py` script.
- Check the console for detailed logs of the operations performed by each script.

This project is designed to be modular and easily extendable, providing a robust framework for face and gender detection tasks.