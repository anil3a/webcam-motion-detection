# imports
import cv2
import datetime


# Record based on face detection


def motion_detection():
    video_capture = cv2.VideoCapture(0)  # value (0) selects the devices default camera

    # Start of config for Video Capture

    # Face detection library
    cascPath = "HaarCascade/haarcascade_frontalface_default.xml"

    fps = 30  # camera.get(cv2.CAP_PROP_FPS)

    video_folder_name = 'videos'
    video_file_name = 'motion'
    file_name_increments = 1
    valid_face_count = 0
    # Runs like 30 = 1 seconds Approx.
    # So we need 10 seconds interval to end
    # Now, 10 x 30 = 300
    # Lower the Detection counts, better lower the stop time
    valid_loop_end_count = 300

    counter = 0
    console_message_shown = 0

    # When to show message in console when run in console
    show_console_message_split_count = 80

    # End of Config for Video Capture

    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    record_video = loop_end_count = 0
    video_writer = cv_video_write(video_folder_name, video_file_name, file_name_increments, fps, size)

    while True:
        frame = video_capture.read()[1]  # gives 2 outputs rectangle_value,frame - [1] selects frame

        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # make each frame greyscale which is needed for threshold

        # Create the haar cascade
        face_cascade = cv2.CascadeClassifier(cascPath)
        # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces in the image
        faces = face_cascade.detectMultiScale(
            greyscale_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30),
            flags=cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # print("Found {0} faces!".format(len(faces)))

        if len(faces) > valid_face_count:
            record_video = 1
        else:
            loop_end_count += 1
            if loop_end_count > valid_loop_end_count and record_video == 1:
                print(str(datetime.datetime.now()) + " - Recording has stopped. [ Loop faces. " +
                      str(valid_face_count) + " ] [ " + str(len(faces)) + " ]")
                print("")
                record_video = 0
                loop_end_count = 0
                console_message_show = 0
                file_name_increments += 1
                video_writer = cv_video_write(video_folder_name, video_file_name, file_name_increments, fps, size)

        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # frame.shape[0] = height, frame.shape[1] = width,

        # using datetime to get date/time stamp, for font positions using frame.shape()
        # which returns a tuple of (rows,columns,channels)
        # going 10 across in rows/width so need columns with frame.shape()[0]
        # we are selecting columns so how ever many pixel height
        # the image is - 10 so opposite end at bottom instead of being at the top like the other text

        counter += 1

        if record_video == 1:
            # print("Video recording......")
            video_writer.write(frame)

            if console_message_shown == 0:
                print(str(datetime.datetime.now()) + " - Recording Started [ FACE Count: " +
                      str(len(faces)) + " ] ..... ")
                console_message_shown = 1

            if counter > show_console_message_split_count:
                counter = 0
                print(str(datetime.datetime.now()) + " - Recording [ FACE Count: " + str(len(faces)) + " ] ..... ")
                console_message_shown = 1

        cv2.imshow('Video', frame)

        key = cv2.waitKey(1) & 0xFF  # (1) = time delay in seconds before execution,
        # and 0xFF takes the last 8 bit to check value or summing
        if key == ord('q'):
            cv2.destroyAllWindows()
            video_capture.release()
            break


def cv_video_write(video_folder_name, video_file_name, file_name_increments, fps, size):
    return cv2.VideoWriter(
        video_folder_name + '/' + video_file_name + str(file_name_increments) + '.mp4',
        cv2.VideoWriter_fourcc('m', 'p', '4', 'v'),
        fps, size, True)


if __name__ == '__main__':
    motion_detection()
