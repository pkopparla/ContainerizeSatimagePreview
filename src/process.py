import subprocess
import numpy as np
import boto3
import time
from osgeo import gdal

'''
def getminmax(tiffile):
    """function to find min and max values of the raster using gdalinfo"""
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
'''


def scaleandfill(tiffiles):
    """function to fill no data and scale values from 0 to 255"""
    bandstrings = ["B4.TIF", "B3.TIF", "B2.TIF"]
    outfilelist = []
    for count, tiffile in enumerate(tiffiles):
        scaledfilename = "scaled" + bandstrings[count]
        scalingcommand = "CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.tif gdal_translate \
        -outsize 959 976 -r cubic {infile} {outfile} --config \
        AWS_REQUEST_PAYER requester"
        subprocess.call(
            scalingcommand.format(infile=tiffile, outfile=scaledfilename),
            shell=True,
        )
        outfilelist.append(scaledfilename)
    return outfilelist


def getstretchlimits(tiffile):
    """get the color stretch limits based on a histogram"""
    im = gdal.Open(tiffile)
    imarray = np.dstack(
        [
            im.GetRasterBand(1).ReadAsArray(),
            im.GetRasterBand(2).ReadAsArray(),
            im.GetRasterBand(3).ReadAsArray(),
        ]
    )

    # imarray = imarray[imarray > 10]  # get rid of the values near zero
    # return (imarray.dtype, imarray.shape)
    return [np.percentile(imarray, 1), np.percentile(imarray, 99)]


def getpreview(bandfiles):
    """Create a quick JPEG preview for a sample Landsat input"""
    blue, green, red = scaleandfill(bandfiles)
    # unpack the bands in to the three colors red, blue and green
    stackcommand = "gdal_merge.py -o rgb.tif -separate -co \
    PHOTOMETRIC=RGB -co COMPRESS=DEFLATE {red} {green} {blue} \
    --config AWS_REQUEST_PAYER requester"

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
    timestring = time.strftime("%H_%M_%S", time.localtime())
    s3filename = "tcilatest" + timestring + ".jpg"
    s3 = boto3.client("s3")
    s3.upload_file("tci.jpg", "testpushkarbucket", s3filename)
    return s3filename
