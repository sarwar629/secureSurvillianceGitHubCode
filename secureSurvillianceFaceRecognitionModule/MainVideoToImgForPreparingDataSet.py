
import cv2
import os

path="./trainingImages/tmp/";
isExist = os.path.exists(path)
if not isExist:
   # Create a new directory because it does not exist
   os.makedirs(path)
   print("The new directory is created!")
isExist = os.path.exists(path)

cap=cv2.VideoCapture(0)
count = 0
while True & isExist:
    ret,test_img=cap.read()
    if not ret :
        continue
    cv2.imwrite(path+"frame%d.jpg" % count, test_img)     # save frame as JPG file
    print(path+"frame%d.jpg saved" % count)
    count += 1
    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('Face Detection ',resized_img)
    if cv2.waitKey(10) == ord('q'):#wait until 'q' key is pressed
        break


cap.release()
cv2.destroyAllWindows
