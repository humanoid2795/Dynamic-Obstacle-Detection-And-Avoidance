import argparse
from obstacle_detection import ObstacleDetection
from obstacle_boundary import ObstacleBoundary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', type=str, default=None, help='Path of Image')
    parser.add_argument('--url', type=str, default=None, help='Url of Image')
    parser.add_argument(
        '--boundary',
        action='store_true',
        help='Boundary of Image',
    )
    argument = parser.parse_args()

    if argument.path is None:
        ObstacleDetection.detect_labels_url(argument.url)
    else:
        ObstacleDetection.detect_labels(argument.path)

    if argument.boundary is True and argument.path is not None:
        obstacle_boundary = ObstacleBoundary(argument.path)
        obstacle_boundary.show_boundary()


if __name__ == "__main__":
    main()
