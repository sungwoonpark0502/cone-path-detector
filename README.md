# Wisconsin Autonomous - Perception

### Result
Original Image            |  Result Image
:-------------------------:|:-------------------------:
![](https://github.com/sungwoonpark0502/cone-path-detector/blob/master/original.png)  |  ![](https://github.com/sungwoonpark0502/cone-path-detector/blob/master/answer.png)

## Project Overview
This project focuses on detecting image traffic cones and fitting boundary lines to demarcate the drivable path using OpenCV and sci-kit-learn.

## Problem Statement
The main objective was to detect red traffic cones and fit lines accurately. The challenge involved ensuring the lines were straight, appropriately placed relative to the detected cones, and adaptive to different scenarios without manual adjustment.

## Approach and Challenges

### Initial Setup
The project began with the implementation of image processing techniques to detect cones. Using the HSV color space was critical because it simplifies color filtering, which is crucial for identifying cones based on their distinct red color.

### Challenges Faced
- **Irregular Cone Detection**: Initially, the detection was inconsistent
- **Line Fitting Issues**: The lines fitted initially were not straight and sometimes were off the cones, which could misguide navigation.

### Solutions Implemented
- **Refining Color Thresholds**: Adjusted the HSV ranges to better accommodate varying lighting conditions, which stabilized cone detection accuracy.
- **Advanced Contour Filtering**: Implemented area-based filtering of contours to ignore small detections that could lead to errors in line fitting.
- **Robust Line Fitting with RANSAC**: Employed RANSACRegressor to fit lines, which is less sensitive to outliers. This approach helped to generate straighter lines.
- **Centroid Adjustment**: Before fitting the lines, the center of the detected cones was adjusted slightly outward (left or right depending on the side). This ensured that the fitted lines did not overlap with the cones and provided a clearer path.

## How It Was Coded

1. **Image Loading**: The image is loaded using the `cv2.imread()` function in the `load_image()` function, which reads the input image in BGR format.

2. **Cone Detection**: The cones are detected in the `detect_cones()` function, where:
   - The image is first converted to the HSV color space using `cv2.cvtColor()` to simplify color-based filtering.
   - Two sets of masks are created to capture the red color in different hue ranges: one for lower reds and another for higher reds. These masks are combined to cover the entire red spectrum.
   - `cv2.findContours()` is used to detect the contours of the cones from the combined mask. Only contours with an area larger than a predefined `min_area` threshold are considered valid cones.

3. **Centroid Calculation and Separation**: In the `fit_boundary_lines()` function:
   - For each detected cone, the bounding rectangle is computed using `cv2.boundingRect()`, and the centroid of each cone is calculated.
   - The centroids are then separated into two groups: left and right, based on their x-coordinate relative to the image center.

4. **Adjusting Centroids**: The centroids are slightly shifted outward (by a `shift_amount`) to avoid the fitted lines intersecting the cones. Left centroids are shifted left, and right centroids are shifted right.

5. **Fitting Boundary Lines**: Using the adjusted centroids, boundary lines are fitted with `RANSACRegressor` from sci-kit-learn:
   - The `RANSACRegressor` is used to fit robust linear models to the left and right cone centroids. The model is fine-tuned using a `residual_threshold` to reduce the impact of outliers on line fitting.

6. **Drawing Boundary Lines**: In the `draw_boundary_lines()` function:
   - The predicted x-values of the boundary lines are generated for the top and bottom of the image using the `predict()` function of the RANSAC models.
   - These lines are then drawn on the image using `cv2.line()`, with red color to indicate the boundaries of the drivable path.

7. **Result Generation**: In the `main()` function:
   - The image is processed through the detection and line fitting functions.
   - The final result, with boundary lines drawn, is saved as a new image using `cv2.imwrite()`.

