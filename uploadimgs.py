import boto3

s3 = boto3.resource('s3')

# Following are just example of uploading pictures into bucket
images=[('image1.jpg','Wenjun'),
      ('image2.jpg','Wenjun'),
      
      ]

# Iterate through list to upload objects to S3   
for image in images:
    file = open(image[0],'rb')
    object = s3.Object('famouspersons-images','index/'+ image[0])
    ret = object.put(Body=file,
                    Metadata={'FullName':image[1]})
