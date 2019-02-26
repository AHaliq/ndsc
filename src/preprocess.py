import googleutil as G
from PIL import Image
import requests
from io import BytesIO

def getimg(csvcol,imsize=128):
    response = requests.get(G.img + csvcol)
    img = Image.open(BytesIO(response.content))
    size = imsize, imsize
    img.thumbnail(size, Image.ANTIALIAS)
    return img