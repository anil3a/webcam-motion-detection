# coding=utf-8
"""
Webcam motion detection
"""
import cv2
import numpy as np

THRESHOLD = 40
camera = cv2.VideoCapture(0)

es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
kernel = np.ones((5, 5), np.uint8)
background = None

# Write video
fps = 30  # camera.get(cv2.CAP_PROP_FPS)
size = (int(camera.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT)))
recordVideo = loopEndCount = 0
videoWriter = cv2.VideoWriter('videos/motion1.avi',
                              cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
                              fps, size)
counter = 0
fileNameIncrement = 1

while True:
    ret, frame = camera.read()
    # The first frame as the background
    if background is None:
        background = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        background = cv2.GaussianBlur(background, (21, 21), 0)
        continue

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)

    # Compare the difference between each frame of image and the background
    diff = cv2.absdiff(background, gray_frame)
    diff = cv2.threshold(diff, THRESHOLD, 255, cv2.THRESH_BINARY)[1]
    diff = cv2.dilate(diff, es, iterations=2)
    # Calculate the outline of the target in the image
    cnts, hierarchy = cv2.findContours(diff.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Counts of Motion Detection
    # From my tests, 3 counts are usually motions to find there is anything
    # Lower than 3 are other small parts that are not human
    if len(cnts) > 3:
        recordVideo = 1
    else:
        # Runs like 30 = 1 seconds Approx.
        # So we need 8 seconds interval to end
        # Now, 10 x 30 = 300
        # Lower the Detection counts, better lower the stop time
        loopEndCount += 1
        if loopEndCount > 300 and recordVideo == 1:
            print("Video has stopped now.")
            counter = 0
            recordVideo = 0
            loopEndCount = 0
            fileNameIncrement += 1
            videoWriter = cv2.VideoWriter('videos/motion' + str(fileNameIncrement) + '.avi',
                                          cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
                                          fps, size)

    for c in cnts:
        if cv2.contourArea(c) < 1500:
            continue
        # Calculate the bounding box
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    if recordVideo == 1:
        counter += 1
        print("Video recording......")
        videoWriter.write(frame)

    cv2.imshow("contours", frame)
    # cv2.imshow("dif", diff)
    # cv2.imwrite('didff.jpg', diff)
    if cv2.waitKey(int(1000 / 12)) & 0xff == ord('q'):
        break
cv2.destroyAllWindows()
camera.release()
