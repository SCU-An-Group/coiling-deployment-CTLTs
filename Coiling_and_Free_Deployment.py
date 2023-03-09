from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
import os

Mdb()

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

#Create a part DCB
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=400.0)
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(0.0, 0.0), 
    direction=CLOCKWISE, 
    point1=(0.0, 34.0), 
    point2=(34.0*sin(60.0*pi/180.0), 34.0*(1-cos(60.0*pi/180.0))))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(34.0*sin(60.0*pi/180.0)*2.0, 34.0), 
    direction=COUNTERCLOCKWISE, 
    point1=(34.0*sin(60.0*pi/180.0), 34.0*(1-cos(60.0*pi/180.0))), 
    point2=(34.0*sin(60.0*pi/180.0)*2.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(34.0*sin(60.0*pi/180.0)*2.0, 0.0), 
    point2=(34.0*sin(60.0*pi/180.0)*2.0 +10.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(0.0, 0.0), 
    direction=COUNTERCLOCKWISE, 
    point1=(0.0, -34.0), 
    point2=(34.0*sin(60.0*pi/180.0), -34.0*(1-cos(60.0*pi/180.0))))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(34.0*sin(60.0*pi/180.0)*2.0, -34.0), 
    direction=CLOCKWISE, 
    point1=(34.0*sin(60.0*pi/180.0), -34.0*(1-cos(60.0*pi/180.0))), 
    point2=(34.0*sin(60.0*pi/180.0)*2.0, 0.0))

