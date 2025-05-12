#!/usr/bin/env rmanpy
import prman


ri = prman.Ri()
ri.Begin("../../build/out.rib")
ri.Option("searchpath", {"string texture": "./textures/:@"})

ri.Display("rgb.exr", "it", "rgba")
ri.Display("+rgb.exr", "openexr", "rgba")

ri.DisplayChannel("float z")

ri.Display("+zdepth.exr", "openexr", "z", {
    "string filter": "zmin",
    "string data": "z"
})
image_scale = 1
ri.Format(1920*image_scale, 1080*image_scale, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 40})

ri.Integrator("PxrPathTracer", "integrator")

ri.Rotate(-10, 1, 0, 0)
ri.Translate(0, -3, 10)
# ri.Rotate(-90, 0, 1, 0)


ri.WorldBegin()

ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0, 0, 0)

## shader begin

ri.Pattern("water", "waterShader", {"float height":[0.05]})

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
ri.Translate(0,0,0.3)
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
