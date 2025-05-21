#!/usr/bin/env rmanpy
import prman
import argparse

def parseArgs():
    parser = argparse.ArgumentParser(description ='Process some integers.')
    parser.add_argument("-fs", "--frameStart",
                        type = int,
                        default = 1,
                        help ="first frame in range to render")

    parser.add_argument("-fe", "--frameEnd",
                        type = int,
                        default = 1,
                        help ="last frame in range to render")

    parser.add_argument("-is", "--imageScale",
                        type = float,
                        default = 0.3,
                        help ="scale of the resolution to render")

    parser.add_argument("-rw", "--resolutionWidth",
                        type = int,
                        default = 1920,
                        help ="width of the resolution to render")

    parser.add_argument("-rh", "--resolutionHeight",
                        type = int,
                        default = 1080,
                        help ="height of the resolution to render")

    parser.add_argument("-ws", "--waveSpeed",
                        type = float,
                        default = 0.06,
                        help ="how fast the waves should move each frame")

    parser.add_argument("-v", "--viewer",
                        action='store_true',
                        help="Output to viewer")

    parser.add_argument("--no-viewer",
                        dest='viewer',
                        action='store_false',
                        help="Output to a file instead of viewer")

    parser.set_defaults(viewer=True)

    args = parser.parse_args()

    return args

def camera1(ri):
    ri.Rotate(-10, 1, 0, 0)
    ri.Translate(0, -3, 10)

def camera2(ri):
    ri.Rotate(-10, 1, 10, 0)
    ri.Rotate(90, 0, 1, 0)
    ri.Translate(0, -1, -20)

def main():
    args = parseArgs()

    speed = args.waveSpeed
    image_scale = args.imageScale

    print("start frame: ", args.frameStart)
    print("end frame: ", args.frameEnd)

    for i in range(args.frameStart, args.frameEnd):
        print("writing frame: ", i)
        frame = i
        f4 = str(i).zfill(4)
        ri = prman.Ri()

        ri.Begin("../../build/out_{}.rib".format(f4))
        ri.Option("searchpath", {"string texture": "./textures/:@"})
        ri.Option("trace", {"int geocachememory": 1024*8})

        if(args.viewer):
            print("outputing to viewer")
            ri.Display("rgb_{}.exr".format(f4), "it", "rgba")
        else:
            file_path = "renders/rgb_{}.exr".format(f4)
            print("outputing to file:", file_path)
            ri.Display(file_path, "openexr", "rgba")

        ri.DisplayChannel("float z")

        ri.Display("+renders/zdepth_{}.exr".format(f4), "openexr", "z", {
            "string filter": "zmin",
            "string data": "z"
        })
        ri.Format(int(1920*image_scale), int(1080*image_scale), 1)
        ri.Projection(ri.PERSPECTIVE, {ri.FOV: 40})

        ri.Integrator("PxrPathTracer", "integrator")

        # camera 1
        # camera1(ri)
        camera2(ri)

        # camera 2

        ri.WorldBegin()

        ri.TransformBegin()
        ri.AttributeBegin()
        ri.Translate(0, 0, 0)

        ## shader begin


        ri.Pattern("water", "waterShader", {"float height":[0.05], "int frame":[frame], "float speed":[speed]})

        # displacement
        ri.Attribute("trace", {"int displacements": [1]})
        ri.Attribute("displacementbound", {"float sphere": [10], "string coordinatesystem": ["shader"]})
        ri.Displace(
            "PxrDisplace", # shader
            "water_displace", # name
            { # parameters
                "uniform float dispAmount": [1],
                # "reference float dispScalar": ["waterShader:outDisplacement"],
                "reference vector dispVector": ["waterShader:outDisplacement"],
            },
        )

        ri.Attribute("visibility", {"int transmission": [1]})
        ri.Bxdf('PxrSurface', 'waterSurface',
        {
            # 'color diffuseColor' : [0.286, 0.353, 0.337],
            "reference color diffuseColor": ["waterShader:outDiffuse"],
            'float diffuseGain' : [1.0],
            'float diffuseRoughness' : [0.0],
            'color specularIor' : [1.333 ,1.333 ,1.333 ], # doesn't make a visible difference

            # 'float subsurfaceGain' : [0.5], 
            # 'color subsurfaceColor' : [1,0,0], 
         #    'float subsurfaceDmfp' : [0.1],

            'color specularFaceColor' : [0.1, 0.11, 0.12],
            # "reference color specularFaceColor": ["waterShader:outDiffuse"],
            'float specularRoughness' : [0.05],

         #    'float refractionGain' : [1.0], 
            # 'color refractionColor' : [0,0.4,0.5], 
        })


        ## shader end

        # program = 'Procedural "RunProgram" ["bin/procedural" ""] [-5 5 -5 5 -5 5]\n'
        # ri.ArchiveRecord(ri.VERBATIM, program)
        patch_size = 500
        ri.Patch("bilinear", {"P": [0.5*patch_size, 0.0, 0.5*patch_size, 0.5*patch_size, 0.0, -0.5*patch_size, -0.5*patch_size, 0.0, 0.5*patch_size, -0.5*patch_size, 0.0, -0.5*patch_size]})

        # buoy
        ri.TransformBegin()
        ri.Bxdf('PxrSurface', 'buoy_surface',
        {
            'color diffuseColor' : [0.965, 0.576, 0.141],
        })
        ri.Displace(
            "PxrDisplace",
            "nodisplace",
        )


        ri.TransformBegin()

        # position
        ri.Translate(7,0,25)

        # wobbly rotation
        ri.Rotate(-12, 1, 0.3, 0.2)

        ri.Rotate(-90, 1, 0, 0)
        # create shape
        buoy_width = 0.35
        ri.Cylinder(0.5*buoy_width, -1, 1, 360)

        ri.Translate(0,0,1)
        ri.Scale(1,1,0.5)
        ri.Sphere(0.5*buoy_width, -1,0.3,360)
        ri.Translate(0,0,0.1)
        ri.Scale(1,1,0.001)
        ri.Sphere(0.4*buoy_width, -1,1,360)
        ri.TransformEnd()



        ri.AttributeEnd()
        ri.TransformEnd()

        ri.TransformBegin()
        ri.AttributeBegin()
        ri.Rotate(-90, 1, 0, 0)
        ri.Rotate(100, 0, 0, 1)
        # ri.Light("PxrEnvDayLight", "sun", {
        #     "float intensity": [10.0]
        # })
        ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "lake_pier_8k.tex"})


        ri.AttributeEnd()
        ri.TransformEnd()

        ri.WorldEnd()
        ri.End()

if(__name__ == "__main__"):
    main()
