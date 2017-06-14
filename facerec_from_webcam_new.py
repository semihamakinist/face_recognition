#import face_recognition
import face_api
import cv2
import os, sys
import numpy as np
import json, codecs

# This is a super simple demo of running face recognition
# on live video from your webcam.
# PLEASE NOTE: This example requires OpenCV (the `cv2` library)
# to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library.
# It's only required if you want to run this
# specific demo. If you have trouble installing it,
# try any of the other demos that don't require it instead.

def match_encoding(all_faces, match):
    name = "Unknown"
    try:
       for index in range(len(match)):
#           if match[index]:
#               name = all_faces[index]["name"]
            if match[index]["match"]:
                print "{} : {}".format(all_faces[index]["name"],
                                match[index]["score"])
                name = all_faces[index]["name"]
    except:
        pass 
    return name
try:
    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)
    
    main_path = os.path.dirname(__file__)
    result_path = os.path.join(main_path, "result")
    
    #open model
    fp = codecs.open(os.path.join(result_path, "face_encodings_gender.json"),
    #fp = codecs.open(os.path.join(result_path, "face_encodings_multi_all.json"),
    #fp = codecs.open(os.path.join(result_path, "face_encodings_sigle_new.json"), 
                     "r", encoding='utf-8')
    obj_text = fp.read()
    average_face_encoding = json.loads(obj_text)
    fp.close()
    
    for index in range(len(average_face_encoding)):
        temp = average_face_encoding[index]["encodings"] 
        average_face_encoding[index]["encodings"] = np.array(temp)
    
    # Initialize some variables
    face_locations = []
    face_encodings = []
    face_names = []
    process_this_frame = True
    
    while True:
        # Grab a single frame of video
        ret, frame = video_capture.read()
    
        # Resize frame of video to 1/2 size for faster face recognition processing
        small_frame = cv2.resize(frame, (0, 0), fx=0.75, fy=0.75)
    
        # Only process every other frame of video to save time
        if process_this_frame:
            # Find all the faces and face encodings in the current frame of video
            face_locations = face_api.face_locations(small_frame)
            face_encodings = face_api.face_encodings(small_frame, face_locations)
    
            face_names = []
            for face_encoding in face_encodings:
                # See if the face is a match for the known face(s)
                match = [face_api.compare_faces([all_encoding["encodings"]],
                                                face_encoding) for all_encoding in average_face_encoding]
        
                name = match_encoding(average_face_encoding, match)
    
                face_names.append(name)
    
        process_this_frame = not process_this_frame
    
    
        # Display the results
        for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= (4./3)
            right *= (4./3)
            bottom *= (4./3)
            left *= (4./3)
            
            left =int(left); top =int(top);bottom =int(bottom);right =int(right)
            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
    
            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), 
                          (right, bottom), (0, 0, 255), 
                          cv2.cv.CV_FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), 
                        font, 1.0, (255, 255, 255), 1)
    
        # Display the resulting image
        cv2.imshow('Video', frame)
    
        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()
except:
    # Release handle to the webcam
    video_capture.release()
    cv2.destroyAllWindows()    
    
    e = sys.exc_info()[0]
    print( "Error: {}".format(e))
