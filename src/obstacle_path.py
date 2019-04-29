import json
import cv2
from math import floor, atan
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

        color += 100
        color = color % 255


def find_angle(self, width, height, x1, y1, x2, y2):
    origin_x, origin_y = int(width / 2), height

    # Left Boundary
    x, y = x1, int((y1 + y2) / 2)
    

