# base path to YOLO directory
from sqlalchemy import true

# define the minimum safe distance (in pixels) that two people can be
# from each other
MIN_DISTANCE = 50

MODEL_PATH = "yolo-coco"

# initialize minimum probability to filter weak detections along with
# the threshold when applying non-maxima suppression
MIN_CONF = 0.3
NMS_THRESH = 0.3

#social distance enable
USE_SOCIAL_DISTANCE=False

#realtime Human Count
USE_HUMAN_COUNT=False

#use both
USE_BOTH=False

#boolean to check whether mobile camera is used 
USE_MOBILE_CAMERA=False

#device camera
USE_DEVICE_CAMERA=False

#ip webcam address
IP_WEBCAM_ADDRESS="none"

# boolean indicating if NVIDIA CUDA GPU should be used
USE_GPU = True

#cpu should be used
USE_CPU = True

#define max number of people at a time.
#if it increases above limit alarm triggered
MAX_PEOPLE=20

#Data social distance and human count
USE_DATA_BOTH=False

#Data social distance
USE_DATA_SOCIAL_DISTANCE=False

#Data human count
USE_DATA_HUMAN_COUNT=False

#Write Data Text File
Write_Data_Text_File=False

#Write Data Word File
Write_Data_Word_File=False

#no data write
No_Data_Write=False

#write data excel file
Write_Data_Excel_File=False

#camera check
webcamworking=False
