import io
import google.cloud.vision


class ObstacleDetection:

    @classmethod
    def detect_labels(cls, path):
        # Detects labels in the image file.

        client = google.cloud.vision.ImageAnnotatorClient()
        with io.open(path, 'rb') as image_file:
            content = image_file.read()

        image = google.cloud.vision.types.Image(content=content)
        response = client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)

    @classmethod
    def detect_labels_url(cls, url):
        # Detects labels in the file located in Google Cloud Storage or on
        # the Web using the url.

        client = google.cloud.vision.ImageAnnotatorClient()
        image = google.cloud.vision.types.Image()
        image.source.image_uri = url

        response = client.label_detection(image=image)
        labels = response.label_annotations

        print('Labels:')
        for label in labels:
            print(label.description)
