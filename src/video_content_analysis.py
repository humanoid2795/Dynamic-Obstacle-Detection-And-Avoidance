FRAME_RATE = 30


class VideoAnalysis:
    '''
    The current source of video for analysis is the video present in the
    google cloud storage servers.
    '''
    def __init__(
        self,
        gcs_uri='gs://minor-project-content-analysis/incoming-vehicle.mp4',
    ):
        self.gcs_uri = gcs_uri
        self.segment_labels = None
        self.object_annotations = None

    def find_labels(self):
        from google.cloud import videointelligence
        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.LABEL_DETECTION]
        operation = video_client.annotate_video(
            self.gcs_uri, features=features)

        result = operation.result(timeout=120)

        # Single video is being processed. '''annotation_results[0]'''
        self.segment_labels = result.annotation_results[0] \
            .segment_label_annotations

    def show_labels(self):
        if self.segment_labels is None:
            print('No labels found!')
            return
        for ii, segment_label in enumerate(self.segment_labels):
            print('Video label description: {}'.format(
                segment_label.entity.description))
            for category_entity in segment_label.category_entities:
                print('\tLabel category description: {}'.format(
                    category_entity.description))

            for i, segment in enumerate(segment_label.segments):
                start_time = (segment.segment.start_time_offset.seconds +
                    segment.segment.start_time_offset.nanos / 1e9)
                end_time = (segment.segment.end_time_offset.seconds +
                    segment.segment.end_time_offset.nanos / 1e9)
                positions = '{}s to {}s'.format(start_time, end_time)
                confidence = segment.confidence
                print('\tSegment {}: {}'.format(i, positions))
                print('\tConfidence: {}'.format(confidence))
            print('\n')

    def content_analysis(self):
        from google.cloud import videointelligence_v1p2beta1 as \
                videointelligence

        video_client = videointelligence.VideoIntelligenceServiceClient()
        features = [videointelligence.enums.Feature.OBJECT_TRACKING]

        operation = video_client.annotate_video(
            input_uri=self.gcs_uri,
            features=features,
            location_id='asia-east1',
        )

        print('\nProcessing video for object annotations.')

        result = operation.result(timeout=300)
        print('\nFinished processing.\n')

        # The first result is retrieved because a single video was processed.
        self.object_annotations = result.annotation_results[0].object_annotations
        return self.object_annotations

    def show_content_analysis(self):
        if self.object_annotations is None:
            print('No Content Analysis Available!')
            return
        for object_annotation in self.object_annotations:
            print('Entity description: {}'.format(
                object_annotation.entity.description))
            if object_annotation.entity.entity_id:
                print('Entity id: {}'.format(object_annotation.entity.entity_id))

            print('Segment: {}s to {}s'.format(
                object_annotation.segment.start_time_offset.seconds +
                object_annotation.segment.start_time_offset.nanos / 1e9,
                object_annotation.segment.end_time_offset.seconds +
                object_annotation.segment.end_time_offset.nanos / 1e9))

            print('Confidence: {}'.format(object_annotation.confidence))

            for frame in object_annotation.frames:

                box = frame.normalized_bounding_box
                print('Time offset of the frame: {}s'.format(
                    frame.time_offset.seconds + frame.time_offset.nanos / 1e9))
                if object_annotation.entity.description == 'car':
                    print('Object Entity Description', object_annotation.entity.description)
                    print('Bounding box position:')
                    print('\tleft  : {}'.format(box.left))
                    print('\ttop   : {}'.format(box.top))
                    print('\tright : {}'.format(box.right))
                    print('\tbottom: {}'.format(box.bottom))
                    print('\tframe: {}'.format(
                        int(
                            (
                                frame.time_offset.seconds +
                                frame.time_offset.nanos /
                            1e9) * FRAME_RATE)
                        )
                    )
                    print('\n')
