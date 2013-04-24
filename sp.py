import ImageOps
import ImageEnhance
import ImageDraw
import Image

def paint_image(r, g, b, img_size):
    """
    """
    img = Image.new("RGB", (img_size, img_size), (0, 0, 0))
    img.save("response.png")




def desaturate(img):
    """
    @return a copy of the image, lighter and desaturated useful for background.
    """
    bw_img = ImageOps.grayscale(img)
    enhancer = ImageEnhance.Brightness(bw_img)
    bw_img_light = enhancer.enhance(0.50)
    bw_img_light = bw_img_light.convert('RGB')
    return bw_img_light

def putnumber(img, n):
    """
    @return image with a number printed on it. Useful for debugging purposes.
    @param n: number to write on the image
    """
    img = img.copy()
    draw = ImageDraw.Draw(img)
    draw.text((10, 10), str(n), fill='fuchsia')
    return img

paint_image(128, 128, 128, 64)