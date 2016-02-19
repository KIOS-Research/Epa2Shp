import shapefile
import yaml, os
import epamodule as d

f = open("arguments.yaml", "r")
cfg = yaml.load(f)

arg=[]
for section in cfg:
    arg.append(cfg[section])

inpname= "%s" % arg[0]
Home = os. getcwd ()

newpath = Home + '\\results'
if not os.path.exists(newpath):
    os.makedirs(newpath)

d.LoadInpFile('networks/'+inpname+'.inp')

# Write Junction Shapefile
w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('dc_id','C',254)
w.field('elevation','N',20)
w.field('pattern','C',254)
w.field('demand','N',20,9)

xy=d.getNodeCoordinates()

x=xy[0]
y=xy[1]
x1=xy[2]
x2=xy[4]
y1=xy[3]
y2=xy[5]
vertx=xy[6]
verty=xy[7]
vertxy=[]
vertxyFinal=[]
for i in range(len(vertx)):
    for u in range(len(vertx[i])):
        vertxy.append([float(vertx[i][u]),float(verty[i][u])])
        vertxyFinal.append(vertxy[u])

if d.getNodeJunctionsCount()>0:
    ndBaseD=d.getNodeBaseDemands()
    ndEle=d.getNodeElevations()
    ndBaseD=d.getNodeBaseDemands()
    ndID=d.getNodeNameID()
    ndPatIndex=d.getNodeDemandPatternIndex()
    ndPatID=d.getPatternNameID()
    for i in range(0,d.getNodeJunctionsCount()):
        w.point(float(x[i]), float(y[i]))
        w.record(ndID[i],ndEle[i],ndPatID[int(ndPatIndex[i]-1)],ndBaseD[i])
    w.save('results/'+inpname[:len(inpname)-4]+'_junctions')

# Write Pipe Shapefile
wpipe = shapefile.Writer(shapefile.POLYLINE)
wpipe.field('dc_id','C',254)
wpipe.field('node1','C',254)
wpipe.field('node2','C',254)
wpipe.field('length','N',20,9)
wpipe.field('diameter','N',20,9)
wpipe.field('status','C',254)
wpipe.field('roughness','N',20,9)
wpipe.field('minorloss','N',20,9)
wpipe.autoBalance = 1
parts=[];pIndex=[]
pumps = d.getLinkPumpIndex()
for i in range(len(pumps)):
    pIndex.append(pumps[i]-1)
vIndex=[]
valves = d.getLinkValveIndex()
for i in range(len(valves)):
    vIndex.append(valves[i]-1)

ndlConn=d.getNodesConnectingLinksID()
if d.getLinkCount()>0:
    p=0;v=0
    linkInStatus=d.getLinkInitialStatus()
    for i in range(0,d.getLinkCount()):
        if i in pIndex:
            xx= (float(x1[i])+float(x2[i]))/2
            yy= (float(y1[i])+float(y2[i]))/2
            for p in range(0,2):
                XY=[]
                if p==0:
                    linkIDFinal=linkID[i]+'_pump1'
                    node1=ndlConn[i][0][0]
                    node2=linkIDFinal
                    indN1 = d.getNodeIndex(node1)
                    XY.append(([float(x[indN1[0]-1]),float(y[indN1[0]-1])],[xx,yy]))
                elif p==1:
                    linkIDFinal=linkID[i]+'_pump2'
                    node1=linkIDFinal
                    node2=ndlConn[i][1][0]
                    indN2 = d.getNodeIndex(node2)

                    XY.append(([xx,yy],[float(x[indN2[0]-1]),float(y[indN2[0]-1])]))
                stat='CLOSED'
                if linkInStatus[i]==1:
                    stat='OPEN'
                length=0
                diameter=0
                roughness=0
                minorloss=0
                wpipe.line(parts=[XY[0]])
                wpipe.record(linkIDFinal,node1,node2,length,diameter,stat,roughness,minorloss)
        elif i in vIndex:
            xx= (float(x1[i])+float(x2[i]))/2
            yy= (float(y1[i])+float(y2[i]))/2
            for v in range(0,2):
                XY=[]
                if v==0:
                    linkIDFinal=linkID[i]+'_valve1'
                    node1=ndlConn[i][0][0]
                    node2=linkIDFinal
                    indN1 = d.getNodeIndex(node1)
                    XY.append(([float(x[indN1[0]-1]),float(y[indN1[0]-1])],[xx,yy]))
                elif v==1:
                    linkIDFinal=linkID[i]+'_valve2'
                    node1=linkIDFinal
                    node2=ndlConn[i][1][0]
                    indN2 = d.getNodeIndex(node2)

                    XY.append(([xx,yy],[float(x[indN2[0]-1]),float(y[indN2[0]-1])]))
                stat='CLOSED'
                if linkInStatus[i]==1:
                    stat='OPEN'
                length=0
                diameter=0
                roughness=0
                minorloss=0
                wpipe.line(parts=[XY[0]])
                wpipe.record(linkIDFinal,node1,node2,length,diameter,stat,roughness,minorloss)
        else:
            linkID=d.getLinkNameID()
            stat='CLOSED'
            if linkInStatus[i]==1:
                stat='OPEN'
            linkLengths=d.getLinkLength()
            linkDiameters=d.getLinkDiameter()
            linkRough=d.getLinkRoughnessCoeff()
            linkMinorloss=d.getLinkMinorLossCoeff()
            point1 = [float(x1[i]),float(y1[i])]
            point2 = [float(x2[i]),float(y2[i])]
            if vertx[i]!=[]:
                parts.append(point1)
                for mm in range(len(vertxyFinal)):
                    parts.append(vertxyFinal[mm])
                parts.append(point2)
                wpipe.line(parts=[parts])
            else:
                wpipe.line(parts=[[[float(x1[i]),float(y1[i])],[float(x2[i]),float(y2[i])]]])
            wpipe.record(linkID[i],ndlConn[i][0][0],ndlConn[i][1][0],linkLengths[i],linkDiameters[i],stat,linkRough[i],linkMinorloss[i])
    wpipe.save('results/'+inpname[:len(inpname)-4]+'_pipes')

