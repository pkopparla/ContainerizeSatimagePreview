from glob import glob
import os

stackcommand = "gdal_merge.py -o rgb.tif -separate -co PHOTOMETRIC=RGB -co COMPRESS=DEFLATE {red} {green} {blue}"
tcicommand = "gdal_translate -scale 0 18000 -exponent 0.5 -ot Byte -of JPEG -outsize 10% 10% rgb.tif tci.jpg"
cleanupcommand = "rm rgb.tif"


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
    ) = bandfiles  # unpack the bands in to the three colors red, blue and green oninllnaegag
    os.system(stackcommand.format(red=red, green=green, blue=blue))
    os.system(tcicommand)
    os.system(cleanupcommand)
    return True


if __name__ == "__main__":
    getpreview()
