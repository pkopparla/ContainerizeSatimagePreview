# import boto3
from src import process
import json


def makefilelist(inpstring):
    """function to get RGB bands file locations given an S3 scene location"""
    frags = list(filter(len, inpstring.split("/")))
    frags[0] = "/vsis3"
    outfilelist = []
    for band in ["B4", "B3", "B2"]:
        copy = list(frags)
        copy.append(frags[-1] + "_" + band + ".TIF")
        outfilelist.append("/".join(copy))
    return outfilelist


def lambda_handler(event, context):

    jsontext = json.loads(event["Records"][0]["Sns"]["Message"])
    bandfiles = makefilelist(jsontext["s3_location"])
    return bandfiles


# if __name__=="__main__":
#    lambda_handler('a','b')
