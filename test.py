#!/usr/bin/env rmanpy
import prman


ri = prman.Ri()
ri.Begin("out.rib")
ri.Option("searchpath", {"string texture": "./textures/:@"})

ri.Display("rgb.exr", "it", "rgba")
ri.Format(1024, 720, 1)
ri.Projection(ri.PERSPECTIVE, {ri.FOV: 40})

ri.Integrator("PxrPathTracer", "integrator")

ri.Rotate(-12, 1, 0, 0)
ri.Translate(0, -0.5, 2.5)
ri.WorldBegin()

ri.TransformBegin()
ri.AttributeBegin()
ri.Bxdf("PxrSurface", "MTL_ball", { })
ri.Translate(0, 0, 0)
# ri.Sphere(0.5, -1, 1, 360)
program = 'Procedural "RunProgram" ["procedural" ""] [-5 5 -5 5 -5 5]\n'
# program = 'Procedural "RunProgram" ["procedural.sh" ""] [-5 5 -5 5 -5 5]\n'
ri.ArchiveRecord(ri.VERBATIM, program)
# ri.Patch("bilinear", {"P": [0.5, 0.0, 0.5, 0.5, 0.0, -0.5, -0.5, 0.0, 0.5, -0.5, 0.0, -0.5]})

ri.AttributeEnd()
ri.TransformEnd()

ri.TransformBegin()
ri.AttributeBegin()
ri.Declare("domeLight", "string")
ri.Rotate(-90, 1, 0, 0)
ri.Rotate(100, 0, 0, 1)
ri.Light("PxrEnvDayLight", "sun", {
    "float intensity": [10.0]
})

ri.AttributeEnd()
ri.TransformEnd()

ri.WorldEnd()
ri.End()
