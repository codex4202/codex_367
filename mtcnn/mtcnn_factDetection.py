from mtcnn import MTCNN
import cv2
import matplotlib.pyplot as plt
import os
import json

def detect_faces_and_draw(image_path, save_cropped=True, save_image=False, output_dir="output", confidence_threshold=0.9):
    # Read the image
    image = cv2.imread(image_path)
    if image is None:
        print("Error: Unable to load image. Check the file path.")
        return
    
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    detector = MTCNN()
    faces = detector.detect_faces(image_rgb)
    
    if not faces:
        print("No faces detected.")
        return
    
    # Check if user wants to save cropped outputs
    save_cropped = input("Do you want to save the cropped outputs? (1 for yes, 0 for no): ").strip()
    save_cropped = save_cropped == "1"
    
    if save_cropped:
        output_dir = input("Enter the directory to save outputs (default: 'output'): ").strip() or "output"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    face_count = 0
    face_data = []
    for face in faces:
        confidence = face['confidence']
        if confidence < confidence_threshold:
            continue
        
        face_count += 1
        x, y, width, height = face['box']
        face_data.append({
            "bounding_box": [int(x), int(y), int(width), int(height)],
            "confidence": float(confidence),
            "keypoints": {key: [int(coord) for coord in point] for key, point in face['keypoints'].items()}
        })
        
        # Draw bounding box
        cv2.rectangle(image_rgb, (x, y), (x + width, y + height), (0, 255, 0), 2)
        
        # Draw landmarks
        for key, point in face['keypoints'].items():
            cv2.circle(image_rgb, (int(point[0]), int(point[1])), 2, (255, 0, 0), -1)
        
        # Save cropped face if the user opted in
        if save_cropped:
            face_crop = image_rgb[y:y + height, x:x + width]
            face_filename = os.path.join(output_dir, f"face_{face_count}.jpg")
            cv2.imwrite(face_filename, cv2.cvtColor(face_crop, cv2.COLOR_RGB2BGR))
            print(f"Cropped face saved to {face_filename}")
    
    print(f"Detected {face_count} faces.")
    
    # Save face data to JSON
    if save_cropped:
        face_data_filename = os.path.join(output_dir, "face_data.json")
        with open(face_data_filename, "w") as json_file:
            json.dump(face_data, json_file, indent=4)
        print(f"Detection details saved to {face_data_filename}")
    
    # Ask to save processed image
    if save_image:
        save_processed = input("Do you want to save the processed image with detections? (yes/no): ").strip().lower()
        if save_processed == "yes":
            processed_image_path = os.path.join(output_dir, "processed_image.jpg")
            cv2.imwrite(processed_image_path, cv2.cvtColor(image_rgb, cv2.COLOR_RGB2BGR))
            print(f"Processed image saved to {processed_image_path}")
    
    # Display the image with detections
    plt.figure(figsize=(10, 10))
    plt.imshow(image_rgb)
    plt.axis('off')
    plt.show()

def main():
    image_path = input("Enter the path of the image for face detection: ")
    confidence_threshold = float(input("Enter confidence threshold (default: 0.9): ") or 0.9)
    save_image = input("Do you want to save the processed image? (yes/no, default: no): ").strip().lower() == 'yes'
    detect_faces_and_draw(image_path, save_image=save_image, confidence_threshold=confidence_threshold)

if __name__ == "__main__":
    main()