mdb.models['Model-1'].Part(dimensionality=THREE_D, name='DCB', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['DCB'].BaseShellExtrude(depth=1000.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].parts['DCB'].ReferencePoint(point=
    mdb.models['Model-1'].parts['DCB'].InterestingPoint(
    mdb.models['Model-1'].parts['DCB'].edges.findAt((8.799848, -32.841478, 
    1000.0), ), CENTER))
mdb.models['Model-1'].parts['DCB'].features.changeKey(fromName='RP', toName=
    'Ref6')

##part the DCB
mdb.models['Model-1'].parts['DCB'].PartitionFaceByCurvedPathEdgeParams(edge1=
    mdb.models['Model-1'].parts['DCB'].edges.findAt((0.0, 34.0, 250.0), ), 
    edge2=mdb.models['Model-1'].parts['DCB'].edges.findAt((29.444864, 17.0, 
    250.0), ), face=mdb.models['Model-1'].parts['DCB'].faces.findAt((27.282955, 
    20.288922, 666.666667), ), parameter1=0.01, parameter2=0.01)
mdb.models['Model-1'].parts['DCB'].PartitionFaceByCurvedPathEdgeParams(edge1=
    mdb.models['Model-1'].parts['DCB'].edges.findAt((29.444864, 17.0, 2.5), ), 
    edge2=mdb.models['Model-1'].parts['DCB'].edges.findAt((58.889727, 0.0, 
    250.0), ), face=mdb.models['Model-1'].parts['DCB'].faces.findAt((54.960484, 
    0.227807, 667.190265), ), parameter1=1.0, parameter2=0.01)
mdb.models['Model-1'].parts['DCB'].PartitionFaceByCurvedPathEdgeParams(edge1=
    mdb.models['Model-1'].parts['DCB'].edges.findAt((58.889727, 0.0, 2.5), ), 
    edge2=mdb.models['Model-1'].parts['DCB'].edges.findAt((68.889727, 0.0, 
    250.0), ), face=mdb.models['Model-1'].parts['DCB'].faces.findAt((62.223061, 
    0.0, 667.190265), ), parameter1=1.0, parameter2=0.01)



##Create rigid plate1
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-25.0, 50.0), 
    point2=(15.0, 50.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[2])
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(15.0, 55.0), direction=COUNTERCLOCKWISE, point1=(15.0, 50.0), point2=(20.0, 55.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='plate1', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['plate1'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

#Creat rigid referencepoint
mdb.models['Model-1'].parts['plate1'].ReferencePoint(point=
    mdb.models['Model-1'].parts['plate1'].InterestingPoint(
    mdb.models['Model-1'].parts['plate1'].edges.findAt((12.5, 50.0, 90.0), ), MIDDLE))
mdb.models['Model-1'].parts['plate1'].features.changeKey(fromName='RP', toName=
    'Ref1')
mdb.models['Model-1'].parts['plate1'].Set(name='Ref1', referencePoints=(
    mdb.models['Model-1'].parts['plate1'].referencePoints[2], ))

mdb.models['Model-1'].parts['plate1'].Set(name='Set-2', referencePoints=(
    mdb.models['Model-1'].parts['plate1'].referencePoints[2], ))
mdb.models['Model-1'].parts['plate1'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models['Model-1'].parts['plate1'].sets['Set-2'])


##Create rigid plate2
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(
    point1=(-25.0, 0.0), 
    point2=(15.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry[2])
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(
    center=(15.0, -5.0), direction=COUNTERCLOCKWISE, point1=(20.0, -5.0), point2=(15.0, 0.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='plate2', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['plate2'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']


mdb.models['Model-1'].parts['plate2'].ReferencePoint(point=
    mdb.models['Model-1'].parts['plate2'].InterestingPoint(
    mdb.models['Model-1'].parts['plate2'].edges.findAt((12.5, 0.0, 90.0), ), 
    MIDDLE))
mdb.models['Model-1'].parts['plate2'].features.changeKey(fromName='RP', toName=
    'Ref2')

mdb.models['Model-1'].parts['plate2'].Set(name='Ref2', referencePoints=(
    mdb.models['Model-1'].parts['plate2'].referencePoints[2], ))
mdb.models['Model-1'].parts['plate2'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models['Model-1'].parts['plate2'].sets['Ref2'])


##Create rigid plate3
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-5.0, 0.0), point2=
    (5.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0), 
    ))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='plate3', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['plate3'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].parts['plate3'].ReferencePoint(point=(0.0, -80.9, 90.0))
mdb.models['Model-1'].parts['plate3'].features.changeKey(fromName='RP', toName=
    'Ref5')

mdb.models['Model-1'].parts['plate3'].Set(name='Set-1', referencePoints=(
    mdb.models['Model-1'].parts['plate3'].referencePoints[2], ))
mdb.models['Model-1'].parts['plate3'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models['Model-1'].parts['plate3'].sets['Set-1'])

##Creat rigid Center Roller
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 80.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='C_Roller', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['C_Roller'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].parts['C_Roller'].ReferencePoint(point=
    mdb.models['Model-1'].parts['C_Roller'].InterestingPoint(
    mdb.models['Model-1'].parts['C_Roller'].edges.findAt((80.0, 0.0, 90.0), ), 
    CENTER))
mdb.models['Model-1'].parts['C_Roller'].features.changeKey(fromName='RP', 
    toName='Ref3')

mdb.models['Model-1'].parts['C_Roller'].Set(name='Set-1', referencePoints=(
    mdb.models['Model-1'].parts['C_Roller'].referencePoints[2], ))
mdb.models['Model-1'].parts['C_Roller'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models['Model-1'].parts['C_Roller'].sets['Set-1'])


##Creat Constraint shaft
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=300.0)
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 87.0), point1=(0.0, 82.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Cst_shaft', type=
    DISCRETE_RIGID_SURFACE)
mdb.models['Model-1'].parts['Cst_shaft'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

mdb.models['Model-1'].parts['Cst_shaft'].ReferencePoint(point=
    mdb.models['Model-1'].parts['Cst_shaft'].InterestingPoint(
    mdb.models['Model-1'].parts['Cst_shaft'].edges.findAt((-5.0, 87.0, 90.0), 
    ), CENTER))
mdb.models['Model-1'].parts['Cst_shaft'].features.changeKey(fromName='RP', 
    toName='Ref4')

mdb.models['Model-1'].parts['Cst_shaft'].Set(name='Set-1', referencePoints=(
    mdb.models['Model-1'].parts['Cst_shaft'].referencePoints[2], ))
mdb.models['Model-1'].parts['Cst_shaft'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models['Model-1'].parts['Cst_shaft'].sets['Set-1'])

##set DCB_single_ply and DCB_double_ply
mdb.models['Model-1'].parts['DCB'].Set(faces=
    mdb.models['Model-1'].parts['DCB'].faces.findAt(((31.606773, 13.711078, 
    340.0), ), ((3.929244, 33.772193, 340.0), ), ((3.929244, -33.772193, 
    666.666667), ), ((31.606773, -13.711078, 666.666667), ), ((54.960484, 
    0.227807, 7.190265), ), ((27.282955, 20.288922, 6.666667), ), ), name=
    'DCB_single')
mdb.models['Model-1'].parts['DCB'].Set(faces=
    mdb.models['Model-1'].parts['DCB'].faces.findAt(((65.556393, 0.0, 6.666667), ),  
    ((62.223061, 0.0, 340.0), ), ), name='DCB_doub')


##create material
mdb.models['Model-1'].Material(name='Composite_material')
mdb.models['Model-1'].materials['Composite_material'].Elastic(table=((80080.0, 
    6670.0, 0.34, 2930.0, 2930.0, 2500.0), ), type=LAMINA)
mdb.models['Model-1'].materials['Composite_material'].Density(table=((1.6e-09, 
    ), ))


mdb.models['Model-1'].CompositeShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, 
    layup=(SectionLayer(thickness=0.08, orientAngle=45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=45.0, material='Composite_material')), 
    name='Section-1', 
    poissonDefinition=DEFAULT, preIntegrate=OFF, symmetric=False, temperature=GRADIENT, 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)

mdb.models['Model-1'].parts['DCB'].SectionAssignment(
    offset=0.0, 
    offsetField='', 
    offsetType=MIDDLE_SURFACE, 
    region=mdb.models['Model-1'].parts['DCB'].sets['DCB_single'], 
    sectionName='Section-1', 
    thicknessAssignment=FROM_SECTION)

mdb.models['Model-1'].CompositeShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, 
    layup=(SectionLayer(thickness=0.08, orientAngle=45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=0.08, orientAngle=45.0, material='Composite_material')), 
    name='Section-2', 
    poissonDefinition=DEFAULT, preIntegrate=OFF, symmetric=True, temperature=GRADIENT, 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)

