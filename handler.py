import json
import boto3
import io
from io import BytesIO
import PIL
from PIL import Image
bucket = "digital-cougar-assets"
import math
import base64
# from resizeimage import resizeimage
s3 = boto3.resource('s3')  



def test(event, context):
    print(event)
    print(context)