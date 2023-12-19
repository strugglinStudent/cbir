import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
import numpy as np
import argparse
from searcher import Searcher
from color.color import ColorDescriptor
from gabor.gabor import GaborDescriptor

class ImageSearchApp:
    def __init__(self, master):
        self.master = master
        master.title("Image Search App")

        self.image_path = None
        self.feature_class = None

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Select a query image:")
        self.label.pack()

        self.browse_button = tk.Button(self.master, text="Browse", command=self.load_image)
        self.browse_button.pack()

        self.feature_label = tk.Label(self.master, text="Select feature class:")
        self.feature_label.pack()

        self.feature_class_var = tk.StringVar(self.master)
        self.feature_class_var.set("color")  # Default feature class

        feature_classes = ["color", "gabor", "hog"]
        self.feature_menu = tk.OptionMenu(self.master, self.feature_class_var, *feature_classes)
        self.feature_menu.pack()

        self.search_button = tk.Button(self.master, text="Search", command=self.search)
        self.search_button.pack()

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.png;*.jpeg")])
        if file_path:
            self.image_path = file_path
            self.show_image()

    def show_image(self):
        if self.image_path:
            img = Image.open(self.image_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)

            if hasattr(self, 'img_label'):
                self.img_label.destroy()

            self.img_label = tk.Label(self.master, image=img)
            self.img_label.image = img
            self.img_label.pack()

    def search(self):
        if self.image_path and self.feature_class_var.get():
            args = {
                "query": self.image_path,
                "class": self.feature_class_var.get()
            }

        if args["class"] == "color" or args["class"] == "gabor" or args["class"] == "hog":

            if(args["class"] == "color"):
                bins = (8,12,3)
                cd = ColorDescriptor(bins)

                query = cv2.imread(args["query"])
                features = cd.describe(query)

                searcher = Searcher("color/index.csv")
                results = searcher.search(features)

            elif args["class"] == "gabor":
                params = {"theta":4, "frequency":(0,1,0.5,0.8), "sigma":(1,3),"n_slice":2}
                gd = GaborDescriptor(params)
                gaborKernels = gd.kernels()

                query = cv2.imread(args["query"])
                features = gd.gaborHistogram(query,gaborKernels)

                searcher = Searcher("gabor/index.csv")
                results = searcher._gsearch(features)

           
            myWindow = cv2.resize(query,(60,60))
            cv2.imshow("query",myWindow)

            for (score,resultId) in results:
                print(score)
                result = cv2.imread("../" +  "database" +"/"+resultId)
                print(resultId)
                myWindow = cv2.resize(result,(80,80))
                cv2.imshow("Result: "+str(score),myWindow)
                ch = cv2.waitKey(0)
                if ch == ord('q'):
                    pass


            # Note: You may need to modify the code in the script after "if args["class"] == ..." to
            # handle the UI interaction and display results in the UI.

def main():
    root = tk.Tk()
    app = ImageSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
