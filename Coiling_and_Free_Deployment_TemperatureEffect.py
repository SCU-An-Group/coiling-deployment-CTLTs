from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
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

#Function for creating virtual nodes
def VirtualNodes(mdb, NameModel, NameRef1, x, y, z):
    from part import THREE_D, DEFORMABLE_BODY
    #Create reference parts and assemble
    mdb.models[NameModel].Part(dimensionality=THREE_D, name=NameRef1, type=
        DEFORMABLE_BODY)
    mdb.models[NameModel].parts[NameRef1].ReferencePoint(point=(x,y,z))
    mdb.models[NameModel].rootAssembly.Instance(dependent=ON, name=NameRef1, 
        part=mdb.models[NameModel].parts[NameRef1])

    #Create set of reference points
    mdb.models[NameModel].rootAssembly.Set(name=NameRef1, referencePoints=(
        mdb.models[NameModel].rootAssembly.instances[NameRef1].referencePoints[1],))


Mdb()

# execfile("Parameters_for_coiling_and_free_unfold.py")
R = 34.0
L2 = 0.0

l = 2000.0 # Length
#L2 = 0.0#lumbus  R = 27.0
R1 = R  # Radius
R2 = R  # R1=R2
L1 = 10.0
Theta = (4*pi*34.0/3.0-L2)/(4*R) # degree
#2*L1+4*Theta*R+L2 = 2*10 + 4*pi*34/3
t = 0.08     #composite material layer's thickness
k = 5        #the number of layers
h1 = R1*(1-cos(Theta)) + R2*(1-cos(Theta)) + t*k/2
h2 = 80.0+t*k+0.1
visc = 1e-8

session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

CUModel = 'CoilingandUnfoldModel'
mdb.models.changeKey(fromName='Model-1', toName=CUModel)


#Create a part DCB
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=400.0)
mdb.models[CUModel].sketches['__profile__'].Line(
    point1=(0.0, R1*(1-cos(Theta)) + R2*(1-cos(Theta))), 
    point2=(L2/2.0, R1*(1-cos(Theta)) + R2*(1-cos(Theta))))
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(L2/2.0, R1*(1-cos(Theta)) + R2*(1-cos(Theta)) - R2), 
    direction=CLOCKWISE, 
    point1=(L2/2.0, R1*(1-cos(Theta)) + R2*(1-cos(Theta))),
    point2=(R2*sin(Theta) + L2/2.0, R1*(1-cos(Theta))))
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(R1*sin(Theta) + R2*sin(Theta) + L2/2.0, R1), 
    direction=COUNTERCLOCKWISE, 
    point1=(R2*sin(Theta) + L2/2.0, R1*(1-cos(Theta))),
    point2=(R1*sin(Theta) + R2*sin(Theta) + L2/2.0, 0.0))
mdb.models[CUModel].sketches['__profile__'].Line(
    point1=(R1*sin(Theta) + R2*sin(Theta) + L2/2.0, 0.0), 
    point2=(L1 + R1*sin(Theta) + R2*sin(Theta) + L2/2.0, 0.0))

mdb.models[CUModel].sketches['__profile__'].Line(
    point1=(0.0, -R1*(1-cos(Theta)) - R2*(1-cos(Theta))), 
    point2=(L2/2.0, -R1*(1-cos(Theta)) - R2*(1-cos(Theta))))
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(L2/2.0, -R1*(1-cos(Theta)) - R2*(1-cos(Theta)) + R2), 
    direction=COUNTERCLOCKWISE, 
    point1=(L2/2.0, -R1*(1-cos(Theta)) - R2*(1-cos(Theta))),
    point2=(R2*sin(Theta) + L2/2.0, -R1*(1-cos(Theta))))
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(R1*sin(Theta) + R2*sin(Theta) + L2/2.0, -R1), 
    direction=CLOCKWISE, 
    point1=(R2*sin(Theta) + L2/2.0, -R1*(1-cos(Theta))),
    point2=(R1*sin(Theta) + R2*sin(Theta) + L2/2.0, 0.0))

mdb.models[CUModel].Part(dimensionality=THREE_D, name='DCB', type=
    DEFORMABLE_BODY)
