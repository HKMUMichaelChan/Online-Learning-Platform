from datetime import datetime, timedelta
import os
from PIL import Image
from flask import  session
import jwt

from route.redirectPage import redirectPage


def create_blank_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, 'w') as file:
            pass

# e.g.
# file_path = "path/to/your/file.txt"
# create_blank_file(file_path)
def authVerify(app, permissionLevel):
    if 'token' in session:
        try:
            token = session['token']

            payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            if datetime.utcnow() > datetime.fromtimestamp(payload['exp']):
                return redirectPage("/login", "The token has expired, please login again!")

            if int(session['username'][0]) < permissionLevel:
                return redirectPage("/login", "Insufficient authority")

            return None #No Error
        except jwt.ExpiredSignatureError:
            return redirectPage("/login", "The token has expired, please log in again!")
        except jwt.InvalidTokenError:
            return redirectPage("/login", "Invalid token, please log in again!")    
    else:
        return redirectPage("/login", "Not logged in, please log in")  

def tokenAlive(app):
    token = session['token']
    authError = authVerify(app, 1)
    if authError is not None:
        return authError
    else:
        decoded_payload = jwt.decode(token, app.secret_key, algorithms=['HS256'])
        if decoded_payload is not None:
            expiration_time = datetime.utcnow() + timedelta(minutes=30)
            decoded_payload['exp'] = expiration_time
            return jwt.encode(decoded_payload, app.secret_key, algorithm='HS256')

def crop_to_square(image_path):

    image = Image.open(image_path)


    width, height = image.size


    size = min(width, height)

    left = (width - size) // 2
    top = (height - size) // 2
    right = left + size
    bottom = top + size


    cropped_image = image.crop((left, top, right, bottom))

    cropped_image.save(image_path)
# e.g.
# image_path = "path/to/your/image.jpg"
# crop_to_square(image_path)



def convert_png_to_jpg(png_file, jpg_path):

    image = Image.open(png_file)


    if image.mode == 'RGBA':
        image = image.convert('RGB')

    image.save(jpg_path, 'JPEG')


# e.g.
# image_path = "path/to/your/image.jpg"
# convert_png_to_jpg(png_file, image_path)
