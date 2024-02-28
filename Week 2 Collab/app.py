# collab app
import os, cv2 as cv
import numpy as np

images = []

def readImage(PATH):
    # CHECK IF file exist
    varr = os.path.isfile(PATH)
    if varr:
        img = cv.imread(PATH)
        return img
    else:
        return []

def collab(images):
    print("==")
    for i in range(len(images)):
        images[i] = cv.resize(images[i], (200, 200))
        
    print("==")

    horizontal_stack = np.hstack(images)
    arr = []
    for Image in images:
        arr.append(horizontal_stack) 
    
    print("==")

    vertical_stack = np.vstack(arr)

    cv.imshow("erer", vertical_stack)
    cv.waitKey(0)

    return None


if __name__ == "__main__":

    images.append(cv.imread("1.jpeg"))
    images.append(cv.imread("2.jpeg"))
    images.append(cv.imread("3.jpeg"))
    images.append(cv.imread("4.jpeg"))
    images.append(cv.imread("5.jpeg"))
    images.append(cv.imread("6.jpeg"))

    while True:
        # clear console
        print("\033[H\033[J")
        print("===================================")
        print("=           Collab App            =")
        print("===================================")
        print(" 1. Select Image")
        print(" 2. Make Collab")
        print(" 3. Exit")
        print("\n")
        ch = input("Your Choice: ")

        if ch == "1":
            print("\033[H\033[J")
            print("===================================")
            print("=           Collab App            =")
            print("===================================")
            print("\n")
            name = input("Enter Image Name: ")
            img = readImage(name)
            if len(img) == 0:
                print("Not Found!")
            else:
                images.append(img)
                print("Image Added!")
            print("Press Enter to Continue")
            input()
        elif ch == "2":
            collab(images)
        elif ch == "3":
            print("Bye")
            break
        else:
            print("Invalid Choice!")
            print("Press Enter to Continue")
            input()


