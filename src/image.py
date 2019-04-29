import cv2


class Image:

    def __init__(self, image_path):
        self.image_path = image_path
        self.image = cv2.imread(image_path, cv2.IMREAD_COLOR)

    
    def update_color(self, x, y, color):
        self.image[x][y][0] = color
        self.image[x][y][1] = color
        self.image[x][y][2] = color
    
    def commit(self):
        cv2.imwrite(self.image_path, self.image)
