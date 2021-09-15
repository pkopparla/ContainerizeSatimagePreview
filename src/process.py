from glob import glob
import subprocess
import os
from PIL import Image
import numpy as np
from osgeo import gdal
import boto3

s3 = boto3.client("s3")


def getminmax(tiffile):
    """function to min and max values of the raster using gdalinfo"""
    """this is too expensive for remote files, replaced by naive values"""
    """f = (
        subprocess.check_output("gdalinfo -stats {0}".format(tiffile), shell=True)
        .decode("utf-8")
        .split("\n")
    )
    for strings in f:
        if strings.find("STATISTICS_MINIMUM") >= 0:
            min = strings.split("=")[-1]
        if strings.find("STATISTICS_MAXIMUM") >= 0:
            max = strings.split("=")[-1] """
    return [0, 65535]  # [min, max]  # note that the list elements are strings


def scaleandfill(tiffiles):
    """function to fill no data and scale values from 0 to 255"""
    bandstrings = ["B4.TIF", "B3.TIF", "B2.TIF"]
    outfilelist = []
    for count, tiffile in enumerate(tiffiles):
        # nodatafilename = "nodata" + tiffile[-6:]
        scaledfilename = "scaled" + bandstrings[count]

        # nodatacommand = "gdal_fillnodata.py {infile} {outfile}"
        # os.system(nodatacommand.format(infile=tiffile, outfile=nodatafilename))
        min, max = getminmax(tiffile)  # getminmax(nodatafilename)
        scalingcommand = "GDAL_DISABLE_READDIR_ON_OPEN=YES CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.tif gdal_translate -ot Byte -scale {min} {max} 0 255 -outsize 959 976 -r cubic {infile} {outfile}"
        subprocess.call(
            scalingcommand.format(
                min=min, max=max, infile=tiffile, outfile=scaledfilename
            ),
            shell=True,
        )
        outfilelist.append(scaledfilename)
    return outfilelist


def getstretchlimits(tiffile):
    """get the color stretch limits based on a histogram"""
    with Image.open(tiffile) as im:
        imarray = np.array(im)
        imarray = imarray[imarray > 10]  # get rid of the values near zero
        return [np.percentile(imarray, 1), np.percentile(imarray, 99)]


def getpreview(bandfiles):
    """Create a quick JPEG preview for a sample Landsat input"""
    blue, green, red = scaleandfill(bandfiles)
    # unpack the bands in to the three colors red, blue and green
    stackcommand = "gdal_merge.py -o rgb.tif -ot Byte -separate -co \
    PHOTOMETRIC=RGB -co COMPRESS=DEFLATE {red} {green} {blue}"

    subprocess.call(
        stackcommand.format(red=red, green=green, blue=blue), shell=True
    )  # this creates a stacked file 'rgb.tif'
    stretchmin, stretchmax = getstretchlimits("rgb.tif")
    tcicommand = "gdal_translate -scale {stretchmin} {stretchmax} 0 255 \
    -exponent 1 -ot Byte -of JPEG rgb.tif tci.jpg"
    subprocess.call(
        tcicommand.format(stretchmin=stretchmin, stretchmax=stretchmax), shell=True
    )  # this color stretches the image and writes to jpeg
    cleanupcommand = "rm *tif *TIF *xml"
    subprocess.call(cleanupcommand, shell=True)
    s3.upload_file("tci.jpg", "testpushkarbucket", "tcilatest.jpg")
    return True


filelist = [
    "/vsicurl/https://landsat-pds.s3.amazonaws.com/c1/L8/170/059/LC08_L1TP_170059_20210527_20210527_01_RT/LC08_L1TP_170059_20210527_20210527_01_RT_B4.TIF",
    "/vsicurl/https://landsat-pds.s3.amazonaws.com/c1/L8/170/059/LC08_L1TP_170059_20210527_20210527_01_RT/LC08_L1TP_170059_20210527_20210527_01_RT_B3.TIF",
    "/vsicurl/https://landsat-pds.s3.amazonaws.com/c1/L8/170/059/LC08_L1TP_170059_20210527_20210527_01_RT/LC08_L1TP_170059_20210527_20210527_01_RT_B2.TIF",
]

localfilelist = [
    "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B2.TIF",
    "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B3.TIF",
    "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B4.TIF",
]
if __name__ == "__main__":
    getpreview(filelist)
