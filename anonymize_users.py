import os

# Specify the folder containing the images
person_images_folder = 'persons'

# List all files in the folder
images = os.listdir(person_images_folder)

# Loop through the files and rename them
for index, img_name in enumerate(images):
    # Split the original filename and its extension
    base, ext = os.path.splitext(img_name)
    
    # New filename with the same extension
    new_name = f"person{index + 1}{ext}"
    
    # Full path for original and new filenames
    old_path = os.path.join(person_images_folder, img_name)
    new_path = os.path.join(person_images_folder, new_name)
    
    # Rename the file
    os.rename(old_path, new_path)
    print(f"Renamed: {img_name} -> {new_name}")

print("All files have been anonymized.")