import matplotlib.pyplot as plt
from osgeo import gdal

""" dataset = gdal.Open("rgb.TIF", gdal.GA_ReadOnly)
band = dataset.GetRasterBand(1)
array = band.ReadAsArray()

plt.hist(array.flatten(),bins=50)
plt.savefig('histrgb1.png') """

from PIL import Image
import numpy as np

im = Image.open("rgb.tif")
imarray = np.array(im)
imarray = imarray[imarray > 10]
print(np.percentile(imarray, 1), np.percentile(imarray, 99))
# ff = plt.hist(imarray.flatten(),bins=50)
# plt.savefig('histrgb.png')
