from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

from PIL import Image, ImageDraw, ImageFont

# Add your Computer Vision subscription key to your environment variables.
if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
    subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
else:
    print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()
# Add your Computer Vision endpoint to your environment variables.
if 'COMPUTER_VISION_ENDPOINT' in os.environ:
    endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
else:
    print("\nSet the COMPUTER_VISION_ENDPOINT environment variable.\n**Restart your shell or IDE for changes to take effect.**")
    sys.exit()

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))





def describir_imagenes():
    imagen = open('images/living2.jpg', 'rb')
    '''
    Describe las imágenes con un cierto nivel de porcentaje

    '''
    print("===== Describe an image - remote =====")
    # Call API
    descripcion_imagen = computervision_client.describe_image_in_stream(imagen)


    # Get the captions (descriptions) from the response, with confidence level
    print("Description of remote image: ")
    if (len(descripcion_imagen.captions) == 0):
        print("No description detected.")
    else:
        for descripcion in descripcion_imagen.captions:
            texto = "'{}' with confidence {:.2f}%".format(descripcion.text, descripcion.confidence * 100)
            print(texto)
            return texto;


def categorias_imagenes():
    imagen = open('images/living2.jpg', 'rb')
    '''
    Detecta los objetos de una imagen
    '''
    
    # Get URL image with different objects

    # Call API with URL
    descripcion = describir_imagenes()
    objetos_detectados = computervision_client.detect_objects_in_stream(imagen)

    # Print detected objects results with bounding boxes
    print("Detecting objects in remote image:")
    image = Image.open('images/living2.jpg')
    dibujar = ImageDraw.Draw(image)
    if len(objetos_detectados.objects) == 0:
        print("No objects detected.")
    else:
        for objecto in objetos_detectados.objects:
            dibujar.rectangle((
            objecto.rectangle.x, objecto.rectangle.y,
            objecto.rectangle.x + objecto.rectangle.w, objecto.rectangle.x + objecto.rectangle.h), outline='red')
            fuente = ImageFont.truetype('Roboto-Regular.ttf', 15)
            dibujar.text((objecto.rectangle.x, objecto.rectangle.y -20, objecto.rectangle.x + objecto.rectangle.w,objecto.rectangle.y+objecto.rectangle.h),objecto.object_property, font = fuente, fill="white")
        dibujar.text((10,0,0,0),descripcion,font = fuente, fill="Black")
    image.show()


#describir_imagenes()  
categorias_imagenes()