mdb.models['Model-1'].parts['DCB'].SectionAssignment(
    offset=0.0, 
    offsetField='', 
    offsetType=MIDDLE_SURFACE, 
    region=mdb.models['Model-1'].parts['DCB'].sets['DCB_doub'], 
    sectionName='Section-2', 
    thicknessAssignment=FROM_SECTION)

##change the direction of the composite material
mdb.models['Model-1'].parts['DCB'].MaterialOrientation(additionalRotationType=
    ROTATION_NONE, axis=AXIS_2, fieldName='', localCsys=None, orientationType=
    GLOBAL, region=mdb.models['Model-1'].parts['DCB'].sets['DCB_single'])
mdb.models['Model-1'].parts['DCB'].MaterialOrientation(additionalRotationType=
    ROTATION_NONE, axis=AXIS_2, fieldName='', localCsys=None, orientationType=
    GLOBAL, region=mdb.models['Model-1'].parts['DCB'].sets['DCB_doub'])


##Assmebly##
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='C_Roller-1', 
    part=mdb.models['Model-1'].parts['C_Roller'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Cst_shaft-1', 
    part=mdb.models['Model-1'].parts['Cst_shaft'])
mdb.models['Model-1'].rootAssembly.rotate(angle=5.0, axisDirection=(0.0, 0.0, 
    -1.0), axisPoint=(0.0, 0.0, 1.0), instanceList=('Cst_shaft-1', ))
mdb.models['Model-1'].rootAssembly.RadialInstancePattern(axis=(0.0, 0.0, 1.0), 
    instanceList=('Cst_shaft-1', ), number=11, point=(0.0, 0.0, 0.0), 
    totalAngle=360.0)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='DCB-1', part=
    mdb.models['Model-1'].parts['DCB'])
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='plate1-1', 
    part=mdb.models['Model-1'].parts['plate1'])
mdb.models['Model-1'].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 10.0, 
    0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('DCB-1', ))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('DCB-1', ), 
    vector=(-5.0, 80.5, 90.0))
