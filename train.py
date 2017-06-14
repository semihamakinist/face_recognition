#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  1 13:46:22 2017

@author: semiha
"""

import face_recognition
import os, argparse
import json, codecs

# This is a super simple demo of running face recognition
# on live video from your webcam.
# PLEASE NOTE: This example requires OpenCV (the `cv2` library)
# to be installed only to read from your webcam.
# OpenCV is *not* required to use the face_recognition library.
# It's only required if you want to run this
# specific demo. If you have trouble installing it,
# try any of the other demos that don't require it instead.

main_path = os.path.dirname(__file__)
result_path = os.path.join(main_path, "result")

#there're the least two images in all folders
def multi_images(foldername, filename):
       images_main_path = os.path.join(main_path, "images", foldername)

       names = os.listdir(images_main_path)
       images_paths = {name : os.listdir(
                              os.path.join(images_main_path,
                                           name)) for name in names}
       # Load a sample picture and learn how to recognize it.
       # compute encoding of each face
       all_face_encodings = []
       index = 0 #index
       for name in names:
           all_face_encodings.append({"name" : name, "encodings" : []})
           for img in images_paths[name]:
               if not img.startswith("."):               
                      try:
                             image = face_recognition.load_image_file(
                                           os.path.join(images_main_path, name, img)
                                           )
                             encoding = face_recognition.face_encodings(image)[0] 
                             all_face_encodings[index]["encodings"].append(encoding)                                  
                      except:
                             pass
           index += 1
       
       print "all_face_encodings = {}".format(len(all_face_encodings))
       average_face_encoding = []
       for face in all_face_encodings:
           try:
               #computing average face encoding for each person
               result = sum(face["encodings"]) / len(face["encodings"])
               average_face_encoding.append({"name" : face["name"],
                                         "encodings" : list(result)})
           except:
               print face["name"]
       
       #save model
       fp = codecs.open(os.path.join(result_path, "{}.json".format(filename)),
                        "w", encoding='utf-8')              
       ### this saves the array in .json format
       json.dump(average_face_encoding, fp, separators=(',', ':'), 
                 sort_keys=True, indent=4)          
       fp.close()

#there's just one image in all folders
def sigle_images(foldername, filename): 
       images_main_path = os.path.join(main_path, "images", foldername)
              
       names = os.listdir(images_main_path)
       images_paths = {name : os.listdir(
                              os.path.join(images_main_path,
                                           name)) for name in names}
       
       ## Load a sample picture and learn how to recognize it.
       ## compute encoding of each face
       all_face_encodings = []
       index = 0 #index
       for name in names:
           all_face_encodings.append({"name" : name})
           for img in images_paths[name]:
               if not img.startswith("."):               
                      try:
                             image = face_recognition.load_image_file(
                                           os.path.join(images_main_path, name, img)
                                           )
                             encoding = face_recognition.face_encodings(image)[0] 
                             all_face_encodings[index]["encodings"]= list(encoding)                                  
                      except:
                          pass
           index += 1
       
       #save model
       fp = codecs.open(os.path.join(result_path, "{}.json".format(filename)), 
                        "w", encoding='utf-8')       
       json.dump(all_face_encodings, fp, separators=(',', ':'), 
                 sort_keys=True, indent=4) ### this saves the array in .json format
                  
       fp.close()

if __name__ == "__main__":
       # python train.py --mod multi --foldname train_gender --filename face_encodings_gender
       parser = argparse.ArgumentParser(description='Process some integers.')
       parser.add_argument("--mod", type=str, 
                    help="choosing mod", default = "sigle")
       parser.add_argument("--foldname", type=str,
                    help="file name", default = "train_single")
       parser.add_argument("--filename", type=str,
                    help="file name", default = "face_encodings_sigle")
       args = parser.parse_args()
#       print args.foldname
       if args.mod == "sigle":
              sigle_images(args.foldname, args.filename)
       elif args.mod == "multi":
              multi_images(args.foldname, args.filename)
