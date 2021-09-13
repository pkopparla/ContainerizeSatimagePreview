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

Acknowledgements: Thanks to Ameen Najjar for the idea to try this. I looked to this [repo] as a reference (https://github.com/eoameen/landsat8_fetch_scene)
