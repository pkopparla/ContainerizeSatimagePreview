## Simple Image Preview Thumbnail with Dockerization

This is a small program that uses GDAL functions to create JPEG preview of a Landsat-8 scene. A test scene is provided in the `newmessage.json` file. It is containerized using a base OSGEO/GDAL image.

To create the Docker image, do

`docker build -t landsat_preview .`

To run tests do

`docker run -it -v $(pwd):/workspace landsat_preview pytest`

To run the code do

`docker run -it -v $(pwd):/workspace landsat_preview python src/process.py`

To run the pre-commit linting do

`pre-commit run`

after adding files to be committed. It does some whitespaces checks and black standard linting.

## Using this pipeline with AWS Lambda

You can package up the Docker image for use as a Lambda function using `sam`. Make sure you have AWS credentials located at `~/.aws`.
The AWS Lambda interface client is included in the requirements as `awslambdaric` and the entrypoint for the Lambda function is defined in the both the `template.yaml` and `Dockerfile` using the script `src/entry_script.sh`. See here
for references on creating Lambda functions from custom Docker images: [Tutorial](https://docs.aws.amazon.com/lambda/latest/dg/images-create.html#images-create-from-alt).

A minimal example is now working with `sam`

Try `sam build` followed by `sam local invoke -e newmessage.json`
This simulates a landsat bucket event for a new scene, which triggers the pipeline and uploads
to the preview image an S3 bucket named `testpushkarbucket` tagged with current time. Because this is not a public
access bucket you will need to change this to your own bucket.

To hook it up to the official Landsat bucket, you will need to set the Lambda trigger to an SNS topic with the ARN `arn:aws:sns:us-west-2:673253540267:public-c2-notify`.
More notes on that are [here](https://www.usgs.gov/core-science-systems/nli/landsat/landsat-commercial-cloud-data-access?qt-science_support_page_related_con=1#qt-science_support_page_related_con).

TBD:

---

- Tried uploading image to ECR and creating a Lambda function with it. GDAL CLI commands throw errors, even
  though they work fine with `sam local invoke`. Needs debugging, maybe refactor to GDAL python bindings?
- Figure out how to securely pass AWS credentials (needed to access requester pays bucket + preview jpeg upload to s3) without passing secret keys in plaintext.

Acknowledgements: Thanks to Dr. Ameen Najjar for the idea to try this.
