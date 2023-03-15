"""
@author: Eduardo Becker Groth
ROUTINE FOR MODELLING TAPE WITH RANDOM THROUGHT DEFECTS 
MAIN GOAL: GENERATE THE SIGNALS TO TEST MACHINE LEARNING SCRIPTS TO APLIIED AT ACOUTIC SIGNALS 
model: rectangular strip
"""

from abaqus import *
from abaqusConstants import *
from numpy.random import random
import __main__

import section
import regionToolset
import displayGroupMdbToolset as dgm
import part
import material
import assembly
import step
import interaction
import load
import mesh
import optimization
import job
import sketch
import visualization
import xyPlot
import displayGroupOdbToolset as dgo
import connectorBehavior
import csv
import numpy as np


f = open("folder.txt")
folder = f.read()


##### PARAMETERS #####################################################################


csv_file_name="tb.csv"
tb=[]
with open(csv_file_name) as f:
    reader = csv.reader(f)
    for row in reader:
        tb.append(row)

 
tone_burst=np.zeros((np.size(tb,1),np.size(tb,0)))
for i in range(np.size(tb,0)):
    for j in range(np.size(tb,1)):
        tone_burst[j][i]=float(tb[i][j])
        
            
parameters=[]
with open('parameters.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        for i in range(len(row)):   
            parameters.append(float(row[i]))

t_tot = parameters[0]                    # total time of simulation
time_interval_monitoring = parameters[1] # acquire step of monitoring signal(s) 
time_interval_history = parameters[2]    # acquire step of default history data storage 
time_interval_field = parameters[3]      # acquire step of defauld field data storage (use to do .gif and pictures)
pm_u1 = parameters[4]                    # initial excitation motion amplitud in x direction
pm_u2 = parameters[5]                    # initial excitation motion apmlitud in y direction 
size_defect = parameters[6]              # defect size
number_defect = parameters[7]            # number of defects in the model

                
########## START THE MODEL ###################################################                  




s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=1.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints

######## GEOMETRY ###########
p = mdb.models['Model-1'].Part(name='placa', dimensionality=TWO_D_PLANAR,type=DEFORMABLE_BODY)
p = mdb.models['Model-1'].parts['placa']
s.rectangle(point1=(-10e-3,-5e-3), point2=(1.2,10e-3)) # strip
c=size_defect    #defect size
a1=0.5
b1=0.5
j=0;
while j<=number_defect:
    a=random()*0.8
    b=random()*5e-3  
    if abs(a-a1)>(2*c+1e-3) and abs(b-b1)>(2*c+1e-3): 
           a1=a
           b1=b 
           s.CircleByCenterPerimeter(center=(a, b), point1=(c+a, b))
           j=j+1
    else :
        a1=a1
        b1=b1
    
        
p.BaseShell(sketch=s)
s.unsetPrimaryObject()

#### PARTITION (separet the model for to do a zone at the end of the model that have rectagular mesh for choose nodes to monitoring)
p = mdb.models['Model-1'].parts['placa']
mdb.models['Model-1'].sketches['__profile__']
p = mdb.models['Model-1'].parts['placa']
f, e, d = p.faces, p.edges, p.datums
t = p.MakeSketchTransform(sketchPlane=f[0], sketchPlaneSide=SIDE1, origin=(0, 0, 0.0))
s = mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=2.42, gridSpacing=0.06)
g, v, d1, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=SUPERIMPOSE)
p = mdb.models['Model-1'].parts['placa']
p.projectReferencesOntoSketch(sketch=s, filter=COPLANAR_EDGES)
s.Line(point1=(1.1, -5e-3), point2=(1.1, 10e-3))
f = p.faces
pickedFaces = f.getSequenceFromMask(mask=('[#1 ]', ), )
e1, d2 = p.edges, p.datums
p.PartitionFaceBySketch(faces=pickedFaces, sketch=s)
s.unsetPrimaryObject()
del mdb.models['Model-1'].sketches['__profile__']

################## MESH
p = mdb.models['Model-1'].parts['placa']
p.seedPart(size=1e-3, deviationFactor=0.1, minSizeFactor=0.1)
p = mdb.models['Model-1'].parts['placa']
p.generateMesh()

#################### SECTION
mdb.models['Model-1'].HomogeneousSolidSection(name='Section-1', material='STEEL', thickness=5e-3)
p = mdb.models['Model-1'].parts['placa']

f = p.faces
region = p.Set(faces=f, name='whole')
p = mdb.models['Model-1'].parts['placa']
p.SectionAssignment(region=region, sectionName='Section-1', offset=0.0, offsetType=MIDDLE_SURFACE, offsetField='',thicknessAssignment=FROM_SECTION)

### sets
p = mdb.models['Model-1'].parts['placa']
n = p.nodes
nodes = n.getByBoundingBox(-11e-3,-6e-3,0 ,-9.9e-3,11e-3 ,0)
p.Set(nodes=nodes, name='load')