mdb.models['Model-1'].rootAssembly.translate(instanceList=('plate1-1', ), 
    vector=(20.0, 64.7, 0.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='plate2-1', 
    part=mdb.models['Model-1'].parts['plate2'])
mdb.models['Model-1'].rootAssembly.translate(instanceList=('plate2-1', ), 
    vector=(20.0, 46.3, 0.0))
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='plate3-1', 
    part=mdb.models['Model-1'].parts['plate3'])
mdb.models['Model-1'].rootAssembly.translate(instanceList=('plate3-1', ), 
    vector=(0.0, 80.9, 0.0))



mdb.models['Model-1'].rootAssembly.Set(name='Ref1', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['plate1-1'].referencePoints[2], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='Ref2', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['plate2-1'].referencePoints[2], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='Ref3', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['C_Roller-1'].referencePoints[2], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='Ref4', referencePoints=((
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-2'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-11'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-10'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-9'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-8'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-7'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-6'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-5'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-4'].referencePoints[2], 
    ), (
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-3'].referencePoints[2], 
    )))
mdb.models['Model-1'].rootAssembly.Set(name='Ref5', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['plate3-1'].referencePoints[2], 
    ))
mdb.models['Model-1'].rootAssembly.Set(name='Ref6', referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].referencePoints[2], 
    ))

mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].edges.findAt(((995.0, 
    80.5, 23.610273), ), ((995.0, 81.658522, 39.91012), ), ((995.0, 104.541631, 
    65.958369), ), ((995.0, 47.658522, 81.200152), ), ((995.0, 70.541631, 
    55.151903), ), ), name='DCB_section')
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].edges.findAt(((-5.0, 
    47.658522, 81.200152), ), ((-5.0, 70.541631, 55.151903), ), ((-5.0, 
    90.458369, 55.151903), ), ((-5.0, 113.341478, 81.200152), ), ((-5.0, 80.5, 
    28.610273), ), ), name='DCB_section2')

mdb.models['Model-1'].rootAssembly.ReferencePoint(point=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].InterestingPoint(
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].edges.findAt((-5.0, 
    47.658522, 81.200152), ), CENTER))
mdb.models['Model-1'].rootAssembly.Set(name='center', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[42], ))

mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].edges.findAt(((252.5, 
    114.5, 90.0), ), ((-2.5, 46.5, 90.0), ),((245.0, 46.5, 90.0), ), ), name='plane_symmetry')

##mesh##
mdb.models['Model-1'].parts['C_Roller'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=8)
mdb.models['Model-1'].parts['C_Roller'].generateMesh()
mdb.models['Model-1'].parts['C_Roller'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models['Model-1'].parts['C_Roller'].faces, ))
mdb.models['Model-1'].parts['Cst_shaft'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=3.0)
mdb.models['Model-1'].parts['Cst_shaft'].generateMesh()
mdb.models['Model-1'].parts['Cst_shaft'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models['Model-1'].parts['Cst_shaft'].faces, ))


mdb.models['Model-1'].parts['DCB'].seedPart(deviationFactor=0.1, minSizeFactor=
    0.1, size=5.0)
mdb.models['Model-1'].parts['DCB'].generateMesh()
mdb.models['Model-1'].parts['DCB'].setElementType(elemTypes=(ElemType(
    elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
    hourglassControl=STIFFNESS), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
    regions=(mdb.models['Model-1'].parts['DCB'].faces, ))


mdb.models['Model-1'].parts['plate1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=10.0)
mdb.models['Model-1'].parts['plate1'].generateMesh()
mdb.models['Model-1'].parts['plate1'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models['Model-1'].parts['plate1'].faces, ))
mdb.models['Model-1'].parts['plate2'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=10.0)
mdb.models['Model-1'].parts['plate2'].generateMesh()
mdb.models['Model-1'].parts['plate2'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models['Model-1'].parts['plate2'].faces, ))
mdb.models['Model-1'].parts['plate3'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=4.0)
mdb.models['Model-1'].parts['plate3'].generateMesh()
mdb.models['Model-1'].parts['plate3'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models['Model-1'].parts['plate3'].faces, ))
mdb.models['Model-1'].rootAssembly.regenerate()