# Write Tank Shapefile
w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('dc_id','C',254)
w.field('elevation','N',20)
w.field('initiallev','N',20)
w.field('minimumlev','N',20)
w.field('maximumlev','N',20)
w.field('diameter','N',20)
w.field('minimumvol','N',20)
w.field('volumecurv','N',20)

if d.getNodeTankCount()>0:
    ndTankelevation=d.getNodeElevations()
    initiallev=d.getNodeTankInitialLevel()
    minimumlev=d.getNodeTankMinimumWaterLevel()
    maximumlev=d.getNodeTankMaximumWaterLevel()
    diameter=d.getNodeTankDiameter()
    minimumvol=d.getNodeTankMinimumWaterVolume()
    volumecurv=d.getNodeTankVolumeCurveIndex()
    ndID=d.getNodeNameID()
    for i, nodetankindex in enumerate(d.getNodeTankIndex()):
        p=nodetankindex-1
        w.point(float(x[p]), float(y[p]))
        w.record(ndID[p],ndTankelevation[p],initiallev[p],minimumlev[p],maximumlev[p],diameter[p],minimumvol[p],volumecurv[p])
    w.save('results/'+inpname[:len(inpname)-4]+'_tanks')


# Write Reservoir Shapefile
w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('dc_id','C',254)
w.field('head','N',20)

if d.getNodeReservoirCount()>0:
    head=d.getNodeElevations()
    ndID=d.getNodeNameID()
    for i, nodereservoirindex in enumerate(d.getNodeReservoirIndex()):
        p=nodereservoirindex-1
        w.point(float(x[p]), float(y[p]))
        w.record(ndID[p],head[p])
    w.save('results/'+inpname[:len(inpname)-4]+'_reservoirs')

# Write Pump Shapefile
w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('dc_id','C',254)
w.field('node1','C',254)
w.field('node2','C',254)
w.field('head','C',254)
w.field('flow','C',254)
w.field('power','N',20,9)
w.field('curveID','C',254)


if d.getLinkPumpCount()>0:
    headc=d.getHeadCurveIndex()
    chPowerPump=d.getLinkPumpPower()
    linkID=d.getLinkNameID();power=[]
    for i, pumpindex in enumerate(d.getLinkPumpIndex()):
        Head=[];Flow=[];Curve=[]
        if d.getCurveCount()>0:
            curveXY = d.getCurvesInfo()
            curveXYF = curveXY[headc[i]-1]

            for i in range(len(curveXYF)):
                Head.append(curveXYF[i][2])
                Flow.append(curveXYF[i][3])
            Curve=curveXYF[0][0]
            p=pumpindex-1
            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            w.point(xx,yy)
            wpipe.line(parts=[[[float(x1[p]),float(y1[p])],[float(x2[p]),float(y2[p])]]])

        else:
            power=chPowerPump[i][1]
            xx= (float(x1[p])+float(x2[p]))/2
            yy= (float(y1[p])+float(y2[p]))/2
            w.point(xx,yy)
            wpipe.line(parts=[[[float(x1[p]),float(y1[p])],[float(x2[p]),float(y2[p])]]])
        if Head==[]:
            Head='NULL'
        if Flow==[]:
            Flow='NULL'
        if Curve==[]:
            Curve='NULL'
        w.record(linkID[p],ndlConn[p][0][0],ndlConn[p][1][0],Head,Flow,power,Curve)
    w.save('results/'+inpname[:len(inpname)-4]+'_pumps')

# Write Valve Shapefile
w = shapefile.Writer(shapefile.POINT)
w.autoBalance = 1
w.field('dc_id','C',254)
w.field('node1','C',254)
w.field('node2','C',254)
w.field('diameter','N',20,9)
w.field('type','C',254)
w.field('setting','N',20,9)
w.field('minorloss','N',20,9)

if d.getLinkValveCount()>0:
    linkID=d.getLinkNameID()
    linkType=d.getLinkType()
    print linkType
    linkDiameter=d.getLinkDiameter()
    linkInitSett=d.getLinkInitialSetting()
    linkMinorloss=d.getLinkMinorLossCoeff()
    for i, valveindex in enumerate(d.getLinkValveIndex()):
        p=valveindex-1
        xx= (float(x1[p])+float(x2[p]))/2
        yy= (float(y1[p])+float(y2[p]))/2
        w.point(xx,yy)
        w.record(linkID[p],ndlConn[p][0][0],ndlConn[p][1][0],linkDiameter[p],linkType[p],linkInitSett[p],linkMinorloss[p])
    w.save('results/'+inpname[:len(inpname)-4]+'_valves')


