from tkinter import messagebox
from Support import social_distancing_config as config
from Support.detection import detect_people
from scipy.spatial import distance as dist
import numpy as np
import argparse
import imutils
import cv2
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import screeninfo
from datetime import datetime
from pygame import mixer
import uuid
import os
from docx import Document
import docx
import pandas as pd
import openpyxl
import xlsxwriter
import win32com.client as win32
import time

def start():

	#sound alert
	mixer.init()
	sound = mixer.Sound('./Sounds/alert.wav')

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--input", type=str, default="")
	ap.add_argument("-o", "--output", type=str, default="")
	ap.add_argument("-d", "--display", type=int, default=1)
	args = vars(ap.parse_args())

	# load the COCO class labels our YOLO model was trained on
	labelsPath = os.path.sep.join([config.MODEL_PATH, "coco.names"])
	LABELS = open(labelsPath).read().strip().split("\n")

	# derive the paths to the YOLO weights and model configuration
	weightsPath = os.path.sep.join([config.MODEL_PATH, "yolov3.weights"])
	configPath = os.path.sep.join([config.MODEL_PATH, "yolov3.cfg"])

	# load our YOLO object detector trained on COCO dataset (80 classes)
	print("[INFO] Loading YOLO from Disk...")
	net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)

	# check if we are going to use GPU
	if config.USE_GPU:
		# set CUDA as the preferable backend and target
		print("[INFO] Setting Preferable Backend and Target to CUDA...")
		net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)
		net.setPreferableTarget(cv2.dnn.DNN_TARGET_CUDA)
	

	# determine only the *output* layer names that we need from YOLO
	ln = net.getLayerNames()
	ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

	# initialize the video stream and pointer to output video file
	print("[INFO] Switching on Camera...")
	if config.USE_MOBILE_CAMERA==False:
		vs = cv2.VideoCapture(0,cv2.CAP_DSHOW)
		if(vs.isOpened()==False):
			messagebox.showerror("Error","No Webcam Detected.")
	else:
		vs = cv2.VideoCapture(1,cv2.CAP_DSHOW)
		address=config.IP_WEBCAM_ADDRESS
		vs.open(address)
		if vs is None or not vs.isOpened():
			messagebox.showerror("Error","IP Webcam app server is not live.\nStart the server and recheck whether URL entered is correct.")
	writer = None

	# loop over the frames from the video stream
	# used to record the time when we processed last frame
	prev_frame_time = 0
	
	# used to record the time at which we processed current frame
	new_frame_time = 0

	while True:
		# read the next frame from the file
		(grabbed, frame) = vs.read()
		new_frame_time = time.time()

		# if the frame was not grabbed, then we have reached the end
		# of the stream
		if not grabbed:
			break

		# resize the frame and then detect people (and only people) in it
		frame = imutils.resize(frame, width=700)
		results = detect_people(frame, net, ln,
			personIdx=LABELS.index("person"))

		# initialize the set of indexes that violate the minimum social
		# distance
		violate = set()

		# ensure there are *at least* two people detections (required in
		# order to compute our pairwise distance maps)
		if len(results) >= 2:
			# extract all centroids from the results and compute the
			# Euclidean distances between all pairs of the centroids
			centroids = np.array([r[2] for r in results])
			D = dist.cdist(centroids, centroids, metric="euclidean")

			# loop over the upper triangular of the distance matrix
			for i in range(0, D.shape[0]):
				for j in range(i + 1, D.shape[1]):
					# check to see if the distance between any two
					# centroid pairs is less than the configured number
					# of pixels
					if D[i, j] < config.MIN_DISTANCE:
						# update our violation set with the indexes of
						# the centroid pairs
						violate.add(i)
						violate.add(j)

		# loop over the results
		for (i, (prob, bbox, centroid)) in enumerate(results):
			# extract the bounding box and centroid coordinates, then
			# initialize the color of the annotation
			(startX, startY, endX, endY) = bbox
			(cX, cY) = centroid
			color = (0, 255, 0)

			# if the index pair exists within the violation set, then
			# update the color
			if i in violate:
				color = (0, 0, 255)

			# draw (1) a bounding box around the person and (2) the
			# centroid coordinates of the person,
			cv2.rectangle(frame, (startX, startY), (endX, endY), color, 2)
			cv2.circle(frame, (cX, cY), 5, color, 1)

		# date and time
		now = datetime.now()
		year = now.strftime("%Y")
		month = now.strftime("%m")
		day = now.strftime("%d")
		time1 = now.strftime("%H:%M:%S")
		date_time = now.strftime("%m/%d/%Y %H:%M:%S")
		sec=now.strftime("%S")
		secint=int(sec)
		cv2.putText(frame, date_time,(475, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.6,(255, 255, 255), 1, cv2.LINE_8)
		textLive = "Live"
		textblank="    "
		if (secint%2==0):
			cv2.putText(frame, textLive,(10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255, 255, 255), 2, cv2.LINE_8)
		else:
			cv2.putText(frame, textblank,(10, 25),cv2.FONT_HERSHEY_SIMPLEX, 0.8,(255, 255, 255), 2, cv2.LINE_8)

		def is_cuda_cv(): # 1 == using cuda, 0 = not using cuda
			try:
				count = cv2.cuda.getCudaEnabledDeviceCount()
				if count > 0:
					return 1
				else:
					return 0
			except:
				return 0
		
		# time when we finish processing for this frame
		new_frame_time = time.time()
		fps = 1/(new_frame_time-prev_frame_time)
		prev_frame_time = new_frame_time
		fps = int(fps)
		fps = str(fps)
		cv2.putText(frame,"FPS:"+fps,(10,55),cv2.FONT_HERSHEY_SIMPLEX, 0.6,(0, 255, 0), 2, cv2.LINE_8)


		textGpu="GPU"
		textCpu="CPU"
		if(is_cuda_cv()==1):
			if(config.USE_GPU==True):
				cv2.putText(frame, textGpu,(660, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 1, cv2.LINE_8)
			else:
				cv2.putText(frame, textCpu,(660, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 1, cv2.LINE_8)
		else:
			cv2.putText(frame, textCpu,(660, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5,(0, 255, 0), 1, cv2.LINE_8)

		if(config.USE_SOCIAL_DISTANCE==True):
			# draw the total number of social distancing violations on the
			# output frame
			textSDV = "Social Distancing Violations: {}".format(len(violate))
			if len(violate)>0:
				cv2.putText(frame, textSDV, (50, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
			else:
				cv2.putText(frame, textSDV, (50, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
		elif(config.USE_HUMAN_COUNT==True):
			#Total number of person
			textTP = "No of People: {}".format(len(results))
			#Here to make changes later on
			if len(results) < config.MAX_PEOPLE:
				cv2.putText(frame, textTP, (475, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
				sound.stop()
			else:
				cv2.putText(frame, textTP, (475, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
				sound.play()
		else:
			# draw the total number of social distancing violations on the
			# output frame
			textSDV = "Social Distancing Violations: {}".format(len(violate))
			if len(violate)>0:
				cv2.putText(frame, textSDV, (50, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
			else:
				cv2.putText(frame, textSDV, (50, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

			#Total number of person
			textTP = "No of People: {}".format(len(results))
			#Here to make changes later on
			if len(results) < config.MAX_PEOPLE:
				cv2.putText(frame, textTP, (475, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
				sound.stop()
			else:
				cv2.putText(frame, textTP, (475, frame.shape[0] - 25), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255), 2)
				sound.play()
	
		if(config.Write_Data_Text_File==True):			
			if(config.USE_DATA_BOTH==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistanceAndHumanCount():
						file.write('\n******Social_Distance_Violations_and_Realtime_Human_Count with Limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet1
					except:
						onlyonceSocialDistanceAndHumanCount()
						oncet1 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(violate)),format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, %s, %s, No\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						fileRaw.write('%s, %s, %s, Yes\n'%(format(len(violate)),format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
					
			elif(config.USE_DATA_HUMAN_COUNT==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceHumanCount():
						file.write('\n******Human_Count with limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet2
					except:
						onlyonceHumanCount()
						oncet2 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Human_Count: %s recorded_at %s\n'%(format(len(results)),date_time))
					else:
						file.write('Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('NA, %s, %s, No\n'%(format(len(results)),date_time))
					else:
						fileRaw.write('NA, %s, %s, Yes\n'%(format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
					
			elif(config.USE_DATA_SOCIAL_DISTANCE==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistance():
						file.write('\n******Social_Distance_Violations on %s.******\n' %(date_time))
					try:
						oncet3
					except:
						onlyonceSocialDistance()
						oncet3 = 1
					file.write('Social_Distance_Violations: %s recorded_at %s\n'%(format(len(violate)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, NA, %s, No\n'%(format(len(violate)),date_time))
					else:
						fileRaw.write('%s, NA, %s, Yes\n'%(format(len(violate)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()		

		elif(config.Write_Data_Word_File==True):
			if(config.USE_DATA_BOTH==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistanceAndHumanCount():
						file.write('\n******Social_Distance_Violations_and_Realtime_Human_Count with Limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet1
					except:
						onlyonceSocialDistanceAndHumanCount()
						oncet1 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(violate)),format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, %s, %s, No\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						fileRaw.write('%s, %s, %s, Yes\n'%(format(len(violate)),format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
					
			elif(config.USE_DATA_HUMAN_COUNT==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceHumanCount():
						file.write('\n******Human_Count with limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet2
					except:
						onlyonceHumanCount()
						oncet2 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Human_Count: %s recorded_at %s\n'%(format(len(results)),date_time))
					else:
						file.write('Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('NA, %s, %s, No\n'%(format(len(results)),date_time))
					else:
						fileRaw.write('NA, %s, %s, Yes\n'%(format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()		
					
			elif(config.USE_DATA_SOCIAL_DISTANCE==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistance():
						file.write('\n******Social_Distance_Violations on %s.******\n' %(date_time))
					try:
						oncet3
					except:
						onlyonceSocialDistance()
						oncet3 = 1
					file.write('Social_Distance_Violations: %s recorded_at %s\n'%(format(len(violate)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, NA, %s, No\n'%(format(len(violate)),date_time))
					else:
						fileRaw.write('%s, NA, %s, Yes\n'%(format(len(violate)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	

			def matches_my_condition(line):
				return line

			# Prepare document
			document = Document()

			with open('Data.txt', 'r') as textfile:
				for line in textfile.readlines():
					if matches_my_condition(line):
						document.add_paragraph(line)

			document.save('Data.docx')

		elif(config.Write_Data_Excel_File==True):			
			if(config.USE_DATA_BOTH==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistanceAndHumanCount():
						file.write('\n******Social_Distance_Violations_and_Realtime_Human_Count with Limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet1
					except:
						onlyonceSocialDistanceAndHumanCount()
						oncet1 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						file.write('Social_Distance_Violations: %s Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(violate)),format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, %s, %s, No\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						fileRaw.write('%s, %s, %s, Yes\n'%(format(len(violate)),format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()

				with open("DataTemp.txt",mode='a') as file:
					if len(results)<config.MAX_PEOPLE:
						file.write('%s,%s,%s,NO\n'%(format(len(violate)),format(len(results)),date_time))
					else:
						file.write('%s,%s,%s,YES\n'%(format(len(violate)),format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("DataTemp.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				
				
				data = pd.read_csv("DataTemp.txt",header = None)
				data.columns = ['Social Distance Violations', 'Human Count', 'Recorded at','Human Count Limit Reached?']
				data.to_csv('Data.csv', index = None)
				datafinal = pd.read_csv('Data.csv') 
				datafinal.to_excel('Data.xlsx', 'Sheet1', index=False)
							


					
			elif(config.USE_DATA_HUMAN_COUNT==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceHumanCount():
						file.write('\n******Human_Count with limit: %s on %s.******\n' %(config.MAX_PEOPLE,date_time))
					try:
						oncet2
					except:
						onlyonceHumanCount()
						oncet2 = 1
					if len(results)<config.MAX_PEOPLE:
						file.write('Human_Count: %s recorded_at %s\n'%(format(len(results)),date_time))
					else:
						file.write('Human_Count: %s recorded_at %s (Limit Reached!)\n'%(format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('NA, %s, %s, No\n'%(format(len(results)),date_time))
					else:
						fileRaw.write('NA, %s, %s, Yes\n'%(format(len(results)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				
				with open("DataTemp.txt",mode='a') as file:
					if len(results)<config.MAX_PEOPLE:
						file.write('%s,%s,NO\n'%(format(len(results)),date_time))
					else:
						file.write('%s,%s,YES\n'%(format(len(results)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("DataTemp.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	
				
				data = pd.read_csv("DataTemp.txt",header = None)
				data.columns = ['Human Count', 'Recorded at','Human Count Limit Reached?']
				data.to_csv('Data.csv', index = None)
				datafinal = pd.read_csv('Data.csv') 
				datafinal.to_excel('Data.xlsx', 'Sheet1', index=False)

			elif(config.USE_DATA_SOCIAL_DISTANCE==True):
				with open("Data.txt",mode='a') as file:
					def onlyonceSocialDistance():
						file.write('\n******Social_Distance_Violations on %s.******\n' %(date_time))
					try:
						oncet3
					except:
						onlyonceSocialDistance()
						oncet3 = 1
					file.write('Social_Distance_Violations: %s recorded_at %s\n'%(format(len(violate)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("Data.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()
				with open("Records/RawData.txt",mode='a+') as fileRaw:
					if len(results)<config.MAX_PEOPLE:
						fileRaw.write('%s, NA, %s, No\n'%(format(len(violate)),date_time))
					else:
						fileRaw.write('%s, NA, %s, Yes\n'%(format(len(violate)),date_time))
					fileRaw.close()
				with open("Records/RawData.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	

				with open("DataTemp.txt",mode='a') as file:
					file.write('%s,%s\n'%(format(len(violate)),date_time))
					file.close()
				lines_seen = set() # holds lines already seen
				with open("DataTemp.txt", mode='r+') as f:
						d = f.readlines()
						f.seek(0)
						for i in d:
							
							if i not in lines_seen:
								f.write(i)
								lines_seen.add(i)
						f.truncate()	

				data = pd.read_csv("DataTemp.txt",header = None)
				data.columns = ['Social Distance Violations', 'Recorded at']
				data.to_csv('Data.csv', index = None)
				datafinal = pd.read_csv('Data.csv') 
				datafinal.to_excel('Data.xlsx', 'Sheet1', index=False)
		

		
		# check to see if the output frame should be displayed to our
		# screen
		if args["display"] > 0:
			# show the output frame
			cv2.namedWindow("Live", cv2.WINDOW_NORMAL)
			cv2.setWindowProperty("Live", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
			cv2.imshow("Live", frame)
			key = cv2.waitKey(1) & 0xFF

			# if the `ESC` key is pressed, break from the loop			
			if key == 27:
				
				if(config.Write_Data_Text_File==True or config.Write_Data_Word_File==True or config.Write_Data_Excel_File==True):
					f1 = open("Records/AllData.txt", 'a+')
					f2 = open("Data.txt", 'r')
					f1.write(f2.read())
					f1.close()
					f2.close()
				
				if(config.Write_Data_Word_File==True):
					if os.path.exists("Data.txt"):
						os.remove("Data.txt")
					if os.path.exists("Data.csv"):
						os.remove("Data.csv")
					if os.path.exists("DataTemp.txt"):
						os.remove("DataTemp.txt")
					if os.path.exists("Data.xlsx"):
						os.remove("Data.xlsx")
				elif(config.Write_Data_Text_File==True):
					if os.path.exists("Data.docx"):
						os.remove("Data.docx")
					if os.path.exists("Data.csv"):
						os.remove("Data.csv")
					if os.path.exists("DataTemp.txt"):
						os.remove("DataTemp.txt")
					if os.path.exists("Data.xlsx"):
						os.remove("Data.xlsx")
				elif(config.Write_Data_Excel_File==True):
					if os.path.exists("Data.docx"):
						os.remove("Data.docx")
					if os.path.exists("Data.txt"):
						os.remove("Data.txt")
					if os.path.exists("Data.csv"):
						os.remove("Data.csv")
					if os.path.exists("DataTemp.txt"):
						os.remove("DataTemp.txt")
				
				if(config.Write_Data_Excel_File==True):
					if(config.USE_DATA_BOTH==True):
						writer = pd.ExcelWriter('Data.xlsx') 
						datafinal.to_excel(writer, sheet_name='Output', index=False, na_rep='NA')
						col_idx1 = datafinal.columns.get_loc('Social Distance Violations')
						writer.sheets['Output'].set_column(col_idx1, col_idx1, 30)
						col_idx2 = datafinal.columns.get_loc('Human Count')
						writer.sheets['Output'].set_column(col_idx2, col_idx2, 30)
						col_idx3 = datafinal.columns.get_loc('Recorded at')
						writer.sheets['Output'].set_column(col_idx3, col_idx3, 30)
						col_idx4 = datafinal.columns.get_loc('Human Count Limit Reached?')
						writer.sheets['Output'].set_column(col_idx4, col_idx4, 30)
						writer.save()
					elif(config.USE_DATA_HUMAN_COUNT==True):
						writer = pd.ExcelWriter('Data.xlsx') 
						datafinal.to_excel(writer, sheet_name='Output', index=False, na_rep='NA')
						col_idx2 = datafinal.columns.get_loc('Human Count')
						writer.sheets['Output'].set_column(col_idx2, col_idx2, 30)
						col_idx3 = datafinal.columns.get_loc('Recorded at')
						writer.sheets['Output'].set_column(col_idx3, col_idx3, 30)
						col_idx4 = datafinal.columns.get_loc('Human Count Limit Reached?')
						writer.sheets['Output'].set_column(col_idx4, col_idx4, 30)
						writer.save()
					elif(config.USE_DATA_SOCIAL_DISTANCE==True):
						writer = pd.ExcelWriter('Data.xlsx') 
						datafinal.to_excel(writer, sheet_name='Output', index=False, na_rep='NA')
						col_idx1 = datafinal.columns.get_loc('Social Distance Violations')
						writer.sheets['Output'].set_column(col_idx1, col_idx1, 30)
						col_idx3 = datafinal.columns.get_loc('Recorded at')
						writer.sheets['Output'].set_column(col_idx3, col_idx3, 30)
						writer.save()



				cv2.destroyAllWindows()
				
				break
			

		

		# if the video writer is not None, write the frame to the output
		# video file
		if writer is not None:
			writer.write(frame)



