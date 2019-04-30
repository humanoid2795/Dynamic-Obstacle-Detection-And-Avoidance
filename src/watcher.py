import os
import subprocess
import time

from glob import glob
from threading import Thread


from google.cloud import storage


BUCKET = 'minor-project-content-analysis'


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print('File {} uploaded to {}.'.format(
        source_file_name,
        destination_blob_name))


def list_blobs(bucket_name=BUCKET):
    """Lists all the blobs in the bucket."""
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs()

    blob_name = []
    for blob in blobs:
        blob_name.append(blob.name)
    
    return blob_name


def list_blobs_with_prefix(bucket_name, prefix='recorded-images/', delimiter=None):
    
    storage_client = storage.Client()
    bucket = storage_client.get_bucket(bucket_name)

    blobs = bucket.list_blobs(prefix=prefix, delimiter=delimiter)

    print('Blobs:')
    blob_names = []
    for blob in blobs:
        blob_names.append(blob.name)

    if delimiter:
        print('Prefixes:')
        for prefix in blobs.prefixes:
            blob_names.append(blob.name)
    return blob_names


class Watcher(Thread):

    def __init__(
        self,
        paths_to_watch=os.getcwd(),
        interval_between_checks=5,
    ):
        self.paths_to_watch = paths_to_watch
        self.interval_between_checks = interval_between_checks
        self.watching = False
        self.previous_modified_times = {}
        for element in glob(self.paths_to_watch):
            try:
                self.previous_modified_times[element] = \
                    os.path.getmtime(element)
            except IOError:
                pass

        Thread.__init__(self)

    def run(self):
        self.watching = True
        while self.watching:
            self.run_watcher()
            time.sleep(self.interval_between_checks)

    def run_watcher(self):
        current_modified_times = {}
        for element in glob('*'):
            try:
                current_modified_times[element] = os.path.getmtime(element)
            except IOError:
                pass

        should_execute_action = False
        # Check if new path is added or updated.
        for current_path, current_time in current_modified_times.items():
            if current_path in self.previous_modified_times:
                if current_time > self.previous_modified_times[current_path]:
                    should_execute_action = True
                    break
                else:
                    del self.previous_modified_times[current_path]
            else:
                should_execute_action = True
                break

        blobs = list_blobs_with_prefix(BUCKET)

        if should_execute_action:
            blobs = list_blobs_with_prefix(BUCKET)
            for ii in range(0, len(blobs)):
                blobs[ii] = os.path.basename(blobs[ii])
            for current_path, current_time in current_modified_times.items():
                try:
                    if current_path not in blobs:
                        upload_blob(
                            BUCKET,
                            current_path,
                            'recorded-images/' + current_path,
                        )
                except TypeError:
                    pass
        self.previous_modified_times = current_modified_times

    def stop_watcher(self):
        self.watching = False


working_directory = os.getcwd()
os.chdir('.\\..\\test\\Images\\')


path_watcher = Watcher(
    paths_to_watch=os.getcwd(),
    interval_between_checks=5,
)


path_watcher.start()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    path_watcher.stop_watcher()
finally:
    os.chdir(working_directory)
