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

def get_image_from_s3(bucket_name, key):
    try:
        print("get_image_from_s3 " + bucket_name + " " + key)
        s3 = boto3.resource('s3')
        obj = s3.Object(
            bucket_name=bucket_name,
            key=key,
        )
        obj_body = obj.get()['Body'].read()
        img = Image.open(BytesIO(obj_body))
        return img
    except:
        print("ERROR: get_image_from_s3");
        return None

def get_image(event, context):
    width = ''
    height = ''
    anchor = 'middlecenter'
    
    if event.get('queryStringParameters',{}) is not None:
        width = event.get('queryStringParameters',{}).get('width','')
        height = event.get('queryStringParameters',{}).get('height','')
        anchor = event.get('queryStringParameters',{}).get('anchor','middlecenter')

    path = event["path"]
    path = path.replace('/s3/', '')
    print("GET image path " + path + " | width:" + width + " | height:" + height + " | anchor:" + anchor)
    paths = path.split("/", 1)
    
    bucketname = paths[0]
    filename = paths[1]

    fileextension = filename.split(".")[-1]
    fileextensionformat = "JPEG"
    if fileextension == "png":
        fileextensionformat = "PNG"
    
    # width and height is exist
    if width is not None and width != "" and height is not None and height != "":
        size = width + "x" + height
        img = resize_image(bucketname, filename, size, anchor) 
        
        buffered = io.BytesIO()
        img.save(buffered, format=fileextensionformat)
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
    # only width specified in query string
    elif width != "" and height == "":
        img = get_image_from_s3(bucketname, filename)
        original_width, original_height = img.size
        height = float(original_height/original_width) * float(width)

        # resize from the original image
        new_size = (int(width), int(height))
        img = img.resize(new_size, PIL.Image.LANCZOS)

        buffered = io.BytesIO()

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(buffered, format=fileextensionformat)
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
    # only height specified in query string
    elif width == "" and height != "":
        img = get_image_from_s3(bucketname, filename)
        original_width, original_height = img.size
        width = float(original_width/original_height) * float(height) 

        # resize from the original image
        new_size = (int(width), int(height))
        img = img.resize(new_size, PIL.Image.LANCZOS)

        buffered = io.BytesIO()

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(buffered, format=fileextensionformat)
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
    # no querystring specified, just get the actual image from S3
    else:
        img = get_image_from_s3(bucketname, filename)
        buffered = io.BytesIO()

        if img.mode != 'RGB':
            img = img.convert('RGB')
            
        img.save(buffered, format=fileextensionformat)
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
    
    response = {
        'isBase64Encoded': True,
        'statusCode': 200,
        'headers': {'Content-Type': 'image/jpg'},
        'body': img_str,
    }
    return response

def resize_crop_top(image, size):
    """
    Crop the image from top centered rectangle of the specified size
    image:      a Pillow image instance
    size:       a list of two integers [width, height]
    """
    img_format = image.format
    image = image.copy()
    old_size = image.size
    left = (old_size[0] - size[0]) / 2
    top = 0
    right = old_size[0] - left
    bottom = size[1]
    rect = [int(math.ceil(x)) for x in (left, top, right, bottom)]
    left, top, right, bottom = rect
    print("rect" + str(left) + " "+ str(top) + " "+ str(right) + " "+ str(bottom) + " ")
    crop = image.crop((left, top, right, bottom))
    crop.format = img_format
    return crop    

def resize_crop_center(image, size):
    """
    Crop the image with a centered rectangle of the specified size
    image:      a Pillow image instance
    size:       a list of two integers [width, height]
    """
    img_format = image.format
    image = image.copy()
    old_size = image.size
    left = (old_size[0] - size[0]) / 2
    top = (old_size[1] - size[1]) / 2
    right = old_size[0] - left
    bottom = top + size[1]
    rect = [int(math.ceil(x)) for x in (left, top, right, bottom)]
    left, top, right, bottom = rect
    print("rect" + str(left) + " "+ str(top) + " "+ str(right) + " "+ str(bottom) + " ")
    crop = image.crop((left, top, right, bottom))
    crop.format = img_format
    return crop    

def resize_cover(image, size, anchor, resample=Image.LANCZOS):
    """
    Resize image according to size.
    image:      a Pillow image instance
    size:       a list of two integers [width, height]
    """
    img_format = image.format
    img = image.copy()
    img_size = img.size
    ratio = max(size[0] / img_size[0], size[1] / img_size[1])
    new_size = [
        int(math.ceil(img_size[0] * ratio)),
        int(math.ceil(img_size[1] * ratio))
    ]
    img = img.resize((new_size[0], new_size[1]), resample)
    
    if anchor == 'topcenter':
        print("resize_crop_top")
        img = resize_crop_top(img, size)
    else:
        print("resize_crop_center")
        img = resize_crop_center(img, size)

    img.format = img_format
    return img    

def resize_image(bucket_name, key, size, anchor):
    size_split = size.split('x')
    resize_width = int(size_split[0])
    resize_height = int(size_split[1])

    key_paths = key.split('/')
    filename = key_paths[-1]
    anchorinfilename = "" # by default anchor is center and in filename is empty, if topcenter then anchor in filename is topcenter to differentiate with default image 
    if anchor == 'topcenter':
        anchorinfilename = '-topcenter'
    
    resized_filename = "{size}{anchor}_{key}".format(size=size, anchor=anchorinfilename, key=filename)
    resized_key = key.replace(filename, resized_filename)
    s3 = boto3.resource('s3')

    print("resized_key " + resized_key)
    resized_image = get_image_from_s3(bucket_name, resized_key)
    if resized_image is None:
        print("resized_image: NONE")
        img = get_image_from_s3(bucket_name, key);
        if img is None:
            return ""

        original_width, original_height = img.size
        resize_ratio = min(resize_width / original_width, resize_height / original_height)
        new_size = (int(original_width * resize_ratio), int(original_height * resize_ratio))

        img = resize_cover(img, [resize_width, resize_height], anchor)
            
        buffer = BytesIO()

        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.save(buffer, 'JPEG')
        buffer.seek(0)

        try:
            obj = s3.Object(
                bucket_name=bucket_name,
                key=resized_key,
            )
            obj.put(Body=buffer, ContentType='image/jpeg')
            print("Image " + resized_key + ' saved to S3 ' + bucket_name )
        except:
            print("ERROR save image to S3")
        return img
    else:
        print("return existing image " + resized_key)
        return resized_image