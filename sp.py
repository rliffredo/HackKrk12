import ImageOps
import ImageEnhance
import ImageDraw

import Image
import ImageFont

import textwrap

def paint_image(r, g, b, img_size):
    """
    """
    img = Image.new("RGB", (img_size, img_size), (255, 255, 255))
    pos, prime = get_number(r, g, b)
    img = put_prime_number(img, pos, prime)
    img.save("response.png")

def get_prime(n):
    """
    TODO!
    """
    return 42

def get_number(r, g, b):
    """
    """
    pos = (r*g*b) + 1
    prime = get_prime(pos)
    return pos, prime

def get_suffix(n):
    last_letter = str(n)[-1:]
    if (last_letter == '1'):
        return 'st'
    if (last_letter == '2'):
        return 'nd'
    if (last_letter == '3'):
        return 'rd'
    return 'th'

def get_prime_number_text(n, p):
    """
    """
    txt = "The %i%s prime number is\n%i" % (n, get_suffix(n), p)
    return textwrap.wrap(txt, 10)

def put_prime_number(img, n, p):
    """
    @return image with a number printed on it. Useful for debugging purposes.
    @param n: number to write on the image
    """
    #fnt = ImageFont.truetype(r"C:\Windows\Fonts\munro_small.ttf", 12)
    img = img.copy()
    draw = ImageDraw.Draw(img)
    for y, line in enumerate(get_prime_number_text(n, p)):
        w, h = draw.textsize(line)
        draw.text(((img.size[0]-w)/2, y*10+7), line, fill='black')
    return img

paint_image(255, 255, 255, 64)


def desaturate(img):
    """
    @return a copy of the image, lighter and desaturated useful for background.
    """
    bw_img = ImageOps.grayscale(img)
    enhancer = ImageEnhance.Brightness(bw_img)
    bw_img_light = enhancer.enhance(0.50)
    bw_img_light = bw_img_light.convert('RGB')
    return bw_img_light

