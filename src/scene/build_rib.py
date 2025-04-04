#!/usr/bin/env rmanpy
import prman


ri = prman.Ri()
ri.Begin("../../build/out.rib")
ri.Option("searchpath", {"string texture": "./textures/:@"})

ri.Display("rgb.exr", "it", "rgba")
# ri.Format(1024, 720, 1)
ri.Format(720,480, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 40})

ri.Integrator("PxrPathTracer", "integrator")

ri.Rotate(-20, 1, 0, 0)
ri.Translate(0, -3, 10)
# ri.Rotate(-90, 0, 1, 0)
ri.WorldBegin()

ri.TransformBegin()
ri.AttributeBegin()
ri.Translate(0, 0, 0)

## shader begin

ri.Pattern("water", "waterShader", {"float scale": [0.01], "float height":[0.1]})

# displacement
ri.Attribute("trace", {"int displacements": [1]})
ri.Attribute("displacementbound", {"float sphere": [2], "string coordinatesystem": ["shader"]})
ri.Displace(
    "PxrDisplace", # shader
    "water_displace", # name
    { # parameters
        "uniform float dispAmount": [0.04],
        "reference float dispScalar": ["waterShader:outDisplacement"]
    },
)

ri.Attribute("visibility", {"int transmission": [1]})
ri.Bxdf('PxrDisney','id',
{
	'color baseColor' : [0,0.01,0.05], 
	'float subsurface' : [0], 
	'color subsurfaceColor' : [0,0,0], 
	'float metallic' : [1], 
	'float specular' : [1], 
	'float specularTint' : [0], 
	'float roughness' : [0], 
	'float anisotropic' : [0], 
	'float sheen' : [0], 
	'float sheenTint' : [.5], 
	'float clearcoat' : [0], 
	'float clearcoatGloss' : [1], 
	'normal bumpNormal' : [0,0,0], 
	'float presence' : [1], 
	'int inputAOV' : [0], 
})


## shader end

program = 'Procedural "RunProgram" ["bin/procedural" ""] [-5 5 -5 5 -5 5]\n'
# ri.ArchiveRecord(ri.VERBATIM, program)
patch_size = 20
ri.Patch("bilinear", {"P": [0.5*patch_size, 0.0, 0.5*patch_size, 0.5*patch_size, 0.0, -0.5*patch_size, -0.5*patch_size, 0.0, 0.5*patch_size, -0.5*patch_size, 0.0, -0.5*patch_size]})

ri.AttributeEnd()
ri.TransformEnd()
ri.Sphere(0.5, -1, 1, 360)

ri.TransformBegin()
ri.AttributeBegin()
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(100, 0, 0, 1)
# ri.Light("PxrEnvDayLight", "sun", {
#     "float intensity": [10.0]
# })
ri.Light("PxrDomeLight", "domeLight", {"string lightColorMap": "lake_pier_1k.tex"})


ri.AttributeEnd()
ri.TransformEnd()

ri.WorldEnd()
ri.End()
