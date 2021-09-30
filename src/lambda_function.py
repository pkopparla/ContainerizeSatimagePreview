import json

# terrible trouble with imports, what works locally doesn't work on Docker
try:
    import src.process as process
except ImportError:
    import process


def makefilelist(inpstring):
    """function to get RGB bands file locations given an S3 scene location"""
    frags = list(filter(len, inpstring.split("/")))
    frags[0] = "/vsis3"
    outfilelist = []
    for band in ["SR_B4", "SR_B3", "SR_B2"]:
        copy = list(frags)
        copy.append(frags[-1] + "_" + band + ".TIF")
        outfilelist.append("/".join(copy))
    return outfilelist


def lambda_handler(event, context):
    jsontext = json.loads(event["Records"][0]["Sns"]["Message"])
    bandfiles = makefilelist(jsontext["s3_location"])
    outfilename = process.getpreview(bandfiles)
    return outfilename


if __name__ == "__main__":
    print(lambda_handler(json.loads(open("newmessage.json", "r").read()), None))
