import ImageOps
import ImageEnhance
import ImageDraw

import Image
import ImageFont

import textwrap

import base64

import re

import urllib2
import urllib


import json

def get_challenge():
    data = { "api_token":"revolutionize B2B infrastructures" }
    req = urllib2.Request("http://canvas.hackkrk.com/api/new_challenge")
    req.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(req, json.dumps(data))
    resp_data = resp.read()
    challenge_data = json.loads(resp_data)
    return challenge_data

def process_challenge(challenge_data):
    b64png = paint_image(challenge_data['color'][0], challenge_data['color'][1], challenge_data['color'][2], challenge_data['answer_width'])
    data = { "api_token":"revolutionize B2B infrastructures", "image": b64png }
    req = urllib2.Request("http://canvas.hackkrk.com/api/challenge/" + str(challenge_data['id']))
    req.add_header('Content-Type', 'application/json')
    resp = urllib2.urlopen(req, json.dumps(data))
    resp_data = resp.read()
    challenge_answer= json.loads(resp_data)
    print challenge_answer['accepted']

def get_averages(image):
  """
  Given PIL Image, return average value of color as (r, g, b)
  """
  # no. of pixels in image
  npixels = image.size[0]*image.size[1]
  # get colors as [(cnt1, (r1, g1, b1)), ...]
  cols = image.getcolors(npixels)
  # get [(c1*r1, c1*g1, c1*g2),...]
  sumRGB = [(x[0]*x[1][0], x[0]*x[1][1], x[0]*x[1][2]) for x in cols] 
  # calculate (sum(ci*ri)/np, sum(ci*gi)/np, sum(ci*bi)/np)
  # the zip gives us [(c1*r1, c2*r2, ..), (c1*g1, c1*g2,...)...]
  avg = tuple([sum(x)/npixels for x in zip(*sumRGB)])
  return avg


def paint_image(r, g, b, img_size):
    """
    """
    pos, prime = get_number(r, g, b)
    bgcolor, fgcolor = (255, 255, 255), (0, 0, 0)
    img = create_image(bgcolor, fgcolor, pos, prime, img_size)
    bgcolor, fgcolor = get_new_colors(img, r, g, b)
    img = create_image(bgcolor, fgcolor, pos, prime, img_size)
    b64 = get_png_base64(img)
#    print (r, g, b)
#    print get_averages(img)
    return b64

def create_image(bgcolor, fgcolor, pos, prime, img_size):
    img = Image.new("RGB", (img_size, img_size), bgcolor)
    img = put_prime_number(img, pos, prime, fgcolor)
    return img

def get_new_colors(img, r, g, b):
    """
    Returns a tuple, with new RGB triplets for both text and background
    """
    colors = img.getcolors()
    n_bg = colors[0][0]
    n_fg = colors[1][0]
    r_bg, r_fg = get_color(r, n_bg, n_fg)
    g_bg, g_fg = get_color(g, n_bg, n_fg)
    b_bg, b_fg = get_color(b, n_bg, n_fg)
    return (r_bg, g_bg, b_bg), (r_fg, g_fg, b_fg)


def get_color(desired, n_bg, n_fg):
    for final_bg in xrange(255, 15, -1):
        final_fg = (desired * (n_bg + n_fg) - n_bg * final_bg) / (n_fg)
        if is_acceptable(final_bg, final_fg):
            break
    else:
        for final_fg in xrange(0, 240):
            final_bg = (desired * (n_bg + n_fg) - n_fg * final_fg) / (n_bg)
            if is_acceptable(final_bg, final_fg):
                break
    return final_bg, final_fg


def is_acceptable(bgcolor, fgcolor):
    if fgcolor > 255 or fgcolor < 0:
        return False
    if bgcolor > 255 or bgcolor < 0:
        return False
    if abs(fgcolor - bgcolor) < 15:
        return False
    return True

# threshold: 30


def get_png_base64(img):
    """
    """
    img.save("response.png")
    img_content = open("response.png", "rb").read()
    return base64.b64encode(img_content)

def get_prime(n):
    """
    TODO!
    """
    data = urllib.urlencode([("n", n)])
    req = urllib2.Request("http://primes.utm.edu/nthprime/index.php", data)
    f = urllib2.urlopen(req)
    html = f.read()
    num_str = re.findall('prime is ([0-9,]+)', html)[1]
    return int(num_str.replace(',', ''))

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

def put_prime_number(img, n, p, textcolor):
    """
    @return image with a number printed on it. Useful for debugging purposes.
    @param n: number to write on the image
    """
    #fnt = ImageFont.truetype(r"C:\Windows\Fonts\munro_small.ttf", 12)
    img = img.copy()
    draw = ImageDraw.Draw(img)
    for y, line in enumerate(get_prime_number_text(n, p)):
        w, h = draw.textsize(line)
        draw.text(((img.size[0]-w)/2, y*10+7), line, fill=textcolor)
    return img

for i in xrange(1000):
    print i,
    data = get_challenge()
    process_challenge(data)

####################################################

def desaturate(img):
    """
    @return a copy of the image, lighter and desaturated useful for background.
    """
    bw_img = ImageOps.grayscale(img)
    enhancer = ImageEnhance.Brightness(bw_img)
    bw_img_light = enhancer.enhance(0.50)
    bw_img_light = bw_img_light.convert('RGB')
    return bw_img_light

