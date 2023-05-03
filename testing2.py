import cv2
import boto3
import io
from PIL import Image
import os
import time
  
   
# Create an object to read 
# from camera
video = cv2.VideoCapture(0)
print("get!")
# We need to check if camera
# is opened previously or not
if (video.isOpened() == False): 
    print("Error reading video file")
  
# We need to set resolutions.
# so, convert them from float to integer.
frame_width = int(video.get(3))
frame_height = int(video.get(4))
   
size = (frame_width, frame_height)
   
# Below VideoWriter object will create
# a frame of above defined The output 
# is stored in 'filename.avi' file.
result = cv2.VideoWriter('./capture_img/capture.mp4', 
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         10, size)
t_end = time.time() + 3
  
while time.time() < t_end:
    ret, frame = video.read()
  
    if ret == True: 
  
        # Write the frame into the
        # file 'filename.avi'
        result.write(frame)
  
        # Display the frame
        # saved in the file
        cv2.imshow('Frame', frame)
  
        # Press S on keyboard 
        # to stop the process
        if cv2.waitKey(1) & 0xFF == ord('s'):
            break
  
    # Break the loop
    else:
        break
  
# When everything done, release 
# the video capture and video 
# write objects
video.release()
result.release()
    
# Closes all the frames
cv2.destroyAllWindows()
   
print("The video was successfully saved")
sucess =0
vidcap = cv2.VideoCapture('./capture_img/capture.mp4')
vidcap.set(cv2.CAP_PROP_FPS, 30)

count = 0
number=0
success = True
while success:
	success,image = vidcap.read()
	if(count % 4 == 0):
		cv2.imwrite("./capture_img/frame%d.jpg" % number, image)     # save frame as JPEG file      
		print('Read a new frame: ', success)
		number += 1
	
	count += 1
vidcap.release() 
rekognition = boto3.client('rekognition', region_name='us-east-1')
dynamodb = boto3.client('dynamodb', region_name='us-east-1')
for i in range(number):
    image_path = "./capture_img/frame%d.jpg" % i

    image = Image.open(image_path)
    stream = io.BytesIO()
    image.save(stream,format="JPEG")
    image_binary = stream.getvalue()


    response = rekognition.search_faces_by_image(
            CollectionId='famouspersons',
            Image={'Bytes':image_binary}                                       
            )

    found = False
    for match in response['FaceMatches']:
        print (match['Face']['FaceId'],match['Face']['Confidence'])
            
        face = dynamodb.get_item(
            TableName='facerecognition',  
            Key={'RekognitionId': {'S': match['Face']['FaceId']}}
            )
        
        if 'Item' in face:
            print ("Found Person: ",face['Item']['FullName']['S'])
            found = True
            success +=1

    if not found:
        print("Person cannot be recognized")
if (success / number) < 0.85:
    print("Can't recognized your face, please try again")
else:
    print("Successful, you are the right person")
for file in os.listdir('./capture_img'):
    if file.endswith('.jpg'):
        os.remove('./capture_img/' + file) 

os.remove("./capture_img/capture.mp4")