mdb.models[CUModel].parts['DCB'].BaseShellExtrude(depth=l, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']


##part the DCB

mdb.models['CoilingandUnfoldModel'].parts['DCB'].DatumPlaneByPrincipalPlane(
    offset=10.0, principalPlane=XYPLANE)
mdb.models['CoilingandUnfoldModel'].parts['DCB'].PartitionFaceByDatumPlane(
    datumPlane=mdb.models['CoilingandUnfoldModel'].parts['DCB'].datums[2], 
    faces=mdb.models['CoilingandUnfoldModel'].parts['DCB'].faces.findAt(
    ((0.0, R1*(1-cos(Theta))+R2*(1-cos(Theta)), 700.0), ), 
    ((R2*sin(Theta*0.5)+L2/2.0, R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), 700.0), ), 
    ((R1*sin(Theta)+R2*sin(Theta)+L2/2.0-R1*sin(Theta*0.5), R1*(1-cos(Theta*0.5)), 700.0), ), 
    ((L1/2.0+R1*sin(Theta)+R2*sin(Theta)+L2/2.0, 0.0, 700.0), ), ))


##Create rigid plate1
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[CUModel].sketches['__profile__'].Line(
    point1=(-5.0, h2+h1), 
    point2=(35.0, h2+h1))
mdb.models[CUModel].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[CUModel].sketches['__profile__'].geometry[2])
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(35.0, h2+h1+5.0), direction=COUNTERCLOCKWISE, point1=(35.0, h2+h1), point2=(40.0, h2+h1+5.0))
mdb.models[CUModel].Part(dimensionality=THREE_D, name='plate1', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[CUModel].parts['plate1'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']

#Creat rigid referencepoint
mdb.models[CUModel].parts['plate1'].ReferencePoint(point=
    mdb.models[CUModel].parts['plate1'].InterestingPoint(
    mdb.models[CUModel].parts['plate1'].edges.findAt((2.5, h2+h1, 90.0), ), MIDDLE))
mdb.models[CUModel].parts['plate1'].features.changeKey(fromName='RP', toName=
    'Ref1')
mdb.models[CUModel].parts['plate1'].Set(name='Ref1', referencePoints=(
    mdb.models[CUModel].parts['plate1'].referencePoints[2], ))
mdb.models[CUModel].parts['plate1'].Set(name='Ref1', referencePoints=(
    mdb.models[CUModel].parts['plate1'].referencePoints[2], ))
mdb.models[CUModel].parts['plate1'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models[CUModel].parts['plate1'].sets['Ref1'])

##Create rigid plate2
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[CUModel].sketches['__profile__'].Line(
    point1=(-5.0, h2-h1), 
    point2=(35.0, h2-h1))
mdb.models[CUModel].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[CUModel].sketches['__profile__'].geometry[2])
mdb.models[CUModel].sketches['__profile__'].ArcByCenterEnds(
    center=(35.0, h2-h1-5.0), direction=COUNTERCLOCKWISE, point1=(40.0, h2-h1-5.0), point2=(35.0, h2-h1))
mdb.models[CUModel].Part(dimensionality=THREE_D, name='plate2', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[CUModel].parts['plate2'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']


mdb.models[CUModel].parts['plate2'].ReferencePoint(point=
    mdb.models[CUModel].parts['plate2'].InterestingPoint(
    mdb.models[CUModel].parts['plate2'].edges.findAt((2.5, h2-h1, 90.0), ), 
    MIDDLE))
mdb.models[CUModel].parts['plate2'].features.changeKey(fromName='RP', toName=
    'Ref2')
mdb.models[CUModel].parts['plate2'].Set(name='Ref2', referencePoints=(
    mdb.models[CUModel].parts['plate2'].referencePoints[2], ))
mdb.models[CUModel].parts['plate2'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models[CUModel].parts['plate2'].sets['Ref2'])

##Create rigid plate3
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[CUModel].sketches['__profile__'].Line(point1=(-5.0, h2+t*k), point2=
    (5.0, h2+t*k))
mdb.models[CUModel].sketches['__profile__'].geometry.findAt((0.0, h2+t*k))
mdb.models[CUModel].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models[CUModel].sketches['__profile__'].geometry.findAt((0.0, h2+t*k), 
    ))
mdb.models[CUModel].Part(dimensionality=THREE_D, name='plate3', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[CUModel].parts['plate3'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']

mdb.models[CUModel].parts['plate3'].ReferencePoint(point=(0.0, 0.0, 90.0))
mdb.models[CUModel].parts['plate3'].features.changeKey(fromName='RP', toName=
    'Ref3')
mdb.models[CUModel].parts['plate3'].Set(name='Ref3', referencePoints=(
    mdb.models[CUModel].parts['plate3'].referencePoints[2], ))
mdb.models[CUModel].parts['plate3'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models[CUModel].parts['plate3'].sets['Ref3'])

##Creat rigid Center Roller
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models[CUModel].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 80.0))
mdb.models[CUModel].Part(dimensionality=THREE_D, name='C_Roller', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[CUModel].parts['C_Roller'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']

mdb.models[CUModel].parts['C_Roller'].ReferencePoint(point=
    mdb.models[CUModel].parts['C_Roller'].InterestingPoint(
    mdb.models[CUModel].parts['C_Roller'].edges.findAt((80.0, 0.0, 90.0), ), 
    CENTER))
mdb.models[CUModel].parts['C_Roller'].features.changeKey(fromName='RP', 
    toName='Ref4')
mdb.models[CUModel].parts['C_Roller'].Set(name='Ref4', referencePoints=(
    mdb.models[CUModel].parts['C_Roller'].referencePoints[2], ))
mdb.models[CUModel].parts['C_Roller'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models[CUModel].parts['C_Roller'].sets['Ref4'])


##Creat Constraint shaft
mdb.models[CUModel].ConstrainedSketch(name='__profile__', sheetSize=300.0)
mdb.models[CUModel].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 89.0), point1=(0.0, 84.0))
mdb.models[CUModel].Part(dimensionality=THREE_D, name='Cst_shaft', type=
    DISCRETE_RIGID_SURFACE)
mdb.models[CUModel].parts['Cst_shaft'].BaseShellExtrude(depth=90.0, sketch=
    mdb.models[CUModel].sketches['__profile__'])
del mdb.models[CUModel].sketches['__profile__']

mdb.models[CUModel].parts['Cst_shaft'].ReferencePoint(point=
    mdb.models[CUModel].parts['Cst_shaft'].InterestingPoint(
    mdb.models[CUModel].parts['Cst_shaft'].edges.findAt((-5.0, 89.0, 90.0), 
    ), CENTER))
mdb.models[CUModel].parts['Cst_shaft'].features.changeKey(fromName='RP', 
    toName='Ref5')
mdb.models[CUModel].parts['Cst_shaft'].Set(name='Ref5', referencePoints=(
    mdb.models[CUModel].parts['Cst_shaft'].referencePoints[2], ))
mdb.models[CUModel].parts['Cst_shaft'].engineeringFeatures.PointMassInertia(
    alpha=0.0, composite=0.0, mass=0.0001, name='Inertia-1', region=
    mdb.models[CUModel].parts['Cst_shaft'].sets['Ref5'])

##set DCB_single_ply and DCB_double_ply
mdb.models[CUModel].parts['DCB'].Set(faces=
    mdb.models[CUModel].parts['DCB'].faces.findAt(
    ((0.0, R1*(1-cos(Theta))+R2*(1-cos(Theta)), 0.0), ), 
    ((R2*sin(Theta*0.5)+L2/2.0, R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), 0.0), ), 
    ((R1*sin(Theta)+R2*sin(Theta)+L2/2.0-R1*sin(Theta*0.5), R1*(1-cos(Theta*0.5)), 0.0), ), 
    ((R1*sin(Theta)+R2*sin(Theta)+L2/2.0-R1*sin(Theta*0.5), -R1*(1-cos(Theta*0.5)), 0.0), ), 
    ((R2*sin(Theta*0.5)+L2/2.0, -R1*(1-cos(Theta))-R2*(1-cos(Theta))+R2*(1-cos(Theta*0.5)), 0.0), ), 
    ((0.0, -R1*(1-cos(Theta))-R2*(1-cos(Theta)), 0.0), ), 
    ((0.0, R1*(1-cos(Theta))+R2*(1-cos(Theta)), l), ), 
    ((R2*sin(Theta*0.5)+L2/2.0, R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), l), ), 
    ((R1*sin(Theta)+R2*sin(Theta)+L2/2.0-R1*sin(Theta*0.5), R1*(1-cos(Theta*0.5)), l), ),
     ), name='DCB_single')
