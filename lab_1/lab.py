# The code below seems to have some problems.
# Fix it before implementing the rest of your lab

def width(image):
    return image["width"]

def height(image):
    return image["height"]

# returns pixel at the (x,y) coordinate
def pixel(image, x, y):
    index = x + width(image)*y
    return image["pixels"][index]

# sets pixel to new color
def set_pixel(image, x, y, color):
    index = x + width(image)*y
    image["pixels"][index] = color

# makes new dark image
def make_image(width, height):
    return {"width": width, "height": height, "pixels": ([0]*width*height)}

# return a new image by applying function f to each pixel of the input image
def apply_per_pixel(image, f):
    # switched width and height
    result = make_image(width(image), height(image))
    for x in range(width(result)):
        for y in range(height(result)):
            color = pixel(image, x, y)
            # moved set_pixel to the innermost for loop 
            # switched x and y
            set_pixel(result, x, y, f(color))
    return result

# inverts colors  
def invert(c):
    # changed 256 to 255 - 255 is the brightest color possible
    return abs(255-c)

# takes square root of the sum of 2 pixels
def sqrtsum(c1, c2):
    return int(round((c1**2 + c2**2)**0.5))

# gets pixel, or returns default if outside image
def get_pixel(image, x, y, default=0):
    if 0 <= x < width(image) and 0 <= y < height(image):
        return pixel(image, x, y)
    else:
        return default
    
# new image from kernel, not forced to [0, 255]
def convolve2d(image, k):
    convolved = make_image(width(image), height(image))
    for x in range(width(convolved)):
        for y in range(height(convolved)):
            set_pixel(convolved, x, y, get_pixel(image, x-1, y-1)*k[0] 
            + get_pixel(image, x, y-1)*k[1] + get_pixel(image, x+1,y-1)*k[2] + get_pixel(image, x-1, y)*k[3] + get_pixel(image, x, y)*k[4] 
            + get_pixel(image, x+1, y)*k[5] + get_pixel(image, x-1, y+1)*k[6] + get_pixel(image, x, y+1)*k[7] + get_pixel(image, x+1, y+1)*k[8])
    return convolved
    
 # new image, combined according to f(pixel1, pixel2)
def combine_images(image1, image2, f):
    combined = make_image(width(image1), height(image1))
    for x in range(width(image1)):
        for y in range(height(image1)):
            set_pixel(combined, x, y, f(get_pixel(image1, x, y), get_pixel(image2, x, y)))
    return combined
    
# forces each pixel into [0, 255] and ints, returns updated image    
def legalize_range(image):
    for x in range(width(image)):
        for y in range(height(image)):
            set_pixel(image, x, y, int(pixel(image, x, y)))
            if pixel(image, x, y) < 0: 
                set_pixel(image, x, y, 0)
            if pixel(image, x, y) > 255: 
                set_pixel(image, x, y, 255)
    return image

# inverts image
def filter_invert(image):
    return apply_per_pixel(image, invert)

# blurs image
def filter_gaussian_blur(image):
    kernel3x3 = [1.0/16, 2.0/16, 1.0/16, 2.0/16, 4.0/16, 2.0/16, 1.0/16, 2.0/16, 1.0/16]
    convolved = convolve2d(image, kernel3x3)
    return legalize_range(convolved)

# output is the square root of the sum of squares of corresponding pixels    
def filter_edge_detect(image):
    k_x = [-1, 0, 1, -2, 0, 2, -1, 0, 1]
    k_y = [-1, -2, -1, 0, 0, 0, 1, 2, 1]
    image1 = convolve2d(image, k_x)
    image2 = convolve2d(image, k_y)
    combined = combine_images(image1, image2, sqrtsum)
    return legalize_range(combined)
    

# any function of the form "filter_X( image ):", where X denotes the name of
# the filter, can be applied via test.py and the web UI!
# Feel free to go wild and implement your favorite filters once you are done.
# Here are some to inspire you: [GIMP filters](https://docs.gimp.org/en/filters.html)
