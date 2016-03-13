KrISS zoom
==========
A simple and smart (or stupid) pan and zoom video blender script

Images
------
<a href="https://en.wikipedia.org/wiki/Lenna#/media/File:Lenna.png"><img src="https://github.com/tontof/kriss_zoom/raw/master/lenna.png" width="124" height="124"></a>
<a href="https://commons.wikimedia.org/wiki/Panorama_of_Paris#/media/File:Front_de_Seine_as_seen_from_Pont_Mirabeau_140412_1.jpg"><img src="https://github.com/tontof/kriss_zoom/raw/master/paris.jpg" width="240" height="96"></a>

Presentation
------------

```
blender -b -P kriss_zoom.py -- --help
```

```
positional arguments:
  input                 Path to picture

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output file (default: /tmp/)
  -r RESOLUTION, --resolution RESOLUTION
                        Output resolution width x height (default: 640x360)
  --fps FPS             Frame per second (default: 25)
  -t TIME, --time TIME  Duration of the video in second (default: 5)
  -i INTERPOLATION, --interpolation INTERPOLATION
                        Interpolation mode for animation (default: LINEAR)
  -ff FILE_FORMAT, --file-format FILE_FORMAT
                        Blender file format (default: FFMPEG)
  -f FORMAT, --format FORMAT
                        Blender format (default: MPEG4)
  -c CODEC, --codec CODEC
                        Blender codec (default: MPEG4)
  -flx FROM_LOCATION_X, --from-location-x FROM_LOCATION_X
                        Initial x position: left, center, right or [percent]
                        (default: center)
  -fly FROM_LOCATION_Y, --from-location-y FROM_LOCATION_Y
                        Initial y position: top, center, bottom or [percent]
                        (default: center)
  -flz FROM_LOCATION_Z, --from-location-z FROM_LOCATION_Z
                        Initial z position: [percent] (default: 50)
  -tlx TO_LOCATION_X, --to-location-x TO_LOCATION_X
                        Final x position: left, center, right or [percent]
                        (default: center)
  -tly TO_LOCATION_Y, --to-location-y TO_LOCATION_Y
                        Final y position: top, center, bottom or [percent]
                        (default: center)
  -tlz TO_LOCATION_Z, --to-location-z TO_LOCATION_Z
                        Final z position: [percent] (default: 100)
  --no-render           Usefull when using blender without -b option (default:
                        True)
```

Options
-------
```
-ff FILE_FORMAT, --file-format FILE_FORMAT
```
BMP, IRIS, PNG, JPEG, JPEG2000, TARGA, TARGA_RAW, CINEON, DPX, OPEN_EXR_MULTILAYER, OPEN_EXR, HDR, TIFF, AVI_JPEG, AVI_RAW, FRAMESERVER, H264, FFMPEG, THEORA

```
-f FORMAT, --format FORMAT
```
MPEG1, MPEG2, MPEG4, AVI, QUICKTIME, DV, H264, XVID, OGG, MKV, FLASH

```
-c CODEC, --codec CODEC
```
NONE, MPEG1, MPEG2, MPEG4, HUFFYUV, DV, H264, THEORA, FLASH, FFV1, QTRLE, DNXHD, PNG

```
-i INTERPOLATION, --interpolation INTERPOLATION
```
CONSTANT, LINEAR, BEZIER, SINE, QUAD, CUBIC, QUART, QUINT, EXPO, CIRC, BACK, BOUNCE, ELASTIC


Examples
--------
* Lenna example with default parameters
```
blender -b -P kriss_zoom.py -- lenna.png
vlc /tmp/0001-0125.mp4
```
* Gif preview for Lenna
```
blender -b -P kriss_zoom.py -- lenna.png -t 2 -ff PNG
convert /tmp/{01..50}.png -resize 150x100 lenna.gif
```
<img src="https://github.com/tontof/kriss_zoom/raw/master/lenna.gif">
* Paris example with pan and zoom :
```
blender -b -P kriss_zoom.py -- paris.jpg -flz 75 -tlz 50 -flx right -tlx left -r 320x180 -f OGG -ff THEORA -o paris.ogv
```
<img src="https://github.com/tontof/kriss_zoom/raw/master/paris.gif">