mdb.models[CUModel].parts['DCB'].Set(faces=
    mdb.models[CUModel].parts['DCB'].faces.findAt(
    ((L1/2.0+R1*sin(Theta)+R2*sin(Theta)+L2/2.0, 0.0, 0.0), ), 
    ((L1/2.0+R1*sin(Theta)+R2*sin(Theta)+L2/2.0, 0.0, l), ), 
    ), name='DCB_doub')

##create material
mdb.models[CUModel].Material(name='Composite_material')
# mdb.models[CUModel].materials['Composite_material'].Elastic(
#     table=((80080.0, 6670.0, 0.34, 2930.0, 2930.0, 2500.0), ), type=LAMINA)
mdb.models[CUModel].materials['Composite_material'].Elastic(table=(
    (80.08E3, 6.67E3, 6.67E3, 0.34, 0.34, 0.20, 2.93E3, 2.93E3, 2.50E3, 0.0), 
    (67.95E3, 3.12E3, 3.12E3, 0.36, 0.36, 0.20, 2.59E3, 2.59E3, 2.00E3, 1.0),
    (84.25E3, 7.02E3, 7.02E3, 0.30, 0.30, 0.20, 4.26E3, 4.26E3, 3.00E3, 2.0),), type=
    ENGINEERING_CONSTANTS, temperatureDependency=ON)

