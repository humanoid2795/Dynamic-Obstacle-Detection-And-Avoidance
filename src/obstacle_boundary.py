import cv2

BLACK = 0
OBJECT_COLOR = 50
WHITE = 255


class ObstacleBoundary:
    # The obstacle is assumed to be have the RBG color
    # gradient less than OBJECT_COLOR.

    def __init__(self, image):
        self.image = cv2.imread(image, cv2.IMREAD_COLOR)
        self.boundary = cv2.imread(image, cv2.IMREAD_COLOR)
        self._image_filter()
        self._find_boundary()

    def _get_resolution(self):
        # The method returns the height and width of the image frame.
        return self.image.shape[:2]

    def _image_filter(self):
        # The method finds the object in the image.

        height, width = self._get_resolution()
        for ii in range(height):
            for jj in range(width):
                color = -1
                if (
                    self.image[ii][jj][0] < OBJECT_COLOR and
                    self.image[ii][jj][1] < OBJECT_COLOR and
                    self.image[ii][jj][2] < OBJECT_COLOR
                ):
                    color = BLACK
                else:
                    color = WHITE
                self.image[ii][jj][0] = color
                self.image[ii][jj][1] = color
                self.image[ii][jj][2] = color
                self.boundary[ii][jj][0] = color
                self.boundary[ii][jj][1] = color
                self.boundary[ii][jj][2] = color

    def _find_boundary(self):
        # The method finds the boundary of the obstacle.

        height, width = self._get_resolution()
        for ii in range(height):
            for jj in range(width):
                if (
                    self.image[ii][jj][0] == BLACK and
                    self.image[ii][jj][1] == BLACK and
                    self.image[ii][jj][2] == BLACK and
                    ii > 0 and
                    ii < height - 1 and
                    jj > 0 and
                    jj < width - 1
                ):
                    adjacent = [[0, -1], [0, +1], [-1, 0], [+1, 0]]
                    adjacent_pixel = 0
                    for kk in range(len(adjacent)):
                        x = ii + adjacent[kk][0]
                        y = jj + adjacent[kk][1]
                        if (
                            self.image[x][y][0] == BLACK and
                            self.image[x][y][1] == BLACK and
                            self.image[x][y][2] == BLACK
                        ):
                            adjacent_pixel += 1
                    if adjacent_pixel == len(adjacent):
                        self.boundary[ii][jj][0] = WHITE
                        self.boundary[ii][jj][1] = WHITE
                        self.boundary[ii][jj][2] = WHITE

    def show_boundary(self, image_name=None):
        # The method shows the boundary of the obstacle.

        cv2.imshow('Obstacle Boundary', self.boundary)
        keystroke = cv2.waitKey(0)
        if keystroke == 115:
            if image_name is None:
                raise NameError('Output file has no name.')
            else:
                cv2.imwrite(image_name, self.boundary)
        cv2.destroyAllWindows()
