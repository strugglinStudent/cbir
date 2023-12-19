import sys
import os
import cv2
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QScrollArea
from PyQt5.QtGui import QPixmap, QImage

class ImageLoaderUI(QWidget):
    def __init__(self):
        super().__init__()

        self.image_label = QLabel("Image will be displayed here")
        self.load_image_button = QPushButton("Load Image")
        self.load_image_button.clicked.connect(self.load_and_compare_image)

        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.load_image_button)

        # Create a scroll area for displaying the most similar images
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_widget = QWidget()
        self.most_similar_layout = QHBoxLayout(self.scroll_widget)
        self.scroll_area.setWidget(self.scroll_widget)

        layout.addWidget(self.scroll_area)

        self.setLayout(layout)
        self.setWindowTitle("Image Loader")

        self.database_folder = "C:\\Users\\Jihen\\tpwided\\CBIR-system\\BE"
        self.similarity_threshold = 1.5  # Adjust the threshold as needed

    def load_and_compare_image(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Open Image File", "", "Image Files (*.png *.jpg *.bmp *.jpeg);;All Files (*)", options=options)

        if file_name:
            query_image = cv2.imread(file_name)
            query_histogram = self.compute_histogram(query_image)

            # Find the most similar images from the database based on threshold
            similar_images = self.find_similar_images(query_histogram)

            # Display the loaded image
            pixmap = QPixmap(file_name)
            self.image_label.setPixmap(pixmap)
            self.image_label.setScaledContents(True)
            self.image_label.resize(pixmap.width(), pixmap.height())

            # Display the most similar images
            self.display_images(similar_images)

    def compute_histogram(self, image):
        # Compute the RGB histogram of the image
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8], [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist, hist).flatten()
        return hist

    def find_similar_images(self, query_histogram):
        # Find similar images based on SSD and threshold
        similar_images = []

        for file_name in os.listdir(self.database_folder):
            if file_name.lower().endswith(('.png', '.jpg', '.bmp', '.jpeg')):
                image_path = os.path.join(self.database_folder, file_name)
                database_image = cv2.imread(image_path)
                hist = self.compute_histogram(database_image)

                ssd = np.sum((query_histogram - hist) ** 2)

                if ssd < self.similarity_threshold:
                    similar_images.append(database_image)

        return similar_images

    def display_images(self, images):
        # Clear the previous similar images
        for i in reversed(range(self.most_similar_layout.count())):
            self.most_similar_layout.itemAt(i).widget().setParent(None)

        # Display the similar images
        for image in images:
            pixmap = self.convert_cv2_image_to_pixmap(image)
            similar_label = QLabel("Similar Image")
            similar_label.setPixmap(pixmap)
            self.most_similar_layout.addWidget(similar_label)

    def convert_cv2_image_to_pixmap(self, cv2_image):
        height, width, channel = cv2_image.shape
        bytes_per_line = 3 * width
        q_image = QImage(cv2_image.data, width, height, bytes_per_line, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image.rgbSwapped())
        return pixmap

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageLoaderUI()
    window.show()
    sys.exit(app.exec_())
