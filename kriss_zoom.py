"""
    Convert a picture into a movie adding a zoom effect
    using blender command line
"""

import bpy
import addon_utils
import sys
import argparse
import os

__author__ = "Tontof"
__copyright__ = "2015 - Copyleft - Tontof - http://tontof.net"


def posTextToPercent(text):
    """
        Convert a string position into percent value
    """
    if text == 'center':
        res = 50
    elif text == 'left':
        res = 0
    elif text == 'right':
        res = 100
    elif text == 'top':
        res = 0
    elif text == 'bottom':
        res = 100
    else:
        res = int(text)

    return res


def loadPlugins():
    """
        Load import images as planes plugin
    """
    # Activate import images as planes plugins
    is_default, is_loaded = addon_utils.check("io_import_images_as_planes")
    if not is_loaded:
        addon_utils.enable("io_import_images_as_planes")


def initScene(args):
    """
        Initialize all scene parameters
    """
    # remove Cube object
    for ob in bpy.context.scene.objects:
        ob.select = ob.type == 'MESH' and ob.name.startswith("Cube")

    bpy.ops.object.delete()

    # Initialize scene/camera
    scene = bpy.context.scene
    scene.camera.data.lens = 1
    scene.camera.data.sensor_height = 1
    scene.camera.data.sensor_fit = 'VERTICAL'
    scene.camera.rotation_euler = (0, 0, 0)
    scene.camera.location = (0, 0, 1)
    scene.cursor_location = (0, 0, 0)
    scene.frame_start = 1
    scene.frame_end = args.fps * args.time
    scene.render.image_settings.file_format = args.file_format
    scene.render.ffmpeg.codec = args.codec
    scene.render.ffmpeg.format = args.format
    scene.render.filepath = args.output
    scene.render.fps = args.fps
    scene.render.resolution_x = int(args.resolution.split('x')[0])
    scene.render.resolution_y = int(args.resolution.split('x')[1])
    scene.render.resolution_percentage = 100


def computeScene(args):
    """
        Compute scene using command line arguments
    """
    # import image
    file = os.path.abspath(args.input)
    bpy.ops.import_image.to_plane(
        use_shadeless=True,
        files=[{'name': os.path.basename(file)}],
        directory=os.path.dirname(file)
    )

    bpy.context.object.name = "Image"
    bpy.context.object.data.name = "Image"

    # compute image, render ratio
    scene = bpy.context.scene
    image_dimensions = bpy.context.object.dimensions
    image_ratio = image_dimensions.x / image_dimensions.y
    render_ratio = scene.render.resolution_x/scene.render.resolution_y

    # compute z corresponding to 100 percent
    z100 = 1
    if image_ratio < render_ratio:
        z100 = image_ratio/render_ratio

    # compute from and to location in percent
    from_loc_x = posTextToPercent(args.from_location_x)
    from_loc_y = posTextToPercent(args.from_location_y)
    to_loc_x = posTextToPercent(args.to_location_x)
    to_loc_y = posTextToPercent(args.to_location_y)

    # set first keyframe
    scene.camera.location.z = z100*args.from_location_z/100

    from_x_delta = (image_ratio-render_ratio*scene.camera.location.z)/2
    from_y_delta = -(1-scene.camera.location.z)/2

    scene.camera.location.x = ((from_loc_x-50)/50)*from_x_delta
    scene.camera.location.y = ((from_loc_y-50)/50)*from_y_delta
    scene.camera.keyframe_insert(data_path="location", frame=1)

    # set last keyframe
    scene.camera.location.z = z100*args.to_location_z/100

    to_x_delta = (image_ratio-render_ratio*scene.camera.location.z)/2
    to_y_delta = -(1-scene.camera.location.z)/2

    scene.camera.location.x = ((to_loc_x-50)/50)*to_x_delta
    scene.camera.location.y = ((to_loc_y-50)/50)*to_y_delta
    scene.camera.keyframe_insert(data_path="location", frame=scene.frame_end)

    # set interpolation
    for fcurve in scene.camera.animation_data.action.fcurves:
        for keyframe in fcurve.keyframe_points:
            keyframe.interpolation = args.interpolation


def renderScene():
    """
        Render animation using scene parameters
    """
    scene = bpy.context.scene
    if scene.render.image_settings.file_format == 'PNG':
        scene.render.filepath += len(str(scene.frame_end))*'#'

    bpy.ops.render.render(animation=True, write_still=True)


def main(args):
    """
        Main function
    """
    loadPlugins()
    initScene(args)
    computeScene(args)
    if args.render:
        renderScene()


# Parse command line
class ArgumentParserError(Exception):
    pass


class ThrowingArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        print(message)
        raise ArgumentParserError(message)

parser = ThrowingArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter
)
parser.add_argument(
    'input',
    help="Path to picture")
parser.add_argument(
    '-o', '--output', default='/tmp/',
    help="Output file")
parser.add_argument(
    '-r', '--resolution', default='640x360',
    help="Output resolution width x height")
parser.add_argument(
    '--fps', type=int, default=25,
    help="Frame per second")
parser.add_argument(
    '-t', '--time', type=int, default='5',
    help="Duration of the video in second")
parser.add_argument(
    '-i', '--interpolation', default='LINEAR',
    help="Interpolation mode for animation")
parser.add_argument(
    '-ff', '--file-format', default='FFMPEG',
    help="Blender file format")
parser.add_argument(
    '-f', '--format', default='MPEG4',
    help="Blender format")
parser.add_argument(
    '-c', '--codec', default='MPEG4',
    help="Blender codec")
parser.add_argument(
    '-flx', '--from-location-x', default='center',
    help="Initial x position: left, center, right or [percent]")
parser.add_argument(
    '-fly', '--from-location-y', default='center',
    help="Initial y position: top, center, bottom or [percent]")
parser.add_argument(
    '-flz', '--from-location-z', type=int, default='50',
    help="Initial z position: [percent]")
parser.add_argument(
    '-tlx', '--to-location-x', default='center',
    help="Final x position: left, center, right or [percent]")
parser.add_argument(
    '-tly', '--to-location-y', default='center',
    help="Final y position: top, center, bottom or [percent]")
parser.add_argument(
    '-tlz', '--to-location-z', type=int, default='100',
    help="Final z position: [percent]")
parser.add_argument(
    '--no-render', dest='render', action='store_false',
    help="Usefull when using blender without -b option")
parser.set_defaults(render=True)

if '--' in sys.argv:
    argv = sys.argv
    sys.argv = [' '.join(argv[:argv.index('--')])] + argv[argv.index('--')+1:]
else:
    sys.argv = [' '.join(sys.argv)]

try:
    main(parser.parse_args())
except ArgumentParserError:
    pass
except SystemExit:
    pass
