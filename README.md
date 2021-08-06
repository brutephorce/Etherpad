# Etherpad
Mediapipe as well as opencv is leveraged in the project.

An virtual drawing screen which can draw anything on it by just capturing the motion of a specified HSV values with a camera. Here a colored object at the tip of the finger is used as the marker. And an ML model is used to detect hands checkpoints.
Color Detection and tracking are used in order to achieve the objective. The color marker is detected and a mask is produced. It includes the further steps of morphological operations on the mask produced which are Erosion and Dilation. Erosion reduces the impurities present in the mask and dilation further restores the eroded main mask.



