import cv2
import os
import csv
from datetime import datetime

# Function to highlight detected faces
def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0,0,i,2]
        if confidence > conf_threshold:
            x1 = int(detections[0,0,i,3] * frameWidth)
            y1 = int(detections[0,0,i,4] * frameHeight)
            x2 = int(detections[0,0,i,5] * frameWidth)
            y2 = int(detections[0,0,i,6] * frameHeight)
            faceBoxes.append([x1,y1,x2,y2])
            cv2.rectangle(frameOpencvDnn, (x1,y1), (x2,y2), (0,255,0), int(round(frameHeight/150)), 8)
    return frameOpencvDnn, faceBoxes

# Initialize counters for male and female detection
male_count = 0
female_count = 0

# Model file paths
faceProto = "gender_detect/opencv_face_detector.pbtxt"
faceModel = "gender_detect/opencv_face_detector_uint8.pb"
ageProto = "gender_detect/age_deploy.prototxt"
ageModel = "gender_detect/age_net.caffemodel"
genderProto = "gender_detect/gender_deploy.prototxt"
genderModel = "gender_detect/gender_net.caffemodel"

MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
genderList = ['Male', 'Female']

# Load models
faceNet = cv2.dnn.readNet(faceModel, faceProto)
ageNet = cv2.dnn.readNet(ageModel, ageProto)
genderNet = cv2.dnn.readNet(genderModel, genderProto)

# Specify the folder containing the images
# Make sure to update this path if you want to change the folder location
person_images_folder = 'persons'
images = os.listdir(person_images_folder)

# Generate CSV filename based on the current timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
csv_filename = f"{timestamp}_results.csv"

with open(csv_filename, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Image Name", "Number of Faces Detected", "Gender", "Gender Confidence (%)", "Age", "Age Confidence (%)"])

    padding = 20
    for img_name in images:
        img_path = os.path.join(person_images_folder, img_name)
        frame = cv2.imread(img_path)
        
        if frame is None:
            print(f"Skipping {img_name}, failed to load.")
            continue

        print("====IMAGE START====")
        print(f"Image name: {img_name}")

        _, faceBoxes = highlightFace(faceNet, frame)
        numberOfFacesDetected = len(faceBoxes)
        if numberOfFacesDetected == 0:
            print("No face detected")
            writer.writerow([img_name, 0, "", "", "", ""])
        else:
            print(f"Number of faces detected: {numberOfFacesDetected}")

        for faceBox in faceBoxes:
            try:
                face = frame[max(0,faceBox[1]-padding):min(faceBox[3]+padding,frame.shape[0]-1),max(0,faceBox[0]-padding):min(faceBox[2]+padding, frame.shape[1]-1)]
                blob = cv2.dnn.blobFromImage(face, 1.0, (227,227), MODEL_MEAN_VALUES, swapRB=False)
                
                # Gender Prediction
                genderNet.setInput(blob)
                genderPreds = genderNet.forward()
                genderClass = genderPreds[0].argmax()
                genderConfidence = genderPreds[0][genderClass]
                gender = genderList[genderClass]

                # Increment the appropriate gender counter
                if gender == "Male":
                    male_count += 1
                else:
                    female_count += 1

                print(f"Gender: {gender}")
                print(f"Gender confidence: {genderConfidence * 100:.2f}%")
                
                # Age Prediction
                ageNet.setInput(blob)
                agePreds = ageNet.forward()
                ageClass = agePreds[0].argmax()
                ageConfidence = agePreds[0][ageClass]
                age = ageList[ageClass]

                print(f"Age: {age[1:-1]} years")
                print(f"Age confidence: {ageConfidence * 100:.2f}%")

                # Write results to CSV
                writer.writerow([img_name, numberOfFacesDetected, gender, f"{genderConfidence * 100:.2f}", age[1:-1], f"{ageConfidence * 100:.2f}"])

            except Exception as e:
                print(f"Error processing face in {img_name}: {str(e)}")
                writer.writerow([img_name, numberOfFacesDetected, "Error", "N/A", "N/A", "N/A"])
        
        print("====IMAGE END====\n")

# Print summary
print("\nSummary:")
print(f"Total Males Detected: {male_count}")
print(f"Total Females Detected: {female_count}")
print(f"Processed images from folder: {person_images_folder}")
print(f"Results saved to: {csv_filename}")
print("\nNote: To change the folder location, update the 'person_images_folder' variable in the script.")