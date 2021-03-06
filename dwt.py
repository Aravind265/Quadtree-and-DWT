# pylint: disable=C0103,E0401,W0631
'Compression methods'
import pywt
import numpy
from PIL import Image
import quadtree as quad
# import utils as util


def extract_rgb_coeff(img):
    """
    Returns RGB dwt applied coefficients tuple
    Parameters
    ----------
    img: PIL Image
    Returns
    -------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    """
    (width, height) = img.size
    img = img.copy()

    mat_r = numpy.empty((width, height))
    mat_g = numpy.empty((width, height))
    mat_b = numpy.empty((width, height))

    for i in range(width):
        for j in range(height):
            (r, g, b) = img.getpixel((i, j))
            mat_r[i, j] = r
            mat_g[i, j] = g
            mat_b[i, j] = b

    coeffs_r = pywt.dwt2(mat_r, 'haar')
   
    coeffs_g = pywt.dwt2(mat_g, 'haar')
    
    coeffs_b = pywt.dwt2(mat_b, 'haar')
    
    return (coeffs_r, coeffs_g, coeffs_b)


def img_from_dwt_coeff(coeff_dwt):
    """
    Returns Image recreated from dwt coefficients
    Parameters
    ----------
    (coeffs_r, coeffs_g, coeffs_b):
        RGB coefficients with Discrete Wavelet Transform Applied
    Returns
    -------
    Image from dwt coefficients
    """
    # Channel Red
    (coeffs_r, coeffs_g, coeffs_b) = coeff_dwt

    cc = numpy.array((coeffs_r, coeffs_g, coeffs_b))

    (width, height) = (len(coeffs_r[0]), len(coeffs_r[0][0]))

    cARed = numpy.array(coeffs_r[0])
    cHRed = numpy.array(coeffs_r[1][0])
    cVRed = numpy.array(coeffs_r[1][1])
    cDRed = numpy.array(coeffs_r[1][2])
    # Channel Green
    cAGreen = numpy.array(coeffs_g[0])
    cHGreen = numpy.array(coeffs_g[1][0])
    cVGreen = numpy.array(coeffs_g[1][1])
    cDGreen = numpy.array(coeffs_g[1][2])
    # Channel Blue
    cABlue = numpy.array(coeffs_b[0])
    cHBlue = numpy.array(coeffs_b[1][0])
    cVBlue = numpy.array(coeffs_b[1][1])
    cDBlue = numpy.array(coeffs_b[1][2])

    dwt_array = []
    for i in range(len(cABlue)):
        temp = []
        temp.append(cARed[i])
        temp.append(cAGreen[i])
        temp.append(cABlue[i])
        dwt_array.append(temp)

    return dwt_array

    # maxValue per channel par matrix
    cAMaxRed = numpy.max(cARed)
    cAMaxGreen = numpy.max(cAGreen)
    cAMaxBlue = numpy.max(cABlue)

    cHMaxRed = numpy.max(cHRed)
    cHMaxGreen = numpy.max(cHGreen)
    cHMaxBlue = numpy.max(cHBlue)

    cVMaxRed = numpy.max(cVRed)
    cVMaxGreen = numpy.max(cVGreen)
    cVMaxBlue = numpy.max(cVBlue)

    cDMaxRed = numpy.max(cDRed)
    cDMaxGreen = numpy.max(cDGreen)
    cDMaxBlue = numpy.max(cDBlue)

    # Image object init
    dwt_img = Image.new('RGB', (width, height), (0, 0, 20))
    # cA reconstruction

    '''
    The image formed from the low frequnecy of the images which contains the main content of the image
    '''
    for i in range(width):
        for j in range(height):
            R = cARed[i][j]
            R = (R/cAMaxRed)*100.0
            G = cAGreen[i][j]
            G = (G/cAMaxGreen)*100.0
            B = cABlue[i][j]
            B = (B/cAMaxBlue)*100.0
            new_value = (int(R), int(G), int(B))
            dwt_img.putpixel((i, j), new_value)
   
    return dwt_img

if __name__ == '__main__':
    img = Image.open('dog.jpg')
    coeff = extract_rgb_coeff(img)
    image = img_from_dwt_coeff(coeff)
    image = numpy.array(image)
    # image.save('dwt.jpg')
    quad.quadtreeSegmentation(image, limit=8, stdLimit=7.0)