mdb.models[CUModel].materials['Composite_material'].Density(table=((1.6e-09, 
    ), ))

mdb.models[CUModel].CompositeShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, 
    layup=(SectionLayer(thickness=t, orientAngle=45.0, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=t, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=45.0, material='Composite_material')), 
    name='Section-1', 
    poissonDefinition=DEFAULT, preIntegrate=OFF, symmetric=False, temperature=GRADIENT, 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
mdb.models[CUModel].parts['DCB'].SectionAssignment(
    offset=0.0, 
    offsetField='', 
    offsetType=MIDDLE_SURFACE, 
    region=mdb.models[CUModel].parts['DCB'].sets['DCB_single'], 
    sectionName='Section-1', 
    thicknessAssignment=FROM_SECTION)

mdb.models[CUModel].CompositeShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, 
    layup=(SectionLayer(thickness=t, orientAngle=45.0, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=t, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=-45.0, material='Composite_material'), 
           SectionLayer(thickness=t, orientAngle=45.0, material='Composite_material')), 
    name='Section-2', 
    poissonDefinition=DEFAULT, preIntegrate=OFF, symmetric=True, temperature=GRADIENT, 
    thicknessModulus=None, thicknessType=UNIFORM, useDensity=OFF)
mdb.models[CUModel].parts['DCB'].SectionAssignment(
    offset=0.0, 
    offsetField='', 
    offsetType=MIDDLE_SURFACE, 
    region=mdb.models[CUModel].parts['DCB'].sets['DCB_doub'], 
    sectionName='Section-2', 
    thicknessAssignment=FROM_SECTION)

##change the direction of the composite material
mdb.models[CUModel].parts['DCB'].MaterialOrientation(additionalRotationType=
    ROTATION_NONE, axis=AXIS_2, fieldName='', localCsys=None, orientationType=
    GLOBAL, region=mdb.models[CUModel].parts['DCB'].sets['DCB_single'])
mdb.models[CUModel].parts['DCB'].MaterialOrientation(additionalRotationType=
    ROTATION_NONE, axis=AXIS_2, fieldName='', localCsys=None, orientationType=
    GLOBAL, region=mdb.models[CUModel].parts['DCB'].sets['DCB_doub'])


##Assmebly##
mdb.models[CUModel].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='C_Roller-1', 
    part=mdb.models[CUModel].parts['C_Roller'])
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='Cst_shaft-1', 
    part=mdb.models[CUModel].parts['Cst_shaft'])
mdb.models[CUModel].rootAssembly.rotate(angle=10.0, axisDirection=(0.0, 0.0, 
    -1.0), axisPoint=(0.0, 0.0, 1.0), instanceList=('Cst_shaft-1', ))
mdb.models[CUModel].rootAssembly.RadialInstancePattern(axis=(0.0, 0.0, 1.0), 
    instanceList=('Cst_shaft-1', ), number=11, point=(0.0, 0.0, 0.0), 
    totalAngle=360.0)
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='DCB-1', part=
    mdb.models[CUModel].parts['DCB'])
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='plate1-1', 
    part=mdb.models[CUModel].parts['plate1'])
mdb.models[CUModel].rootAssembly.rotate(angle=90.0, axisDirection=(0.0, 10.0, 
    0.0), axisPoint=(0.0, 0.0, 0.0), instanceList=('DCB-1', ))
