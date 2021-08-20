import requests
import cv2
import math
from random import randint
from random import random
import argparse
import os


genders=['Male','Female']
faceNet=cv2.dnn.readNet("opencv_face_detector_uint8.pb","opencv_face_detector.pbtxt")
ageNet=cv2.dnn.readNet("age.caffemodel","age.prototxt")
genderNet=cv2.dnn.readNet("gender.caffemodel","gender.prototxt")

parser = argparse.ArgumentParser(description='Generate random identity')
parser.add_argument('-m', help='male identity', action="store_true")
parser.add_argument('-f', help='female identity', action='store_true')
parser.add_argument('-i', type=str, help='additional information, e.g. website', default='')
args = parser.parse_args()


def find_face():
	with open('temp.jpg', 'wb') as f:
		f.write(requests.get('https://thispersondoesnotexist.com/image').content)
	video=cv2.VideoCapture('temp.jpg')

	hasFrame,frame=video.read()
	height, width=frame.shape[:2]
	blob=cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 177, 123], True, False)

	faceNet.setInput(blob)
	detections=faceNet.forward()
	for i in range(detections.shape[2]):
		if detections[0,0,i,2]>0.7:
			x1, x2 = int(detections[0,0,i,3]*width), int(detections[0,0,i,5]*width)
			y1, y2 = int(detections[0,0,i,4]*height), int(detections[0,0,i,6]*height)
			return frame, [x1,y1,x2,y2]
	find_face()

		
def get_age_sex():
	frame, box = find_face()
	
	face=frame[max(0,box[1]-20):
			   min(box[3]+20,frame.shape[0]-1),max(0,box[0]-20)
			   :min(box[2]+20, frame.shape[1]-1)]

	blob=cv2.dnn.blobFromImage(face, 1.0, (227,227), (78, 87, 114), swapRB=False)
	genderNet.setInput(blob)
	ageNet.setInput(blob)
	
	return ageNet.forward()[0].argmax(), genders[genderNet.forward()[0].argmax()]


def randomize_age(bracket):
	if bracket == 0:
		return randint(0, 2)
	elif bracket == 1:
		return randint(4, 6)
	elif bracket == 2:
		return randint(8, 12)
	elif bracket == 3:
		return randint(15, 20)
	elif bracket == 4:
		return randint(25, 32)
	elif bracket == 5:
		return randint(38, 43)
	elif bracket == 6:
		return randint(48, 53)
	elif bracket == 7:
		return randint(60, 100)
	else:
		return randint(20, 40)

	
def get_name(gender):
	firstname = "John"
	lastname = "Doe"
	names = []
	
	with open(gender + "_names.txt") as fh:
		names = fh.readlines()
	index = math.floor(abs(random() - random()) * (1 + len(names)))
	firstname = names[index].rstrip()
	
	with open("lastnames.txt") as fh:
		names = fh.readlines()
	index = math.floor(abs(random() - random()) * (1 + len(names)))
	lastname = names[index].rstrip()
	return firstname.title(), lastname.title()


def start():
	agebracket, gender = get_age_sex()
	
	if (args.m and gender == 'Female') or (args.f and gender == 'Male'):
		start()
	else:
		age = randomize_age(agebracket)
		firstname, lastname = get_name(gender)
		if args.i != '':
			os.rename('temp.jpg', "identities/" + args.i + "_" + firstname + " " + lastname + ", " + str(age) + ".jpg")
		else:
			os.rename('temp.jpg', "identities/" + firstname + " " + lastname + ", " + str(age) + ".jpg")
		print("Created " + firstname + " " + lastname + ", " + str(age) + " years old")
	
	
start()