p = mdb.models['Model-1'].parts['placa']
n = p.nodes
nodes = n.getByBoundingBox(1.1999, -6e-3,0 ,1.21,11e-3,0)
p.Set(nodes=nodes, name='encraste')


############ MATERIAL 
mdb.models['Model-1'].Material(name='STEEL')
mdb.models['Model-1'].materials['STEEL'].Density(table=((7860.0, ), ))
mdb.models['Model-1'].materials['STEEL'].Elastic(table=((210000000000, 0.3), ))
    
############# STEP
a = mdb.models['Model-1'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON, optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
mdb.models['Model-1'].ExplicitDynamicsStep(name='Step-1', previous='Initial', timePeriod=t_tot)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(step='Step-1')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=EVERY_TIME_INCREMENT)

############# HISTORY    
p = mdb.models['Model-1'].parts['placa']
n = p.nodes
nodes = n.getByBoundingBox(1.15,2.5e-3-0.5e-3, 0,1.15+1.2e-3,2.5e-3+0.5e-3, 0)
p.Set(nodes=nodes, name='monitoring')

a = mdb.models['Model-1'].rootAssembly
a.regenerate()
session.viewports['Viewport: 1'].setValues(displayedObject=a)

a1 = mdb.models['Model-1'].rootAssembly
p = mdb.models['Model-1'].parts['placa']
a1.Instance(name='placa-1', part=p, dependent=ON)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(adaptiveMeshConstraints=ON)

regionDef=mdb.models['Model-1'].rootAssembly.allInstances['placa-1'].sets['monitoring']

mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(timeInterval=time_interval_field, timeMarks=ON)
    
mdb.models['Model-1'].historyOutputRequests['H-Output-1'].setValues(timeInterval=time_interval_history)
    

mdb.models['Model-1'].HistoryOutputRequest(name='monitormanento',createStepName='Step-1', variables=('U1', 'U2', 'U3', 'UR1', 'UR2','UR3'), 
                                           timeInterval=time_interval_monitoring, region=regionDef, sectionPoints=DEFAULT,rebar=EXCLUDE)
########### TONE BURST 
mdb.models['Model-1'].TabularAmplitude(name='Amp-1', timeSpan=STEP, smooth=SOLVER_DEFAULT,data=tone_burst)

############ LOAD** (precribed motion)
region = a.instances['placa-1'].sets['load']

#prescribed motion 
mdb.models['Model-1'].DisplacementBC(name='BC-2', createStepName='Step-1', region=region, 
                                     u1=pm_u1, u2=pm_u2, ur3=0, amplitude='Amp-1', fixed=OFF, distributionType=UNIFORM, fieldName='', localCsys=None)
a = mdb.models['Model-1'].rootAssembly

########### Bondary Ccondition 

region = a.instances['placa-1'].sets['encraste']
mdb.models['Model-1'].EncastreBC(name='BC-1', createStepName='Step-1',region=region, localCsys=None)

a = mdb.models['Model-1'].rootAssembly
node=a.instances['placa-1'].sets['monitoring'].nodes[0].label


########### JOB
os.chdir(folder)

mdb.Job(name='tira', model='Model-1', description='', type=ANALYSIS, 
    atTime=None, waitMinutes=0, waitHours=0, queue=None, memory=90, 
    memoryUnits=PERCENTAGE, explicitPrecision=SINGLE, 
    nodalOutputPrecision=SINGLE, echoPrint=OFF, modelPrint=OFF, 
    contactPrint=OFF, historyPrint=OFF, userSubroutine='', 
    scratch=folder, 
    resultsFormat=ODB, parallelizationMethodExplicit=DOMAIN, numDomains=1, 
    activateLoadBalancing=False, multiprocessingMode=DEFAULT, numCpus=1)

mdb.jobs['tira'].submit(consistencyChecking=OFF)
mdb.jobs['tira'].waitForCompletion()


jobname = 'tira.odb'       ###  extract results from .odb file 
o1 = session.openOdb(name=jobname)
session.viewports['Viewport: 1'].setValues(displayedObject=o1)
odb = session.odbs[jobname]

xy1 = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Spatial displacement: U1 at Node %s in NSET MONITORING' %(node), suppressQuery=True)
c1 = session.Curve(xyData=xy1)
xy2 = xyPlot.XYDataFromHistory(odb=odb, outputVariableName='Spatial displacement: U2 at Node %s in NSET MONITORING' %(node), suppressQuery=False)
c2 = session.Curve(xyData=xy2)
xyp = session.XYPlot('XYPlot-1')
chartName = xyp.charts.keys()[0]
chart = xyp.charts[chartName]
chart.setValues(curvesToPlot=(c1, c2, ), )
session.viewports['Viewport: 1'].setValues(displayedObject=xyp)
x0 = session.xyDataObjects['_temp_1']
x1 = session.xyDataObjects['_temp_2']
session.writeXYReport(fileName='u0.txt', xyData=(x0, x1))

