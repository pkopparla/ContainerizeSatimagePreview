### Simple Image Preview Thumbnail with Dockerization

This is a small program that uses GDAL functions to create JPEG preview of a Landsat-8 scene. A test scene is provided in the `download` directory. It is containerized using a base OSGEO/GDAL image.

To create the Docker image, do

`docker build -t landsat_preview .`

To run tests do

`docker run -it -v $(pwd):/workspace landsat_preview pytest`

To run the code do

`docker run -it -v $(pwd):/workspace landsat_preview python src/process.py`

To run the pre-commit linting do

`pre-commit run`

after adding files to be committed. It does some whitespaces checks and black standard linting.

TBD:

<ol>
<li> Add a few more unit tests for when commands error out
<li>Find an easy way to put this onto a Lambda function which is triggered by new scenes uploaded to the Landsat PDS bucket. Currently, the Docker image is quite huge at 1.6 GB. Some demo code for this already exists in this [repo](https://github.com/pkopparla/LandsatThumnails)
</ol>
Acknowledgements: Thanks to Dr. Ameen Najjar for the idea to try this. I looked to this [repo](https://github.com/eoameen/landsat8_fetch_scene) as a reference.
