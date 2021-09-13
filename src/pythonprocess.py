from glob import glob
import subprocess
import os
from PIL import Image
import numpy as np
from osgeo import gdal


def getminmax(tiffile):
    """function to min and max values of the raster using gdalinfo"""
    info = gdal.Info(tiffile).split("\n")
    for strings in info:
        if strings.find("STATISTICS_MINIMUM") >= 0:
            min = strings.split("=")[-1]
        if strings.find("STATISTICS_MAXIMUM") >= 0:
            max = strings.split("=")[-1]
    return [min, max]  # note that the list elements are strings


def scaleandfill(tiffiles):
    """function to fill no data and scale values from 0 to 255"""
    outfilelist = []
    for tiffile in tiffiles:
        scaledfilename = "scaled" + tiffile[-6:]
        min, max = getminmax(tiffile)
        gdal.Translate(
            scaledfilename,
            tiffile,
            width=959,
            height=976,
            outputType=gdal.gdalconst.GDT_Byte,
            resampleAlg="cubic",
            scaleParams=[[min, max, 0, 255]],
        )
        outfilelist.append(scaledfilename)
    return outfilelist


def getstretchlimits(tiffile):
    """get the color stretch limits based on a histogram"""
    with Image.open(tiffile) as im:
        imarray = np.array(im)
        imarray = imarray[imarray > 10]  # get rid of the values near zero
        return [np.percentile(imarray, 1), np.percentile(imarray, 99)]


def getpreview(dir="download"):
    """Create a quick JPEG preview for a sample Landsat input"""
    bandfiles = glob(os.path.join(dir, "*B[2-4].TIF"))
    if not bandfiles:
        raise FileNotFoundError("No valid files were found in download directory")

    bandfiles.sort(reverse=False)
    (
        blue,
        green,
        red,
    ) = scaleandfill(bandfiles)
    # unpack the bands in to the three colors red, blue and green
    stackcommand = "gdal_merge.py -o rgb.tif -ot Byte -separate -co \
    PHOTOMETRIC=RGB -co COMPRESS=DEFLATE {red} {green} {blue}"

    subprocess.call(
        stackcommand.format(red=red, green=green, blue=blue)
    )  # this creates a stacked file 'rgb.tif'
    stretchmin, stretchmax = getstretchlimits("rgb.tif")
    tcicommand = "gdal_translate -scale {stretchmin} {stretchmax} 0 255 \
    -exponent 1 -ot Byte -of JPEG rgb.tif tci.jpg"
    subprocess.call(
        tcicommand.format(stretchmin=stretchmin, stretchmax=stretchmax)
    )  # this color stretches the image and writes to jpeg
    cleanupcommand = "rm *tif *TIF *xml"
    subprocess.call(cleanupcommand)
    return True


if __name__ == "__main__":
    getpreview()