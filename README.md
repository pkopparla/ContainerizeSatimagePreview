### Simple Image Preview Thumbnail with Dockerization

This is a small program that uses GDAL functions to create JPEG preview of a Landsat-8 scene. A test scene is provided in the `download` directory.

To create the Docker image, do

```docker build -t satimage_preview .```

To run tests do

```docker run -it -v $(pwd):/workspace landsat_preview pytest```

To run the code do

```docker run -it -v $(pwd):/workspace landsat_preview python src/process.py```