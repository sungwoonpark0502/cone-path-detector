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
- **Robust Line Fitting with RANSAC**: Employed RANSACRegressor to fit lines, which is less sensitive to outliers. This approach helped in generating straighter lines.
- **Centroid Adjustment**: Before fitting the lines, the center of the detected cones were adjusted slightly outward (left or right depending on the side). This ensured that the fitted lines did not overlap with the cones and provided a clearer path.

## Outcomes and Improvements
The adjustments led to a more reliable detection of cones and the fitting of more accurate boundary lines. Future improvements could include implementing dynamic threshold adjustments based on real-time feedback from the environment, enhancing the system’s adaptability.

