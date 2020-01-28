# Webcam Motion Detection with Face detection
Python Motion detection with separate video between intervals

### Descriptions
Video recording with AVI output recorded when motion is detected. The problem here is some motions are not 
actually a real motion but a shadow of trees and headlights from outside. Therefore, What I am trying to
achieve here is add a face detection or an actual motion detection to see if i can achieve proper motion.

### Requirements
- opencv-python
- numpy

To install requirements:
```python
pip install requirements.txt
```

### Usage
```python
python motion.py
``` 

### TODOs
- Advance motion detection to avoid shadow and headlights of cars from room's window
- Add Face detection to accurate motion due to human
- Optimize code if it is not

### References and Credits:
- https://github.com/richard512/python-security-camera
- https://realpython.com/face-recognition-with-python