##create surface for the model
mdb.models['Model-1'].rootAssembly.Surface(name='plate1_bottom', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['plate1-1'].faces.findAt(((
    39.957717, 119.051123, 60.0), ), ((21.666667, 114.7, 60.0), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='plate2_top', side2Faces=
    mdb.models['Model-1'].rootAssembly.instances['plate2-1'].faces.findAt(((
    39.957717, 41.948876, 60.0), ), ((21.666667, 46.3, 60.0), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='plate3_bottom', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['plate3-1'].faces.findAt(((
    1.666667, 80.9, 60.0), )))
mdb.models['Model-1'].rootAssembly.Surface(name='Roller_surface', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['C_Roller-1'].faces.findAt(((
    -79.986964, 1.444175, 30.0), )))
mdb.models['Model-1'].rootAssembly.Surface(name='shafts_surface', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-2'].faces.findAt(
    ((-38.745642, 72.319655, 60.0), (-0.662901, -0.748707, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1'].faces.findAt(((
    6.504049, 81.78664, 60.0), (0.722797, -0.691061, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-11'].faces.findAt(
    ((49.68875, 65.286946, 60.0), (0.479738, -0.877412, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-10'].faces.findAt(
    ((77.097625, 28.059107, 60.0), (-0.306565, -0.95185, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-9'].faces.findAt(
    ((80.028548, -18.0773, 60.0), (-0.912751, -0.408516, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-8'].faces.findAt(
    ((57.550972, -58.474292, 60.0), (-0.911224, 0.41191, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-7'].faces.findAt(
    ((16.80137, -80.306109, 60.0), (-0.294011, 0.955802, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-6'].faces.findAt(
    ((-29.282549, -76.641304, 60.0), (0.522632, 0.852558, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-5'].faces.findAt(
    ((-66.069465, -48.643427, 60.0), (0.984991, 0.172603, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-4'].faces.findAt(
    ((-81.879793, -5.201605, 60.0), (0.783423, -0.621489, 0.0)), )+\
    mdb.models['Model-1'].rootAssembly.instances['Cst_shaft-1-rad-3'].faces.findAt(
    ((-71.693865, 39.891689, 60.0), (0.065621, -0.997845, 0.0)), ))
mdb.models['Model-1'].rootAssembly.Surface(name='DCB', side12Faces=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].faces.findAt(((335.0, 
    80.5, 27.776939), ), ((335.0, 94.211078, 58.393227), ), ((335.0, 
    114.272193, 86.070756), ), ((661.666667, 46.727807, 86.070756), ), ((
    661.666667, 66.788922, 58.393227), ), ((2.190265, 80.727807, 35.039516), ), 
    ((1.666667, 100.788922, 62.717045), ), ((1.666667, 80.5, 24.443607), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='DCB_bottom', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].faces.findAt(((335.0, 
    80.5, 27.776939), ), ((1.666667, 80.5, 24.443607), ), ), side2Faces=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].faces.findAt(((
    661.666667, 46.727807, 86.070756), ), ((661.666667, 66.788922, 58.393227), 
    ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='DCB_smalltop', side2Faces=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].faces.findAt(((
    2.190265, 80.727807, 35.039516), ), ((1.666667, 100.788922, 62.717045), ), 
    ((1.666667, 80.5, 24.443607), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='DCB_top', side2Faces=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].faces.findAt(((335.0, 
    80.5, 27.776939), ), ((335.0, 94.211078, 58.393227), ), ((335.0, 
    114.272193, 86.070756), ), ((2.190265, 80.727807, 35.039516), ), ((
    1.666667, 100.788922, 62.717045), ), ((1.666667, 80.5, 24.443607), ), ))


##Step##
mdb.models['Model-1'].ExplicitDynamicsStep(description='Compress-the-DCB', 
    improvedDtMethod=ON, name='Flatten', previous='Initial', timePeriod=1.0)
mdb.models['Model-1'].ExplicitDynamicsStep(description='change-the-contact', 
    improvedDtMethod=ON, name='New_contact', previous='Flatten', timePeriod=
    0.5)
mdb.models['Model-1'].ExplicitDynamicsStep(description='Coiling-deformation', 
    improvedDtMethod=ON, name='Coiling', previous='New_contact', timePeriod=
    2.0)
mdb.models['Model-1'].ExplicitDynamicsStep(description='unfold_freely', 
    improvedDtMethod=ON, name='free_unfold', previous='Coiling', timePeriod=
    2.0)


mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=
    0.01)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(
    stepName='New_contact', timeInterval=0.005)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValuesInStep(
    stepName='Coiling', timeInterval=0.01)
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
    'RF', 'CSTRESS', 'EVF', 'COORD'))

mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(
    timeInterval=0.01)
mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValuesInStep(
    stepName='New_contact', timeInterval=0.005)
mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValuesInStep(
    stepName='Coiling', timeInterval=0.01)



##Interaction##
mdb.models['Model-1'].ContactProperty('IntProp-1-nofric')
mdb.models['Model-1'].interactionProperties['IntProp-1-nofric'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models['Model-1'].interactionProperties['IntProp-1-nofric'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models['Model-1'].ContactProperty('IntProp-2-fric')
mdb.models['Model-1'].interactionProperties['IntProp-2-fric'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
    table=((0.1, ), ), temperatureDependency=OFF)
mdb.models['Model-1'].interactionProperties['IntProp-2-fric'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models['Model-1'].ContactProperty('IntProp-3-cling')
mdb.models['Model-1'].interactionProperties['IntProp-3-cling'].TangentialBehavior(
    formulation=ROUGH)
mdb.models['Model-1'].interactionProperties['IntProp-3-cling'].NormalBehavior(
    allowSeparation=OFF, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)

mdb.models['Model-1'].ContactExp(createStepName='Initial', name='Int-1')
mdb.models['Model-1'].interactions['Int-1'].includedPairs.setValuesInStep(
    addPairs=((mdb.models['Model-1'].rootAssembly.surfaces['DCB'], SELF), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate1_bottom'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB']), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate2_top'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB'])), stepName='Initial', 
    useAllstar=OFF)
mdb.models['Model-1'].interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1-nofric'), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate1_bottom'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB'], 'IntProp-2-fric'), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate2_top'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB'], 'IntProp-2-fric')), 
    stepName='Initial')
mdb.models['Model-1'].interactions['Int-1'].deactivate('New_contact')
mdb.models['Model-1'].ContactExp(createStepName='New_contact', name='Int-2')
mdb.models['Model-1'].interactions['Int-2'].includedPairs.setValuesInStep(
    addPairs=((mdb.models['Model-1'].rootAssembly.surfaces['DCB'], SELF), (
    mdb.models['Model-1'].rootAssembly.surfaces['Roller_surface'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB']), (
    mdb.models['Model-1'].rootAssembly.surfaces['shafts_surface'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB']), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate3_bottom'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB_smalltop'])), stepName=
    'New_contact', useAllstar=OFF)
mdb.models['Model-1'].interactions['Int-2'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1-nofric'), (
    mdb.models['Model-1'].rootAssembly.surfaces['plate3_bottom'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB_smalltop'], 
    'IntProp-3-cling')), stepName='New_contact')
mdb.models['Model-1'].interactions['Int-2'].includedPairs.setValuesInStep(
    removePairs=((
    mdb.models['Model-1'].rootAssembly.surfaces['shafts_surface'], 
    mdb.models['Model-1'].rootAssembly.surfaces['DCB']), ), stepName=
    'free_unfold')

#create coupling:DCBsection
mdb.models['Model-1'].Coupling(controlPoint=
    mdb.models['Model-1'].rootAssembly.sets['Ref6'], couplingType=STRUCTURAL, 
    influenceRadius=WHOLE_SURFACE, localCsys=None, name='Ref6_with_DCBsection', 
    surface=mdb.models['Model-1'].rootAssembly.sets['DCB_section'], u1=ON, u2=
    ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
#create coupling:DCBsection2
mdb.models['Model-1'].Coupling(controlPoint=
    mdb.models['Model-1'].rootAssembly.sets['center'], couplingType=STRUCTURAL, 
    influenceRadius=WHOLE_SURFACE, localCsys=None, name=
    'center_with_DCBsection2', surface=
    mdb.models['Model-1'].rootAssembly.sets['DCB_section2'], u1=ON, u2=ON, u3=
    ON, ur1=ON, ur2=ON, ur3=ON, weightingMethod=UNIFORM)

##create load##
mdb.models['Model-1'].SmoothStepAmplitude(data=((0.0, 0.0), (1.0, 1.0)), name=
    'Smooth1', timeSpan=STEP)
mdb.models['Model-1'].SmoothStepAmplitude(data=((0.0, 0.0), (2.0, 1.0)), name=
    'Smooth2', timeSpan=STEP)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate1', 
    region=mdb.models['Model-1'].rootAssembly.sets['Ref1'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].boundaryConditions['BC-plate1'].setValuesInStep(
    amplitude='Smooth1', stepName='Flatten', u2=-33.8)
mdb.models['Model-1'].boundaryConditions['BC-plate1'].setValuesInStep(stepName=
    'New_contact', u2=0.0)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Ref2'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].boundaryConditions['BC-plate2'].setValuesInStep(
    amplitude='Smooth1', stepName='Flatten', u2=33.8)
mdb.models['Model-1'].boundaryConditions['BC-plate2'].setValuesInStep(stepName=
    'New_contact', u2=0.0)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-shafts', 
    region=mdb.models['Model-1'].rootAssembly.sets['Ref4'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-Roller', 
    region=mdb.models['Model-1'].rootAssembly.sets['Ref3'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].boundaryConditions['BC-Roller'].setValuesInStep(
    amplitude='Smooth2', stepName='Coiling', ur3=10.5)
mdb.models['Model-1'].boundaryConditions['BC-Roller'].setValuesInStep(stepName=
    'free_unfold', ur3=0.0)

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate3', 
    region=mdb.models['Model-1'].rootAssembly.sets['Ref5'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models['Model-1'].boundaryConditions['BC-plate3'].setValuesInStep(
    amplitude='Smooth2', stepName='Coiling', ur3=10.5)
mdb.models['Model-1'].boundaryConditions['BC-plate3'].setValuesInStep(stepName=
    'free_unfold', ur3=0.0)
# mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
#     distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-DCB', 
#     region=mdb.models['Model-1'].rootAssembly.sets['Ref6'], u1=UNSET, u2=SET, 
#     u3=SET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
# mdb.models['Model-1'].boundaryConditions['BC-DCB'].deactivate('free_unfold')

mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'BC-DCBsection2', region=mdb.models['Model-1'].rootAssembly.sets['center'], 
    u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].boundaryConditions['BC-DCBsection2'].deactivate(
    'New_contact')

mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='free_unfold', 
    distributionType=VISCOUS, field='', magnitude=1e-08, name=
    'viscous_pressure_DCBtop', region=
    mdb.models['Model-1'].rootAssembly.surfaces['DCB_top'])
mdb.models['Model-1'].Pressure(amplitude=UNSET, createStepName='free_unfold', 
    distributionType=VISCOUS, field='', magnitude=1e-08, name=
    'viscous_pressure_bottom', region=
    mdb.models['Model-1'].rootAssembly.surfaces['DCB_bottom'])

mdb.models['Model-1'].ZsymmBC(createStepName='Initial', localCsys=None, name=
    'BC-symplane', region=
    mdb.models['Model-1'].rootAssembly.sets['plane_symmetry'])

mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['DCB-1'].edges.findAt(((995.0, 
    80.5, 23.610273), )), name='line')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-line', 
    region=mdb.models['Model-1'].rootAssembly.sets['line'], u1=UNSET, u2=SET, 
    u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].boundaryConditions['BC-line'].deactivate('free_unfold')

#Job##
if not os.path.exists('FEModelFiles'):
    os.mkdir('FEModelFiles')
os.chdir('FEModelFiles')
jobName = 'halfDCB_coiling_and_free_unfold'
mdb.Job(model='Model-1', name=jobName, explicitPrecision=DOUBLE_PLUS_PACK, numCpus=16, numDomains=16)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