mdb.models[CUModel].rootAssembly.translate(instanceList=('DCB-1', ), 
    vector=(-5.0, h2, 90.0))
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='plate2-1', 
    part=mdb.models[CUModel].parts['plate2'])
mdb.models[CUModel].rootAssembly.Instance(dependent=ON, name='plate3-1', 
    part=mdb.models[CUModel].parts['plate3'])


mdb.models[CUModel].rootAssembly.Set(name='Ref5', referencePoints=((
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-2'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-3'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-4'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-5'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-6'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-7'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-8'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-9'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-10'].referencePoints[2], 
    ), (
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-11'].referencePoints[2], 
    )))



VirtualNodes(mdb, CUModel, 'center1', 1995.0, h2, 90.0)    
#Ref6
VirtualNodes(mdb, CUModel, 'center2', -5.0, h2, 90.0)      
#center

mdb.models[CUModel].rootAssembly.Set(edges=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].edges.findAt(
    ((l-10.0, h2-R1*(1-cos(Theta))-R2*(1-cos(Theta)), 90.0), ), 
    ((0.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta)), 90.0), ),
    ((l-10.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta)), 90.0), ), 
    ), name='plane_symmetry')

mdb.models[CUModel].rootAssembly.Set(edges=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].edges.findAt(
    ((l-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), )), name='line')

##mesh##
mdb.models[CUModel].parts['plate1'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=10.0)
mdb.models[CUModel].parts['plate1'].generateMesh()
mdb.models[CUModel].parts['plate1'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models[CUModel].parts['plate1'].faces, ))
mdb.models[CUModel].parts['plate2'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=10.0)
mdb.models[CUModel].parts['plate2'].generateMesh()
mdb.models[CUModel].parts['plate2'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models[CUModel].parts['plate2'].faces, ))
mdb.models[CUModel].parts['plate3'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=4.0)
mdb.models[CUModel].parts['plate3'].generateMesh()
mdb.models[CUModel].parts['plate3'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models[CUModel].parts['plate3'].faces, ))
mdb.models[CUModel].parts['C_Roller'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=8)
mdb.models[CUModel].parts['C_Roller'].generateMesh()
mdb.models[CUModel].parts['C_Roller'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models[CUModel].parts['C_Roller'].faces, ))
mdb.models[CUModel].parts['Cst_shaft'].seedPart(deviationFactor=0.1, 
    minSizeFactor=0.1, size=3.0)
mdb.models[CUModel].parts['Cst_shaft'].generateMesh()
mdb.models[CUModel].parts['Cst_shaft'].setElementType(elemTypes=(ElemType(
    elemCode=R3D4, elemLibrary=EXPLICIT), ElemType(elemCode=R3D3, 
    elemLibrary=EXPLICIT)), regions=(
    mdb.models[CUModel].parts['Cst_shaft'].faces, ))

mdb.models[CUModel].parts['DCB'].seedPart(deviationFactor=0.1, minSizeFactor=
    0.1, size=5.0)
mdb.models[CUModel].parts['DCB'].generateMesh()
mdb.models[CUModel].parts['DCB'].setElementType(elemTypes=(ElemType(
    elemCode=S4R, elemLibrary=EXPLICIT, secondOrderAccuracy=OFF, 
    hourglassControl=STIFFNESS), ElemType(elemCode=S3R, elemLibrary=EXPLICIT)), 
    regions=(mdb.models[CUModel].parts['DCB'].faces, ))

mdb.models['CoilingandUnfoldModel'].rootAssembly.regenerate()

DCB_section1 = mdb.models[CUModel].rootAssembly.instances['DCB-1'].nodes.getByBoundingBox(1994.9999, h2-200.0, 90.0-200.0, 1995.0001, h2+200.0, 90.0+200.0) 
mdb.models[CUModel].rootAssembly.Set(name='DCB_section1', nodes=DCB_section1)
DCB_section2 = mdb.models[CUModel].rootAssembly.instances['DCB-1'].nodes.getByBoundingBox(-5.0001, h2-200.0, 90.0-200.0, -4.9999, h2+200.0, 90.0+200.0) 
mdb.models[CUModel].rootAssembly.Set(name='DCB_section2', nodes=DCB_section2)


mdb.models[CUModel].Coupling(controlPoint=
    mdb.models[CUModel].rootAssembly.sets['center1'], couplingType=STRUCTURAL, 
    influenceRadius=WHOLE_SURFACE, localCsys=None, name='center1_with_DCBsection1', 
    surface=mdb.models[CUModel].rootAssembly.sets['DCB_section1'], u1=ON, u2=
    ON, u3=ON, ur1=ON, ur2=ON, ur3=ON)
