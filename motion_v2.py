# imports
import cv2
import datetime
# import imutils


def motion_detection():
    video_capture = cv2.VideoCapture(0)  # value (0) selects the devices default camera

    # Start of config for Video Capture

    # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over
    # 100 will become 255(white))
    threshold = 60

    fps = 30  # camera.get(cv2.CAP_PROP_FPS)

    video_folder_name = 'videos'
    video_file_name = 'motion'
    file_name_increments = 1
    valid_motion_count = 1
    # Runs like 30 = 1 seconds Approx.
    # So we need 10 seconds interval to end
    # Now, 10 x 30 = 300
    # Lower the Detection counts, better lower the stop time
    valid_loop_end_count = 300

    counter = 0
    console_message_shown = 0

    # When to show message in console when run in console
    show_console_message_split_count = 80

    first_frame = None  # initiate the first fame

    # End of Config for Video Capture

    size = (int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
            int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    record_video = loop_end_count = 0
    video_writer = cv2.VideoWriter(video_folder_name + '/' + video_file_name + '1.avi',
                                   cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
                                   fps, size)

    while True:
        frame = video_capture.read()[1]  # gives 2 outputs rectangle_value,frame - [1] selects frame

        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # make each frame greyscale which is needed for threshold

        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)
        # uses a kernel of size(21,21) // has to be odd number to to ensure there is a valid integer in the centre
        # and we need to specify the standard deviation in x and y direction which is the (0) if only x(sigma x)
        # is specified
        # then y(sigma y) is taken as same as x. sigma = standard deviation(mathematics term)

        blur_frame = cv2.blur(gaussian_frame, (5, 5))
        # uses a kernel of size(5,5)(width,height) which goes over 5x5 pixel area left to right
        # does a calculation and the pixel located in the centre of the kernel will become
        # a new value(the sum of the kernel after the calculations) and then it moves to the right one and
        # has a new centre pixel
        # and does it all over again..until the image is done, obv this can cause the edges to not be changed,
        # but is very minute

        greyscale_image = blur_frame
        # greyscale image with blur etc which is the final image ready to be used for threshold and motion detection

        if first_frame is None:
            first_frame = greyscale_image
            # first frame is set for background subtraction(BS) using abs-diff and then using threshold to get the
            # foreground mask
            # foreground mask (black background anything that wasn't in image in first frame but is in new frame over
            # the threshold will
            # be a white pixel(white) foreground image is black with new object being white...there is
            # your motion detection
        else:
            pass

        # frame = imutils.resize(frame, width=500)
        frame_delta = cv2.absdiff(first_frame, greyscale_image)
        # calculates the absolute difference between each element/pixel between the two images,
        # first_frame - greyscale (on each element)

        thresh = cv2.threshold(frame_delta, threshold, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs rectangle_value,threshold image. using [1] on the end i am selecting the
        # threshold image that is produced

        dilate_image = cv2.dilate(thresh, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foreground)
        # is to enlarge/expand the white
        # pixels in the foreground which are white(255), element=Mat() = default 3x3 kernel matrix and
        # iterations=2 means it
        # will do it twice

        cnt, _ = cv2.findContours(dilate_image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2:]
        # contours gives 3 different outputs image, contours and hierarchy, so using [1] on
        # end means contours = [1](cnt)
        # cv2.CHAIN_APPROX_SIMPLE saves memory by removing all redundant points and compressing the contour,
        # if you have a rectangle
        # with 4 straight lines you don't need to plot each point along the line, you only need to plot the
        # corners of the rectangle
        # and then join the lines, eg instead of having say 750 points, you have 4 points....
        # look at the memory you save!

        if len(cnt) > valid_motion_count:
            record_video = 1
        else:
            loop_end_count += 1
            print(" video recording but ending soon  ......" + str(len(cnt)))
            if loop_end_count > valid_loop_end_count and record_video == 1:
                print(str(datetime.datetime.now()) + " - Recording has stopped. [ Loop motion. " +
                      str(valid_motion_count) + " ] [ " + str(len(cnt)) + " ]")
                print("")
                record_video = 0
                loop_end_count = 0
                console_message_show = 0
                file_name_increments += 1
                video_writer = cv2.VideoWriter(
                    video_folder_name + '/' + video_file_name + str(file_name_increments) + '.avi',
                    cv2.VideoWriter_fourcc('D', 'I', 'V', 'X'),
                    fps, size)

        cv2.putText(frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
                    (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        # frame.shape[0] = height, frame.shape[1] = width,

        # using datetime to get date/time stamp, for font positions using frame.shape()
        # which returns a tuple of (rows,columns,channels)
        # going 10 across in rows/width so need columns with frame.shape()[0]
        # we are selecting columns so how ever many pixel height
        # the image is - 10 so opposite end at bottom instead of being at the top like the other text

        for c in cnt:
            if cv2.contourArea(c) > 1500:  # if contour area is less then 800 non-zero(not-black) pixels(white)
                (x, y, w, h) = cv2.boundingRect(c)
                # x,y are the top left of the contour and w,h are the width and height

                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                # (0, 255, 0) = color R,G,B = lime / 2 = thickness(i think?)(YES IM RIGHT!)
                # image used for rectangle is frame so that its on the security feed image and
                # not the binary/threshold/foreground image
                # as its already used the threshold/(binary image) to find the contours
                # this image/frame is what image it will be drawn on
            else:
                pass

        counter += 1

        if record_video == 1:
            # print("Video recording......")
            video_writer.write(frame)

            if console_message_shown == 0:
                print(str(datetime.datetime.now()) + " - Recording Started [ " + str(len(cnt)) + " ] ..... ")
                console_message_shown = 1

            if counter > show_console_message_split_count:
                counter = 0
                print(str(datetime.datetime.now()) + " - Recording [ " + str(len(cnt)) + " ] ..... ")
                console_message_shown = 1

        cv2.imshow('Video', frame)
        cv2.imshow('Threshold(foreground mask)', dilate_image)
        cv2.imshow('Frame_delta', frame_delta)

        key = cv2.waitKey(1) & 0xFF  # (1) = time delay in seconds before execution,
        # and 0xFF takes the last 8 bit to check value or summing
        if key == ord('q'):
            cv2.destroyAllWindows()
            video_capture.release()
            break


if __name__ == '__main__':
    motion_detection()
