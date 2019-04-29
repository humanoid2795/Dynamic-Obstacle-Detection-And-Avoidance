import json
import cv2
from math import floor, atan


# x = 0
# while x < len(object_tracing) - 1:

# 	frame_number = object_tracing[x]['frame']
# 	image_name = 'frame' + str(frame_number) + '.jpg'

# 	image = cv2.imread(image_name, cv2.IMREAD_COLOR)
# 	height, width = image.shape[:2]
	
# 	"""
# 	center = ((width/2), (height/2))
# 	angle = 270
# 	scale = 1.0
# 	M = cv2.getRotationMatrix2D(center, angle, scale)
# 	rotated = cv2.warpAffine(image, M, (height, width))
# 	image = rotated
# 	width, height = height, width
# 	"""
# 	left = floor(object_tracing[x]['left'] * width)
# 	top = floor(object_tracing[x]['top'] * height)
# 	right = floor(object_tracing[x]['right'] * width)
# 	bottom = floor(object_tracing[x]['bottom'] * height)


# 	for ii in range(0, width):
# 		for jj in range(0, height):
# 			pass
# 			#image[jj][ii][0] = 255
# 			#image[jj][ii][1] = 255
# 			#image[jj][ii][2] = 255

# 	print(width, height)
# 	print(left, top, right, bottom, frame_number)
# 	for ii in range(left, right):
# 		for jj in range(top, bottom):
# 			image[jj][ii][0] = 0
# 			image[jj][ii][1] = 0
# 			image[jj][ii][2] = 0
# 	font = cv2.FONT_HERSHEY_SIMPLEX
# 	bottomLeftCornerOfText = (10,500)
# 	fontScale = 1
# 	fontColor = (255,255,255)
# 	lineType = 2


# 	try:

# 		if (left * left) >= ((width - right) * (width - right)):
# 			print('Movement towards the LEFT from the mean center')
# 			center_x, center_y = int(width / 2), int(height / 2)
# 			left_x, left_y = 0, int((top + bottom) / 2)
# 			slope_one = (center_y - left_y) / (center_x - left_x)

# 			left_x, left_y = left, int((top + bottom) / 2)
# 			slope_two = (center_y - left_y) / (center_x - left_x)

# 			angle = atan(abs((slope_two - slope_one) / (1 + slope_one * slope_two)))
# 			angle = angle * 180 / 3.14
# 			print(90 - angle)
# 			cv2.putText(image_name,'LEFT: %s' % (str(90 - angle)), 
# 			    bottomLeftCornerOfText, 
# 			    font, 
# 			    fontScale,
# 			    fontColor,
# 			    lineType)
# 		else:
# 			print('Movement towards the RIGHT from the mean center')
# 			center_x, center_y = int(width / 2), int(height / 2)
# 			right_x, right_y = width, int((top + bottom) / 2)
# 			slope_one = (center_y - right_y) / (center_x - right_x)
# 			# print(center_x, center_y, right_x, right_y)
# 			right_x, right_y = right, int((top + bottom) / 2)
# 			slope_two = (center_y - right_y) / (center_x - right_x)
# 			# print(center_x, center_y, right_x, right_y)
# 			angle = atan(abs((slope_two - slope_one) / (1 + slope_one * slope_two)))
# 			# print(angle)
# 			angle = (angle * 180) / 3.14
# 			print(90 - angle)
# 			print('Movement towards the RIGHT from the mean center at an angle: %s' % (str(90 - angle)))
# 			cv2.putText(image,'RIGHT: %s' % (str(90 - angle)), 
# 			    bottomLeftCornerOfText, 
# 			    font, 
# 			    fontScale,
# 			    fontColor,
# 			    lineType)
# 	except:
# 		pass



# 	# cv2.imshow('Obstacle Image', image)
# 	# keystroke = cv2.waitKey(0)
# 	# cv2.destroyAllWindows()
# 	cv2.imwrite(image_name, image)
# 	x += 1
# 	"""
# 	left = 0.3810257613658905
# 	top = 0.14640088379383087
# 	right = 0.4893268346786499
# 	bottom = 0.2181389182806015
# 	x = int(left * width)
# 	y = int(top * height)

# 	x2 = x + int(right * width)
# 	y2 = y + int(bottom * height)

# 	print(x, y, x2, y2)
# 	img = cv2.rectangle(image, (x,y), (x2,y2), (0,0,255), 2)
# 	cv2.imshow('Image', img)
# 	cv2.waitKey(0)
# 	cv2.destroyAllWindows()
# 	"""

from video_content_analysis import VideoAnalysis
import time
import os
from google.cloud import storage
from image import Image
from enum import Enum


BUCKET = 'minor-project-content-analysis'
IMAGES = '.\\..\\test\\Images\\'
GCS_URI = 'gs://minor-project-content-analysis/incoming-vehicle.mp4'


def download_blob(bucket_name, source_blob_name, destination_file_name):
    """Downloads a blob from the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(source_blob_name)

    blob.download_to_filename(destination_file_name)

    print('Blob {} downloaded to {}.'.format(
        source_blob_name,
        destination_file_name))


def get_video(video_url):
    # Assumed no duplication in name.
    download_blob(
        BUCKET,
        os.path.basename(video_url),
        '.\..\\test\\' + os.path.basename(video_url)
    )
    # Slicing into images.
    
    vidcap = cv2.VideoCapture('.\..\\test\\' + os.path.basename(video_url))
    success,image = vidcap.read()
    count = 0
    while success:
        cv2.imwrite(".\\..\\test\\Images\\frame%d.jpg" % count, image)     # save frame as JPEG file      
        success,image = vidcap.read()
        print('Read a new frame: ', success)
        count += 1
        print(count)


def mark_obstacle():
    video_analysis = VideoAnalysis()
    object_annotations = video_analysis.content_analysis()
    color = 0
    for object_annotation in object_annotations:

        for frame in object_annotation.frames:
            if frame is None:
                break
            box = frame.normalized_bounding_box
            frame_number = int((frame.time_offset.seconds + frame.time_offset.nanos /1e9) * 30)
            image_name = '.\\..\\test\\Images\\frame' + str(frame_number) + '.jpg'
            if not os.path.isfile(image_name):
                break
            temp_image = cv2.imread(image_name, cv2.IMREAD_COLOR)
            height, width = temp_image.shape[:2]
            print(height, width)
            left = floor(box.left * width)
            right = floor(box.right * width)
            top = floor(box.top * height)
            bottom = floor(box.bottom * height)

            image = Image(image_name)
            for ii in range(left, right):
                for jj in range(top, bottom):
                    image.update_color(jj, ii, color)
            image.commit()

            print(box.left, box.right, box.top, box.bottom, int((frame.time_offset.seconds + frame.time_offset.nanos /1e9) * 30))
        color += 100
        color = color % 255
        

# get_video(GCS_URI) 
# mark_obstacle('car')
mark_obstacle()