mdb.models[CUModel].Coupling(controlPoint=
    mdb.models[CUModel].rootAssembly.sets['center2'], couplingType=STRUCTURAL, 
    influenceRadius=WHOLE_SURFACE, localCsys=None, name='center2_with_DCBsection2', 
    surface=mdb.models[CUModel].rootAssembly.sets['DCB_section2'], u1=ON, u2=ON, u3=
    ON, ur1=ON, ur2=ON, ur3=ON, weightingMethod=UNIFORM)



##create surface for the model
mdb.models[CUModel].rootAssembly.Surface(name='plate1_bottom', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['plate1-1'].faces)
mdb.models[CUModel].rootAssembly.Surface(name='plate2_top', side2Faces=
    mdb.models[CUModel].rootAssembly.instances['plate2-1'].faces)
mdb.models[CUModel].rootAssembly.Surface(name='plate3_bottom', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['plate3-1'].faces)
mdb.models[CUModel].rootAssembly.Surface(name='Roller_surface', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['C_Roller-1'].faces)
mdb.models[CUModel].rootAssembly.Surface(name='shafts_surface', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-2'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-3'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-4'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-5'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-6'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-7'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-8'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-9'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-10'].faces+\
    mdb.models[CUModel].rootAssembly.instances['Cst_shaft-1-rad-11'].faces)

mdb.models[CUModel].rootAssembly.Surface(name='DCB', side12Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces)
mdb.models[CUModel].rootAssembly.Surface(name='DCB_smalltop', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces.findAt(
    ((-5.0, h2+R1*(1-cos(Theta*0.5)), 90.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0+R1*sin(Theta*0.5)), ), 
    ((-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), 90.0-R2*sin(Theta*0.5)-L2/2.0), ),  
    ((-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta)), 90.0-L2/4.0), ), )
    , side2Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces.findAt(
    ((-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), ),))
mdb.models[CUModel].rootAssembly.Surface(name='DCB_top', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces.findAt(
    ((l-5.0, h2+R1*(1-cos(Theta*0.5)), 90.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0+R1*sin(Theta*0.5)), ), 
    ((l-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), 90.0-R2*sin(Theta*0.5)-L2/2.0), ), 
    ((l-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta)), 90.0-L2/4.0), ), 
    ((-5.0, h2+R1*(1-cos(Theta*0.5)), 90.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0+R1*sin(Theta*0.5)), ), 
    ((-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta))-R2*(1-cos(Theta*0.5)), 90.0-R2*sin(Theta*0.5)-L2/2.0), ), 
    ((-5.0, h2+R1*(1-cos(Theta))+R2*(1-cos(Theta)), 90.0-L2/4.0), ), )
    , side2Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces.findAt(
    ((l-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), ),
    ((-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), ),))
mdb.models[CUModel].rootAssembly.Surface(name='DCB_bottom', side1Faces=
    mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces.findAt(
    ((-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), ),
    ((l-5.0, h2, 90.0-L1/2.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0), ),
    ((-5.0, h2-R1*(1-cos(Theta))-R2*(1-cos(Theta)), 90.0-L2/4.0), ), 
    ((-5.0, h2-R1*(1-cos(Theta))-R2*(1-cos(Theta))+R2*(1-cos(Theta*0.5)), 90.0-R2*sin(Theta*0.5)-L2/2.0), ), 
    ((-5.0, h2-R1*(1-cos(Theta*0.5)), 90.0-R1*sin(Theta)-R2*sin(Theta)-L2/2.0+R1*sin(Theta*0.5)), ), ))


##Step##
mdb.models[CUModel].ExplicitDynamicsStep(description='Compress-the-DCB', 
    improvedDtMethod=ON, name='Flatten', previous='Initial', timePeriod=
    1.0)
mdb.models[CUModel].ExplicitDynamicsStep(description='change-the-contact', 
    improvedDtMethod=ON, name='New_contact', previous='Flatten', timePeriod=
    0.5)
mdb.models[CUModel].ExplicitDynamicsStep(description='Coiling-deformation', 
    improvedDtMethod=ON, name='Coiling', previous='New_contact', timePeriod=
    4.0)
