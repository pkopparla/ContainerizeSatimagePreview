# import boto3
from src import process
import json


def getkey(messagetext, band):
    objectpath = messagetext["Records"][0]["s3"]["object"]["key"]
    frags = objectpath.split("/")
    suffix = "_" + band + ".TIF"
    filename = frags[-2] + suffix
    filepath = "/".join(frags[:-1])
    filepath = filepath + "/" + filename
    return filepath


def getbucketname(messagetext):
    bucketname = messagetext["Records"][0]["s3"]["bucket"]["name"]
    return bucketname


def lambda_handler(event, context):
    # rgbbands = ['B4','B3','B2'] #red,green,blue
    # filelist = []
    # for band in rgbbands:
    #     key = getkey(event,band)
    #     resourceloc = '/vsicurl/https://landsat-pds.s3.amazonaws.com/'+key
    #     filelist.append(resourceloc)
    # print(filelist)
    filelist = [
        "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B4.TIF",
        "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B3.TIF",
        "download/LC08_L2SP_044034_20201129_20201211_02_T1_SR_B2.TIF",
    ]
    process.getpreview(filelist)
    return True


# if __name__=="__main__":
#    lambda_handler('a','b')
