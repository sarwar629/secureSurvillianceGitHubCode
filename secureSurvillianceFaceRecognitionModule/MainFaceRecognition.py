from datetime import datetime
import os
from time import time
import cv2
import numpy as np
import requests

import appConfig
import faceRecognition as fr


MIN_TIME_BETWEEN_TWO_TXNS=int(appConfig.getAppConfig("MIN_TIME_BETWEEN_TWO_TXNS")) 
MINING_NODE_ADDRESS=appConfig.getAppConfig("MINING_NODE_ADDRESS") 
NODE_LOCATION=appConfig.getAppConfig("NODE_LOCATION") 

#print(MIN_TIME_BETWEEN_TWO_TXNS)

#This module captures images via webcam and performs face recqognition
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
face_recognizer.read('trainingData.yml')#Load saved training data

# print(cv2.__version__)

name = {0 : "Priyanka",1 : "Kangana", 2 : "Sarwar"}
detected_person={}
                    # "personid":"",
                    # "name":"",
                    # "entry_time":"",
                    # "exit_time":"",
                    
detected_persons={}
                # {0:detected_person,
                # 1:detected_person,
                # 2:detected_person,
                # }

camera_id=0
cap=cv2.VideoCapture(camera_id)

while True:
    ret,test_img=cap.read()# captures frame and returns boolean value and captured image
    faces_detected,gray_img=fr.faceDetection(test_img)
    
    #cv2.imwrite("trainingImages/2/sarwar_"+datetime.now().strftime("%H%M%S")+".jpg",test_img)

    for (x,y,w,h) in faces_detected:
      cv2.rectangle(test_img,(x,y),(x+w,y+h),(255,0,0),thickness=7)

    resized_img = cv2.resize(test_img, (1000, 700))
    #cv2.imshow('face detection Tutorial ',resized_img)
    cv2.waitKey(3)


    for face in faces_detected:
        (x,y,w,h)=face
        roi_gray=gray_img[y:y+w, x:x+h]
        label,confidence=face_recognizer.predict(roi_gray)#predicting the label of given image
        # print("----------------------------------------")
        # print("confidence:",confidence)
        # print("label:",label)
        fr.draw_rect(test_img,face)
        predicted_name=name[label]
        
        if confidence < 50:#If confidence less than 37 then don't print predicted face text on screen
          fr.put_text(test_img,predicted_name,x,y)
          print("----------------------------------------")
          print("confidence:",confidence)
          print("label:",label)




          
          detected_person=detected_persons.get(label)
          
          if(detected_person==None):
            detected_person={}
          print("detected person is empty**********************************************",detected_person)
          if(len(detected_person)==0):
            #print("dtected person is empty************************************************************")
            detected_person["personid"]=label
            detected_person["name"]=name[label]
            detected_person["entry_time"]=datetime.now()
            detected_person["exit_time"]=datetime.now()
            detected_person["camera_id"]=camera_id
          print("Time between two txns: ",(datetime.now()-detected_person["exit_time"]).total_seconds())
          if((datetime.now()-detected_person["exit_time"]).total_seconds()<MIN_TIME_BETWEEN_TWO_TXNS):
            detected_person["exit_time"]=datetime.now()
          else:
            ####################################
            # make an entry of detected_person to blockchain
            detectedPersonEntryDetails = "Time: "+detected_person["entry_time"].strftime("%Y-%m-%d %H:%M:%S")+";        "\
                            +"Found Location: "+NODE_LOCATION
                            #+str(detected_person["camera_id"])
                            #+detected_person["exit_time"].strftime("%Y-%m-%d %H:%M:%S")+" "
            detectedPersonDetails = str(detected_person["personid"])+" "+detected_person["name"]

            post_object = {
                'detectedPersonDetails': detectedPersonDetails,
                'detectedPersonEntryDetails': detectedPersonEntryDetails,
            }

            # Submit a transaction
            new_tx_address = "{}/new_transaction".format(MINING_NODE_ADDRESS)

            #if((detected_person["exit_time"]-detected_person["entry_time"]).total_seconds()>=1): #stop false positive submission.
            print(post_object)
            requests.post(new_tx_address,
                      json=post_object,
                      headers={'Content-type': 'application/json'})
            #####################################
            print("Successfull entry in block chain for Person id: ",label," & name: ",name[label])
            detected_person={}
            del detected_persons[label]

          
          detected_persons[label]=detected_person
          
          print(detected_person)
          print("Person Name: ",predicted_name)
          print("Entry Time: ",datetime.now())
          print("Exit Time: ",datetime.now())
          print("Camera location/id: ",camera_id)


    resized_img = cv2.resize(test_img, (1000, 700))
    cv2.imshow('face recognition tutorial ',resized_img)
    #if cv2.waitKey(1) == ord('q'):     #wait until 'q' key is pressed
    if cv2.waitKey(1) == 27:  #wait until 'Esc' key is pressed
      print("====================================================")
      print("Person Id: ",detected_person["personid"])
      print("Person Name: ",detected_person["name"])
      print("Entry Time: ",detected_person["entry_time"])
      print("Exit Time: ",detected_person["exit_time"])
      print("Camera location/id: ",detected_person["camera_id"])
      print("difference of time(sec): ",(detected_person["exit_time"]-detected_person["entry_time"]).total_seconds())
      print("====================================================")
      break


cap.release()
cv2.destroyAllWindows