mdb.models[CUModel].ExplicitDynamicsStep(description='change-the-material-properties', 
    improvedDtMethod=ON, name='New_material', previous='Coiling', timePeriod=
    0.5)
mdb.models[CUModel].ExplicitDynamicsStep(description='unfold_freely', 
    improvedDtMethod=ON, name='free_unfold', previous='New_material', timePeriod=
    20.0)

mdb.models[CUModel].fieldOutputRequests['F-Output-1'].setValues(
    timeInterval=0.01)
mdb.models[CUModel].historyOutputRequests['H-Output-1'].setValues(
    timeInterval=0.01)

mdb.models[CUModel].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'SVAVG', 'PE', 'PEVAVG', 'PEEQ', 'PEEQVAVG', 'LE', 'U', 'V', 'A', 
    'RF', 'CSTRESS', 'EVF', 'COORD'))


#change parameters of the material
mdb.models[CUModel].rootAssembly.Set(faces=mdb.models[CUModel].rootAssembly.instances['DCB-1'].faces, name='Set-All')
mdb.models[CUModel].Temperature(createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(0.0, ), name='Predefined Field-1', region=
    mdb.models[CUModel].rootAssembly.sets['Set-All'])
mdb.models[CUModel].predefinedFields['Predefined Field-1'].setValuesInStep(
    magnitudes=(1.0, ), stepName='New_material')


