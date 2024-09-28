import cv2
import numpy as np
from sklearn.linear_model import RANSACRegressor

def load_image(image_path):
    image = cv2.imread(image_path)
    return image

def detect_cones(image):
    # Convert to HSV color space
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define range for red color (cones)
    lower_red = np.array([0, 120, 70])  # Adjust these ranges if needed
    upper_red = np.array([10, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    
    lower_red = np.array([170, 120, 70])  # Second range for red hues
    upper_red = np.array([180, 255, 255])
    mask2 = cv2.inRange(hsv, lower_red, upper_red)
    
    # Combine masks
    mask = mask1 + mask2
    
    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Filter contours based on area
    min_area = 100
    cone_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    return cone_contours

def fit_boundary_lines(image, cone_contours, shift_amount=10):
    centroids = []
    for cnt in cone_contours:
        x, y, w, h = cv2.boundingRect(cnt)
        center_x = x + w // 2
        center_y = y + h // 2
        centroids.append((center_x, center_y))
    
    # Separate left and right cones
    left_cones = [pt for pt in centroids if pt[0] < image.shape[1] // 2]
    right_cones = [pt for pt in centroids if pt[0] >= image.shape[1] // 2]
    
    # Adjust centroids outward
    adjusted_left_cones = [(x - shift_amount, y) for x, y in left_cones]
    adjusted_right_cones = [(x + shift_amount, y) for x, y in right_cones]

    # Fit lines using RANSACRegressor for robustness with fine-tuned residual threshold
    left_model = RANSACRegressor(residual_threshold=3.0).fit(np.array(adjusted_left_cones)[:, 1].reshape(-1, 1), np.array(adjusted_left_cones)[:, 0])
    right_model = RANSACRegressor(residual_threshold=3.0).fit(np.array(adjusted_right_cones)[:, 1].reshape(-1, 1), np.array(adjusted_right_cones)[:, 0])
    
    return left_model, right_model


def draw_boundary_lines(image, left_model, right_model):
    h, w = image.shape[:2]
    
    # Generate points for the lines
    y = np.array([0, h-1])
    left_x = left_model.predict(y.reshape(-1, 1)).astype(int)
    right_x = right_model.predict(y.reshape(-1, 1)).astype(int)
    
    # Ensure the points are within the image boundaries
    left_x = np.clip(left_x, 0, w-1)
    right_x = np.clip(right_x, 0, w-1)
    
    # Draw lines
    cv2.line(image, (left_x[0], 0), (left_x[1], h-1), (0, 0, 255), 2)
    cv2.line(image, (right_x[0], 0), (right_x[1], h-1), (0, 0, 255), 2)
    
    return image

def main():
    input_path = 'original.png'
    output_path = 'answer.png'
    
    # Load image
    image = load_image(input_path)
    
    # Detect cones
    cone_contours = detect_cones(image)
    
    # Fit boundary lines
    left_model, right_model = fit_boundary_lines(image, cone_contours)
    
    # Draw boundary lines
    result = draw_boundary_lines(image.copy(), left_model, right_model)
    
    # Save result
    cv2.imwrite(output_path, result)
    print(f"Successfully processed the image. Result saved as '{output_path}'.")

if __name__ == "__main__":
    main()
