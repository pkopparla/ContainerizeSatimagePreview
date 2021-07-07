### Simple Image Preview Thumbnail with Dockerization

This is a small program that uses GDAL functions to create JPEG preview of a Landsat-8 scene. A test scene is provided in the `download` directory. It is containerized using a base OSGEO/GDAL image.

To create the Docker image, do

```docker build -t satimage_preview .```

To run tests do

```docker run -it -v $(pwd):/workspace landsat_preview pytest```

To run the code do

```docker run -it -v $(pwd):/workspace landsat_preview python src/process.py```

A lot of the structure of this code is based on this [repo](https://github.com/eoameen/landsat8_fetch_scene)