##Interaction##
mdb.models[CUModel].ContactProperty('IntProp-1-nofric')
mdb.models[CUModel].interactionProperties['IntProp-1-nofric'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models[CUModel].interactionProperties['IntProp-1-nofric'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models[CUModel].ContactProperty('IntProp-2-fric')
mdb.models[CUModel].interactionProperties['IntProp-2-fric'].TangentialBehavior(
    dependencies=0, directionality=ISOTROPIC, elasticSlipStiffness=None, 
    formulation=PENALTY, fraction=0.005, maximumElasticSlip=FRACTION, 
    pressureDependency=OFF, shearStressLimit=None, slipRateDependency=OFF, 
    table=((0.1, ), ), temperatureDependency=OFF)
mdb.models[CUModel].interactionProperties['IntProp-2-fric'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models[CUModel].ContactProperty('IntProp-3-cling')
mdb.models[CUModel].interactionProperties['IntProp-3-cling'].TangentialBehavior(
    formulation=ROUGH)
mdb.models[CUModel].interactionProperties['IntProp-3-cling'].NormalBehavior(
    allowSeparation=OFF, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)

mdb.models[CUModel].ContactExp(createStepName='Initial', name='Int-1')
mdb.models[CUModel].interactions['Int-1'].includedPairs.setValuesInStep(
    addPairs=((mdb.models[CUModel].rootAssembly.surfaces['DCB'], SELF), (
    mdb.models[CUModel].rootAssembly.surfaces['plate1_bottom'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB']), (
    mdb.models[CUModel].rootAssembly.surfaces['plate2_top'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB'])), stepName='Initial', 
    useAllstar=OFF)
mdb.models[CUModel].interactions['Int-1'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1-nofric'), (
    mdb.models[CUModel].rootAssembly.surfaces['plate1_bottom'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB'], 'IntProp-2-fric'), (
    mdb.models[CUModel].rootAssembly.surfaces['plate2_top'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB'], 'IntProp-2-fric')), 
    stepName='Initial')
mdb.models[CUModel].interactions['Int-1'].deactivate('New_contact')
mdb.models[CUModel].ContactExp(createStepName='New_contact', name='Int-2')
mdb.models[CUModel].interactions['Int-2'].includedPairs.setValuesInStep(
    addPairs=((mdb.models[CUModel].rootAssembly.surfaces['DCB'], SELF), (
    mdb.models[CUModel].rootAssembly.surfaces['Roller_surface'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB']), (
    mdb.models[CUModel].rootAssembly.surfaces['shafts_surface'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB']), (
    mdb.models[CUModel].rootAssembly.surfaces['plate3_bottom'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB_smalltop'])), stepName=
    'New_contact', useAllstar=OFF)
mdb.models[CUModel].interactions['Int-2'].contactPropertyAssignments.appendInStep(
    assignments=((GLOBAL, SELF, 'IntProp-1-nofric'), (
    mdb.models[CUModel].rootAssembly.surfaces['plate3_bottom'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB_smalltop'], 
    'IntProp-3-cling')), stepName='New_contact')
mdb.models[CUModel].interactions['Int-2'].includedPairs.setValuesInStep(
    removePairs=((
    mdb.models[CUModel].rootAssembly.surfaces['shafts_surface'], 
    mdb.models[CUModel].rootAssembly.surfaces['DCB']), ), stepName=
    'free_unfold')


##create load##
mdb.models[CUModel].SmoothStepAmplitude(data=((0.0, 0.0), (1.0, 1.0)), name=
    'Smooth1', timeSpan=STEP)
mdb.models[CUModel].SmoothStepAmplitude(data=((0.0, 0.0), (4.0, 1.0)), name=
    'Smooth2', timeSpan=STEP)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate1', 
    region=mdb.models[CUModel].rootAssembly.sets['plate1-1.Ref1'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models[CUModel].boundaryConditions['BC-plate1'].setValuesInStep(
    amplitude='Smooth1', stepName='Flatten', u2=-(h1-t*k))
mdb.models[CUModel].boundaryConditions['BC-plate1'].setValuesInStep(stepName=
    'New_contact', u2=0.0)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate2', 
    region=mdb.models[CUModel].rootAssembly.sets['plate2-1.Ref2'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models[CUModel].boundaryConditions['BC-plate2'].setValuesInStep(
    amplitude='Smooth1', stepName='Flatten', u2=h1-t*k)
mdb.models[CUModel].boundaryConditions['BC-plate2'].setValuesInStep(stepName=
    'New_contact', u2=0.0)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-plate3', 
    region=mdb.models[CUModel].rootAssembly.sets['plate3-1.Ref3'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models[CUModel].boundaryConditions['BC-plate3'].setValuesInStep(
    amplitude='Smooth2', stepName='Coiling', ur3=24.0)
mdb.models[CUModel].boundaryConditions['BC-plate3'].setValuesInStep(stepName=
    'New_material', ur3=0.0)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-Roller', 
    region=mdb.models[CUModel].rootAssembly.sets['C_Roller-1.Ref4'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)
mdb.models[CUModel].boundaryConditions['BC-Roller'].setValuesInStep(
    amplitude='Smooth2', stepName='Coiling', ur3=24.0)
mdb.models[CUModel].boundaryConditions['BC-Roller'].setValuesInStep(stepName=
    'New_material', ur3=0.0)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-shafts', 
    region=mdb.models[CUModel].rootAssembly.sets['Ref5'], u1=SET, u2=SET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'BC-DCBsection2', region=mdb.models[CUModel].rootAssembly.sets['center2'], 
    u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[CUModel].boundaryConditions['BC-DCBsection2'].deactivate(
    'New_contact')

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='New_material', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name=
    'BC-DCBsection1', region=mdb.models[CUModel].rootAssembly.sets['center1'], 
    u1=SET, u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[CUModel].boundaryConditions['BC-DCBsection1'].deactivate(
    'free_unfold')

mdb.models[CUModel].Pressure(amplitude=UNSET, createStepName='free_unfold', 
    distributionType=VISCOUS, field='', magnitude=visc, name=
    'viscous_pressure_DCBtop', region=
    mdb.models[CUModel].rootAssembly.surfaces['DCB_top'])
mdb.models[CUModel].Pressure(amplitude=UNSET, createStepName='free_unfold', 
    distributionType=VISCOUS, field='', magnitude=visc, name=
    'viscous_pressure_bottom', region=
    mdb.models[CUModel].rootAssembly.surfaces['DCB_bottom'])


mdb.models[CUModel].ZsymmBC(createStepName='Initial', localCsys=None, name=
    'BC-symplane', region=
    mdb.models[CUModel].rootAssembly.sets['plane_symmetry'])

mdb.models[CUModel].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-line', 
    region=mdb.models[CUModel].rootAssembly.sets['line'], u1=UNSET, u2=SET, 
    u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models[CUModel].boundaryConditions['BC-line'].deactivate('free_unfold')

#Job##
if not os.path.exists('FEModelFiles'):
    os.mkdir('FEModelFiles')
os.chdir('FEModelFiles')
jobName = 'halfDCB_coiling_and_free_unfold_2m_T1'
mdb.Job(model=CUModel, name=jobName, explicitPrecision=DOUBLE_PLUS_PACK, numCpus=64, numDomains=64)
mdb.saveAs(pathName=jobName)
mdb.jobs[jobName].submit()
mdb.jobs[jobName].waitForCompletion()
