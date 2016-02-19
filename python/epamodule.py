#!/usr/bin/env python
"""Python EpanetToolkit interface

not yet implemented:
# epanet20013patch #
-ENgetaveragepatternvalue
-ENgetbasedemand
-ENgetcurve
-ENgetdemandpattern
-ENgetheadcurve
-ENgetnumdemands
-ENgetpumptype
-ENgetqualinfo
-ENgetstatistic
-ENsetbasedemand
#####################

- ENresetreport
- ENsetreport
- ENsetstatusreport
- ENwriteline

- ENsavehydfile
- ENusehydfile

added functions:
+ ENsimtime"""

import ctypes
import platform
import datetime

_plat= platform.system()
if _plat=='Linux':
  _lib = ctypes.CDLL("libepanet.so.2")
elif _plat=='Windows':
  _lib = ctypes.windll.epanet2 # epanet2.dll
else:
  Exception('Platform '+ _plat +' unsupported (not yet)')


_current_simulation_time=  ctypes.c_long()

_max_label_len= 32
_err_max_char= 80





def ENepanet(nomeinp, nomerpt='report.txt', nomebin='', vfunc=None):
    """Runs a complete EPANET simulation.

    Arguments:
    nomeinp: name of the input file
    nomerpt: name of an output report file
    nomebin: name of an optional binary output file
    vfunc  : pointer to a user-supplied function which accepts a character string as its argument."""
    ierr= _lib.ENepanet(ctypes.c_char_p(nomeinp), ctypes.c_char_p(nomerpt), ctypes.c_char_p(nomebin), vfunc)
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopen(nomeinp, nomerpt, nomebin):
    """Opens the Toolkit to analyze a particular distribution system

    Arguments:
    nomeinp: name of the input file
    nomerpt: name of an output report file
    nomebin: name of an optional binary output file
    """
    ierr= _lib.ENopen(ctypes.c_char_p(nomeinp), ctypes.c_char_p(nomerpt), ctypes.c_char_p(nomebin))
    if ierr!=0: raise ENtoolkitError(ierr);
    global inpname; inpname = nomeinp


def ENclose():
  """Closes down the Toolkit system (including all files being processed)"""
  ierr= _lib.ENclose()
  if ierr!=0: raise ENtoolkitError(ierr)


def ENgetnodeindex(nodeid):
    """Retrieves the index of a node with a specified ID.

    Arguments:
    nodeid: node ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetnodeindex(ctypes.c_char_p(nodeid), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetnodeid(index):
    """Retrieves the ID label of a node with a specified index.

    Arguments:
    index: node index"""
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetnodeid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value


def ENgetnodetype(index):
    """Retrieves the node-type code for a specific node.

    Arguments:
    index: node index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetnodetype(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetnodevalue(index, paramcode):
    """Retrieves the value of a specific node parameter.

    Arguments:
    index:     node index
    paramcode: Node parameter codes consist of the following constants:
                  EN_ELEVATION  Elevation
                  EN_BASEDEMAND ** Base demand
                  EN_PATTERN    ** Demand pattern index
                  EN_EMITTER    Emitter coeff.
                  EN_INITQUAL   Initial quality
                  EN_SOURCEQUAL Source quality
                  EN_SOURCEPAT  Source pattern index
                  EN_SOURCETYPE Source type (See note below)
                  EN_TANKLEVEL  Initial water level in tank
                  EN_DEMAND     * Actual demand
                  EN_HEAD       * Hydraulic head
                  EN_PRESSURE   * Pressure
                  EN_QUALITY    * Actual quality
                  EN_SOURCEMASS * Mass flow rate per minute of a chemical source
                    * computed values)
                   ** primary demand category is last on demand list

               The following parameter codes apply only to storage tank nodes:
                  EN_INITVOLUME  Initial water volume
                  EN_MIXMODEL    Mixing model code (see below)
                  EN_MIXZONEVOL  Inlet/Outlet zone volume in a 2-compartment tank
                  EN_TANKDIAM    Tank diameter
                  EN_MINVOLUME   Minimum water volume
                  EN_VOLCURVE    Index of volume versus depth curve (0 if none assigned)
                  EN_MINLEVEL    Minimum water level
                  EN_MAXLEVEL    Maximum water level
                  EN_MIXFRACTION Fraction of total volume occupied by the inlet/outlet zone in a 2-compartment tank
                  EN_TANK_KBULK  Bulk reaction rate coefficient"""
    j= ctypes.c_float()
    ierr= _lib.ENgetnodevalue(index, paramcode, ctypes.byref(j))
    if ierr!=0:
        if paramcode!=7:
            raise ENtoolkitError(ierr)
        else:
            return -1
    return j.value


##------
def ENgetlinkindex(linkid):
    """Retrieves the index of a link with a specified ID.

    Arguments:
    linkid: link ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetlinkindex(ctypes.c_char_p(linkid), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetlinkid(index):
    """Retrieves the ID label of a link with a specified index.

    Arguments:
    index: link index"""
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetlinkid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value


def ENgetlinktype(index):
    """Retrieves the link-type code for a specific link.

    Arguments:
    index: link index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetlinktype(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetlinknodes(index):
    """Retrieves the indexes of the end nodes of a specified link.

    Arguments:
    index: link index"""
    j1= ctypes.c_int()
    j2= ctypes.c_int()
    ierr= _lib.ENgetlinknodes(index,ctypes.byref(j1),ctypes.byref(j2))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j1.value,j2.value

def ENgetcoord(index):
    """Retrieves the indexes of the end nodes of a specified link.

    Arguments:
    index: link index"""
    j1= ctypes.c_float()
    j2= ctypes.c_float()
    ierr= _lib.ENgetcoord(index,ctypes.byref(j1),ctypes.byref(j2))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j1.value,j2.value

def ENgetlinkvalue(index, paramcode):
    """Retrieves the value of a specific link parameter.

    Arguments:
    index:     link index
    paramcode: Link parameter codes consist of the following constants:
                 EN_DIAMETER     Diameter
                 EN_LENGTH       Length
                 EN_ROUGHNESS    Roughness coeff.
                 EN_MINORLOSS    Minor loss coeff.
                 EN_INITSTATUS   Initial link status (0 = closed, 1 = open)
                 EN_INITSETTING  Roughness for pipes, initial speed for pumps, initial setting for valves
                 EN_KBULK        Bulk reaction coeff.
                 EN_KWALL        Wall reaction coeff.
                 EN_FLOW         * Flow rate
                 EN_VELOCITY     * Flow velocity
                 EN_HEADLOSS     * Head loss
                 EN_STATUS       * Actual link status (0 = closed, 1 = open)
                 EN_SETTING      * Roughness for pipes, actual speed for pumps, actual setting for valves
                 EN_ENERGY       * Energy expended in kwatts
                   * computed values"""
    j= ctypes.c_float()
    ierr= _lib.ENgetlinkvalue(index, paramcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value
#------

def ENgetpatternid(index):
    """Retrieves the ID label of a particular time pattern.

    Arguments:
    index: pattern index"""
    label = ctypes.create_string_buffer(_max_label_len)
    ierr= _lib.ENgetpatternid(index, ctypes.byref(label))
    if ierr!=0: raise ENtoolkitError(ierr)
    return label.value

def ENgetpatternindex(patternid):
    """Retrieves the index of a particular time pattern.

    Arguments:
    id: pattern ID label"""
    j= ctypes.c_int()
    ierr= _lib.ENgetpatternindex(ctypes.c_char_p(patternid), ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetpatternlen(index):
    """Retrieves the number of time periods in a specific time pattern.

    Arguments:
    index:pattern index"""
    j= ctypes.c_int()
    ierr= _lib.ENgetpatternlen(index, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetpatternvalue( index, period):
    """Retrieves the multiplier factor for a specific time period in a time pattern.

    Arguments:
    index:  time pattern index
    period: period within time pattern"""
    j= ctypes.c_float()
    ierr= _lib.ENgetpatternvalue(index, period, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value



def ENgetcount(countcode):
    """Retrieves the number of network components of a specified type.

    Arguments:
    countcode: component code EN_NODECOUNT
                              EN_TANKCOUNT
                              EN_LINKCOUNT
                              EN_PATCOUNT
                              EN_CURVECOUNT
                              EN_CONTROLCOUNT"""
    j= ctypes.c_int()
    ierr= _lib.ENgetcount(countcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgetflowunits():
    """Retrieves a code number indicating the units used to express all flow rates."""
    j= ctypes.c_int()
    ierr= _lib.ENgetflowunits(ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


def ENgettimeparam(paramcode):
    """Retrieves the value of a specific analysis time parameter.
    Arguments:
    paramcode: EN_DURATION
               EN_HYDSTEP
               EN_QUALSTEP
               EN_PATTERNSTEP
               EN_PATTERNSTART
               EN_REPORTSTEP
               EN_REPORTSTART
               EN_RULESTEP
               EN_STATISTIC
               EN_PERIODS"""
    j= ctypes.c_int()
    ierr= _lib.ENgettimeparam(paramcode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value


#-------Retrieving other network information--------
def ENgetcontrol(cindex, ctype, lindex, setting, nindex, level):
    """Retrieves the parameters of a simple control statement.
    Arguments:
       cindex:  control statement index
       ctype:   control type code EN_LOWLEVEL   (Low Level Control)
                                  EN_HILEVEL    (High Level Control)
                                  EN_TIMER      (Timer Control)
                                  EN_TIMEOFDAY  (Time-of-Day Control)
       lindex:  index of link being controlled
       setting: value of the control setting
       nindex:  index of controlling node
       level:   value of controlling water level or pressure for level controls
                or of time of control action (in seconds) for time-based controls"""
    #int ENgetcontrol(int cindex, int* ctype, int* lindex, float* setting, int* nindex, float* level )
    ctype = ctypes.c_int()
    lindex = ctypes.c_int()
    nindex = ctypes.c_int()
    setting = ctypes.c_float()
    level = ctypes.c_float()
    controls =[]
    ierr= _lib.ENgetcontrol(ctypes.c_int(cindex), ctypes.byref(ctype),
                            ctypes.byref(lindex), ctypes.byref(setting),
                            ctypes.byref(nindex), ctypes.byref(level))

    if ierr!=0 : raise ENtoolkitError(ierr)
    else:
        controls.append(TYPECONTROL[ctype.value])
        controls.append(ctype.value)
        controls.append(lindex.value)
        controls.append(nindex.value)
        controls.append(setting.value)
        controls.append(level.value)
        return controls

def ENgetoption(optioncode):
    """Retrieves the value of a particular analysis option.

    Arguments:
    optioncode: EN_TRIALS
                EN_ACCURACY
                EN_TOLERANCE
                EN_EMITEXPON
                EN_DEMANDMULT"""
    j= ctypes.c_float()
    ierr= _lib.ENgetoption(optioncode, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value

def ENgetversion():
    """Retrieves the current version number of the Toolkit."""
    j= ctypes.c_int()
    ierr= _lib.ENgetversion(ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value

def ENgetcurve(curveIndex):
   curveid = ctypes.create_string_buffer(_max_label_len)
   nValues = ctypes.c_int()
   xValues= ctypes.POINTER(ctypes.c_float)()
   yValues= ctypes.POINTER(ctypes.c_float)()
   ierr= _lib.ENgetcurve(curveIndex,
                         ctypes.byref(curveid),
                     ctypes.byref(nValues),
                     ctypes.byref(xValues),
                     ctypes.byref(yValues)
                 )
   # strange behavior of ENgetcurve: it returns also curveID
   # better split in two distinct functions ....
   #print nValues.value
   if ierr!=0: raise ENtoolkitError(ierr)
   curve= []
   for i in range(nValues.value):
      curve.append( (curveid.value, nValues.value, xValues[i],yValues[i]) )
   return curve

def ENgetheadcurveindex(args):
    j= ctypes.c_int()
    ierr= _lib.ENgetheadcurveindex(args, ctypes.byref(j))
    if ierr!=0: raise ENtoolkitError(ierr)
    return j.value

#---------Setting new values for network parameters-------------
def ENsetcontrol(cindex, ctype, lindex, setting, nindex, level ):
    """Sets the parameters of a simple control statement.
    Arguments:
       cindex:  control statement index
       ctype:   control type code  EN_LOWLEVEL   (Low Level Control)
                                   EN_HILEVEL    (High Level Control)
                                   EN_TIMER      (Timer Control)
                                   EN_TIMEOFDAY  (Time-of-Day Control)
       lindex:  index of link being controlled
       setting: value of the control setting
       nindex:  index of controlling node
       level:   value of controlling water level or pressure for level controls
                or of time of control action (in seconds) for time-based controls"""
    #int ENsetcontrol(int cindex, int* ctype, int* lindex, float* setting, int* nindex, float* level )
    ierr= _lib.ENsetcontrol(ctypes.c_int(cindex), ctypes.c_int(ctype),
                            ctypes.c_int(lindex), ctypes.c_float(setting),
                            ctypes.c_int(nindex), ctypes.c_float(level) )
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetnodevalue(index, paramcode, value):
    """Sets the value of a parameter for a specific node.
    Arguments:
    index:  node index
    paramcode: Node parameter codes consist of the following constants:
                  EN_ELEVATION  Elevation
                  EN_BASEDEMAND ** Base demand
                  EN_PATTERN    ** Demand pattern index
                  EN_EMITTER    Emitter coeff.
                  EN_INITQUAL   Initial quality
                  EN_SOURCEQUAL Source quality
                  EN_SOURCEPAT  Source pattern index
                  EN_SOURCETYPE Source type (See note below)
                  EN_TANKLEVEL  Initial water level in tank
                       ** primary demand category is last on demand list
               The following parameter codes apply only to storage tank nodes
                  EN_TANKDIAM      Tank diameter
                  EN_MINVOLUME     Minimum water volume
                  EN_MINLEVEL      Minimum water level
                  EN_MAXLEVEL      Maximum water level
                  EN_MIXMODEL      Mixing model code
                  EN_MIXFRACTION   Fraction of total volume occupied by the inlet/outlet
                  EN_TANK_KBULK    Bulk reaction rate coefficient
    value:parameter value"""
    ierr= _lib.ENsetnodevalue(ctypes.c_int(index), ctypes.c_int(paramcode), ctypes.c_float(value))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetlinkvalue(index, paramcode, value):
    """Sets the value of a parameter for a specific link.
    Arguments:
    index:  link index
    paramcode: Link parameter codes consist of the following constants:
                 EN_DIAMETER     Diameter
                 EN_LENGTH       Length
                 EN_ROUGHNESS    Roughness coeff.
                 EN_MINORLOSS    Minor loss coeff.
                 EN_INITSTATUS   * Initial link status (0 = closed, 1 = open)
                 EN_INITSETTING  * Roughness for pipes, initial speed for pumps, initial setting for valves
                 EN_KBULK        Bulk reaction coeff.
                 EN_KWALL        Wall reaction coeff.
                 EN_STATUS       * Actual link status (0 = closed, 1 = open)
                 EN_SETTING      * Roughness for pipes, actual speed for pumps, actual setting for valves
                 * Use EN_INITSTATUS and EN_INITSETTING to set the design value for a link's status or setting that
                   exists prior to the start of a simulation. Use EN_STATUS and EN_SETTING to change these values while
                   a simulation is being run (within the ENrunH - ENnextH loop).

    value:parameter value"""
    ierr= _lib.ENsetlinkvalue(ctypes.c_int(index), ctypes.c_int(paramcode), ctypes.c_float(value))
    if ierr!=0:
        if paramcode!=3:raise ENtoolkitError(ierr)

def ENaddpattern(patternid):
    """Adds a new time pattern to the network.
    Arguments:
      id: ID label of pattern"""
    ierr= _lib.ENaddpattern(ctypes.c_char_p(patternid))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetpattern(index, factors):
    """Sets all of the multiplier factors for a specific time pattern.
    Arguments:
    index:    time pattern index
    factors:  multiplier factors list for the entire pattern"""
    # int ENsetpattern( int index, float* factors, int nfactors )
    #print factors
    #print len(factors)
    nfactors= len(factors)
    cfactors_type= ctypes.c_float* nfactors
    cfactors= cfactors_type()
    for i in range(nfactors):
       cfactors[i]= float(factors[i] )
    ierr= _lib.ENsetpattern(ctypes.c_int(index), cfactors, ctypes.c_int(nfactors) )
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetpatternvalue(index, period, value):
    """Sets the multiplier factor for a specific period within a time pattern.
    Arguments:
       index: time pattern index
       period: period within time pattern
       value:  multiplier factor for the period"""
    #int ENsetpatternvalue( int index, int period, float value )
    ierr= _lib.ENsetpatternvalue( ctypes.c_int(index), ctypes.c_int(period), ctypes.c_float(value) )
    if ierr!=0: raise ENtoolkitError(ierr)

def ENsetqualtype (qualcode,chemname,chemunits,tracenode):
    """Sets the type of water quality analysis called for.
    Arguments:
    qualcode:   water quality analysis code (see below)
    chemname:   name of the chemical being analyzed
    chemunits:  units that the chemical is measured in
    tracenode:  ID of node traced in a source tracing analysis"""
    ierr= _lib.ENsetqualtype( ctypes.c_int(qualcode), chemname, chemunits, tracenode)
    if ierr!=0: raise ENtoolkitError(ierr)

def  ENsettimeparam(paramcode, timevalue):
    """Sets the value of a time parameter.
    Arguments:
      paramcode: time parameter code EN_DURATION
                                     EN_HYDSTEP
                                     EN_QUALSTEP
                                     EN_PATTERNSTEP
                                     EN_PATTERNSTART
                                     EN_REPORTSTEP
                                     EN_REPORTSTART
                                     EN_RULESTEP
                                     EN_STATISTIC
                                     EN_PERIODS
      timevalue: value of time parameter in seconds
                      The codes for EN_STATISTIC are:
                      EN_NONE     none
                      EN_AVERAGE  averaged
                      EN_MINIMUM  minimums
                      EN_MAXIMUM  maximums
                      EN_RANGE    ranges"""
    ierr= _lib.ENsettimeparam(ctypes.c_int(paramcode), ctypes.c_int(timevalue))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsetoption( optioncode, value):
    """Sets the value of a particular analysis option.

    Arguments:
      optioncode: option code EN_TRIALS
                              EN_ACCURACY
                              EN_TOLERANCE
                              EN_EMITEXPON
                              EN_DEMANDMULT
      value:  option value"""
    ierr= _lib.ENsetoption(ctypes.c_int(optioncode), ctypes.c_float(value))
    if ierr!=0: raise ENtoolkitError(ierr)






#----------Running a hydraulic analysis --------------------------
def ENsolveH():
    """Runs a complete hydraulic simulation with results for all time periods written to the
    binary Hydraulics file."""
    ierr= _lib.ENsolveH()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopenH():
    """Opens the hydraulics analysis system"""
    ierr= _lib.ENopenH()


def ENinitH(flag=None):
    """Initializes storage tank levels, link status and settings, and the simulation clock time prior
to running a hydraulic analysis.

    flag  EN_NOSAVE [+EN_SAVE] [+EN_INITFLOW] """
    ierr= _lib.ENinitH(flag)
    if ierr!=0: raise ENtoolkitError(ierr)


def ENrunH():
    """Runs a single period hydraulic analysis, retrieving the current simulation clock time t"""
    ierr= _lib.ENrunH(ctypes.byref(_current_simulation_time))
    if ierr>=100:
       raise ENtoolkitError(ierr)
    elif ierr>0:
       return ENgeterror(ierr)
    elif ierr==0:
        return _current_simulation_time.value


def ENsimtime():
    """retrieves the current simulation time t as datetime.timedelta instance"""
    return datetime.timedelta(seconds= _current_simulation_time.value )


def ENnextH():
    """Determines the length of time until the next hydraulic event occurs in an extended period
       simulation."""
    _deltat= ctypes.c_long()
    ierr= _lib.ENnextH(ctypes.byref(_deltat))
    if ierr!=0: raise ENtoolkitError(ierr)
    return _deltat.value


def ENcloseH():
    """Closes the hydraulic analysis system, freeing all allocated memory."""
    ierr= _lib.ENcloseH()
    if ierr!=0: raise ENtoolkitError(ierr)

#--------------------------------------------

#----------Running a quality analysis --------------------------
def ENsolveQ():
    """Runs a complete water quality simulation with results at uniform reporting intervals written to EPANET's binary Output file."""
    ierr= _lib.ENsolveQ()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENopenQ():
    """Opens the water quality analysis system"""
    ierr= _lib.ENopenQ()


def ENinitQ(flag=None):
    """Initializes water quality and the simulation clock time prior to running a water quality analysis.

    flag  EN_NOSAVE | EN_SAVE """
    ierr= _lib.ENinitQ(flag)
    if ierr!=0: raise ENtoolkitError(ierr)

def ENrunQ():
    """Makes available the hydraulic and water quality results that occur at the start of the next time period of a water quality analysis, where the start of the period is returned in t."""
    ierr= _lib.ENrunQ(ctypes.byref(_current_simulation_time))
    if ierr>=100:
      raise ENtoolkitError(ierr)
    elif ierr>0:
      return ENgeterror(ierr)
    elif ierr==0:
        return _current_simulation_time.value

def ENnextQ():
    """Advances the water quality simulation to the start of the next hydraulic time period."""
    _deltat= ctypes.c_long()
    ierr= _lib.ENnextQ(ctypes.byref(_deltat))
    if ierr!=0: raise ENtoolkitError(ierr)
    return _deltat.value

def ENstepQ():
    """Advances the water quality simulation one water quality time step."""
    _deltat= ctypes.c_long()
    ierr= _lib.ENstepQ(ctypes.byref(_deltat))
    if ierr!=0: raise ENtoolkitError(ierr)
    return _deltat.value

def ENcloseQ():
    """Closes the water quality analysis system, freeing all allocated memory."""
    ierr= _lib.ENcloseQ()
    if ierr!=0: raise ENtoolkitError(ierr)
#--------------------------------------------





def ENsaveH():
    """Transfers results of a hydraulic simulation from the binary Hydraulics file to the binary
Output file, where results are only reported at uniform reporting intervals."""
    ierr= _lib.ENsaveH()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENsaveinpfile(fname):
    """Writes all current network input data to a file using the format of an EPANET input file."""
    ierr= _lib.ENsaveinpfile( ctypes.c_char_p(fname))
    if ierr!=0: raise ENtoolkitError(ierr)


def ENreport():
    """Writes a formatted text report on simulation results to the Report file."""
    ierr= _lib.ENreport()
    if ierr!=0: raise ENtoolkitError(ierr)


def ENgeterror(errcode):
    """Retrieves the text of the message associated with a particular error or warning code."""
    errmsg= ctypes.create_string_buffer(_err_max_char)
    _lib.ENgeterror( errcode,ctypes.byref(errmsg), _err_max_char )
    return errmsg.value


def LoadInpFile(nomeinp):
    nomerpt=nomeinp[:len(nomeinp)-4]+'.txt'
    nomebin=nomeinp[:len(nomeinp)-4]+'.bin'
    ENopen(nomeinp, nomerpt, nomebin)



## Get type of the parameters
def getLinkTypeIndex():
    #Retrieves the link-type code for all links.
    LinkTypeIndex=[]
    for i in range(1,getLinkCount()+1):
        LinkTypeIndex.append(ENgetlinktype(i))
    return LinkTypeIndex

def getLinkType():
    #Retrieves the link-type code for all links.
    LinkType=[]
    LinkTypeIndex=getLinkTypeIndex()
    for i in range(0,getLinkCount()):
        LinkType.append(TYPELINK[LinkTypeIndex[i]])
    return LinkType

def getNodeTypeIndex():
    #Retrieves the node-type code for all nodes.
    NodeTypeIndex=[]
    for i in range(1,getNodeCount()+1):
        NodeTypeIndex.append(ENgetnodetype(i))
    return NodeTypeIndex

def getNodeType():
    #Retrieves the link-type code for all links.
    NodeType=[]
    NodeTypeIndex=getNodeTypeIndex()
    for i in range(0,getNodeCount()):
        NodeType.append(TYPENODE[NodeTypeIndex[i]])
    return NodeType

## Get all the countable network parameters
def getNodeCount():
    return ENgetcount(EN_NODECOUNT)

def getNodeTankReservoirCount():
    return ENgetcount(EN_TANKCOUNT)

def getLinkCount():
    return ENgetcount(EN_LINKCOUNT)

def getPatternCount():
    return ENgetcount(EN_PATCOUNT)

def getCurveCount():
    return ENgetcount(EN_CURVECOUNT)

def getControlRulesCount():
    return ENgetcount(EN_CONTROLCOUNT)

def getNodeJunctionsCount():
    return getNodeCount()-getNodeTankReservoirCount()

def getNodeReservoirCount():
    NodeReservoirCount=0
    NodeTypeIndex = getNodeTypeIndex()
    for i in range(0,getNodeCount()):
        if NodeTypeIndex[i]==1:
            NodeReservoirCount+=1
    return NodeReservoirCount

def getNodeTankCount():
    NodeTankCount=0
    NodeTypeIndex = getNodeTypeIndex()
    for i in range(0,getNodeCount()):
        if NodeTypeIndex[i]==2:
            NodeTankCount+=1
    return NodeTankCount

def getLinkPipeCount():
    LinkPipeCount=0
    LinkTypeIndex = getLinkTypeIndex()
    for i in range(0,getLinkCount()):
        if LinkTypeIndex[i]<2:
            LinkPipeCount+=1
    return LinkPipeCount

def getLinkPumpCount():
    LinkPumpCount=0
    LinkTypeIndex = getLinkTypeIndex()
    for i in range(0,getLinkCount()):
        if LinkTypeIndex[i]==2:
            LinkPumpCount+=1
    return LinkPumpCount

def getLinkValveCount():
    LinkValveCount=0
    LinkTypeIndex = getLinkTypeIndex()
    for i in range(0,getLinkCount()):
        if LinkTypeIndex[i]>2:
            LinkValveCount+=1
    return LinkValveCount

def getControls():
    #Retrieves the parameters of all control statements
    Controls=[]
    if getControlRulesCount()>0:
        for i in range(1,getControlRulesCount()+1):
            Controls.append(ENgetcontrol(i, 0, 0, 0, 0, 0))
    return Controls

def getFlowUnits():
    #Retrieves flow units used to express all flow rates.
    units=[]
    flowunitsindex = ENgetflowunits()
    units = FlowUnits[flowunitsindex]
    return units

def getFlowUnitsCode():
    #Retrieves flow units used to express all flow rates.
    return ENgetflowunits()

## Get all the link data
def getLinkNameID(*args):
    #Retrieves the ID label(s) of all links, or the IDs of an index set of links
    linknameid=[]
    if len(args) == 0:
        for i in range(1, getLinkCount()+1, 1):
            linknameid.append(ENgetlinkid(i))
        return linknameid
    else:
        for i in range(0, len(args), 1):
            linknameid.append(ENgetlinkid(args[i]))
        return linknameid

def getLinkIndex(*args):
    #Retrieves the indices of all links, or the indices of an ID set of links
    value = []
    if len(args) == 0:
        value = range(1, getLinkCount()+1)
        return value
    else:
        for i in range(0, len(args), 1):
            value.append(ENgetlinkindex(args[i]))
        return value

def getLinkPipeIndex():
    #Retrieves the pipe index
    value = tuple(range(1, getLinkPipeCount()+1, 1))
    return value

def getLinkPumpIndex():
    #Retrieves the pump index
    value = getLinkTypeIndex()
    LinkPumpIndex = []
    for i in range(0, getLinkCount()):
        if value[i] == 2:
            LinkPumpIndex.append(i+1)
    return LinkPumpIndex

def getLinkValveIndex():
    #Retrieves the valve index
    value = getLinkTypeIndex()
    LinkValveIndex = []
    for i in range(0, getLinkCount()):
        if value[i] > 2:
            LinkValveIndex.append(i+1)
    return LinkValveIndex

def getLinkDiameter():
    #Retrieves the value of all link diameters
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 0))
    return value

def getLinkLength():
    #Retrieves the value of all link lengths
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 1))
    return value

def getLinkRoughnessCoeff():
    #Retrieves the value of all link roughness
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 2))
    return value

def getLinkMinorLossCoeff():
    #Retrieves the value of all link minor loss coefficients
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 3))
    return value

def getLinkInitialStatus():
    #Retrieves the value of all link initial status
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 4))
    return value

def getLinkInitialSetting():
    #Retrieves the value of all link roughness for pipes or initial speed for pumps or initial setting for valves
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 5))
    return value

def getLinkBulkReactionCoeff():
    #Retrieves the value of all link bulk reaction coefficients
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 6))
    return value

def getLinkWallReactionCoeff():
    #Retrieves the value of all link wall reaction coefficients
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i, 7))
    return value

def getLinkPipeNameID():
    args = getLinkPipeIndex()
    pipesid=[]
    for i in range(0, len(args), 1):
        pipesid.append(ENgetlinkid(args[i]))
    return pipesid

def getLinkPumpNameID():
    args = getLinkPumpIndex()
    pumpsid=[]
    for i in range(0, len(args), 1):
        pumpsid.append(ENgetlinkid(args[i]))
    return pumpsid

def getLinkValveNameID():
    args = getLinkValveIndex()
    valvesid=[]
    for i in range(0, len(args), 1):
        valvesid.append(ENgetlinkid(args[i]))
    return valvesid

# link dynamics
def getLinkFlows():
    #Retrieves the value of all computed link flow rates
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,8))
    return value

def getLinkVelocity():
    #Retrieves the value of all computed link velocities
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,9))
    return value

def getLinkHeadloss():
    #Retrieves the value of all computed link headloss
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,10))
    return value
def getLinkStatus():
    #Retrieves the value of all computed link status (0 = closed, 1 = open)
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,11))
    return value
def getLinkSettings():
    #Retrieves the value of all computed link roughness for pipes or actual speed for pumps or actual setting for valves
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,12))
    return value
def getLinkPumpEnergy():
    #Retrieves the value of all computed energy in kwatts
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,13))
    return value
def getLinkQuality():
    #epanet20013
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,14))
    return value
def getLinkPumpPatternIndex():
    #epanet20013
    value=[]
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinkvalue(i,15))
    return value

## Get all the node data
def getNodeNameID(*args):
    #Retrieves the ID label of all nodes or some nodes with a specified index.
    nodenameid=[]
    if len(args) == 0:
        for i in range(1, getNodeCount()+1, 1):
            nodenameid.append(ENgetnodeid(i))
        return nodenameid
    else:
        for i in range(0, len(args), 1):
            nodenameid.append(ENgetnodeid(args[i]))
        return nodenameid

def getNodeIndex(*args):
    #Retrieves the indices of all nodes, or the indices of an ID set of nodes
    value = []
    if len(args) == 0:
        value = range(1, getNodeCount()+1)
        return value
    else:
        for i in range(0, len(args), 1):
            value.append(ENgetnodeindex(args[i]))
        return value

def getNodeJunctionIndex():
    #Retrieves the junction index
    value = range(1, getNodeJunctionsCount()+1, 1)
    return value

def getNodeReservoirIndex():
    #Retrieves the reservoir index
    value = getNodeTypeIndex()
    NodeReservoirIndex = []
    for i in range(0, getNodeCount()):
        if value[i] == 1:
            NodeReservoirIndex.append(i+1)
    return NodeReservoirIndex

def getNodeTankIndex():
    #Retrieves the tank index
    value = getNodeTypeIndex()
    NodeTankIndex = []
    for i in range(0, getNodeCount()):
        if value[i] == 2:
            NodeTankIndex.append(i+1)
    return NodeTankIndex

def getNodeReservoirNameID():
    args = getNodeReservoirIndex()
    reservoirsid=[]
    for i in range(0, len(args), 1):
        reservoirsid.append(ENgetnodeid(args[i]))
    return reservoirsid

def getNodeTankNameID():
    args = getNodeTankIndex()
    tanksid=[]
    for i in range(0, len(args), 1):
        tanksid.append(ENgetnodeid(args[i]))
    return tanksid

def getNodeJunctionNameID():
    args = getNodeJunctionIndex()
    junctionsid=[]
    for i in range(0, len(args), 1):
        junctionsid.append(ENgetnodeid(args[i]))
    return junctionsid

def getNodeElevations():
    #Retrieves the value of all node elevations
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i, 0))
    return value

def getNodeBaseDemands():
    #Retrieves the value of all node basedemands
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i, 1))
    return value

def getNodeDemandPatternIndex():
    #Retrieves the value of all node demand pattern indices
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i, 2))
    return value

def getNodeEmitterCoeff():
    #Retrieves the value of all node emmitter coefficients
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i, 3))
    return value

def getNodeInitialQuality():
    #Retrieves the value of all node initial quality
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i, 4))
    return value

def getNodeSourceQuality():
    #Retrieves the value of all nodes source quality
    value = []
    for i in range(1, getNodeCount()+1):
        try:
            value.append(ENgetnodevalue(i, 5))
        except:
            value.append(None)
    return value

def getNodeSourcePatternIndex():
    #Retrieves the value of all node source pattern index
    value = []
    for i in range(1, getNodeCount()+1):
        try:
            value.append(ENgetnodevalue(i, 6))
        except:
            value.append(None)
    return value

def getNodeSourceTypeCode():
    #Retrieves the value of all node source pattern index
    value = []
    for i in range(1, getNodeCount()+1):
        try:
            value.append(ENgetnodevalue(i, 7))
        except:
            value.append(None)
    return value

def getNodeSourceType():
    #Retrieves the value of all node source type
    cnt=getNodeCount()
    value = [None] * cnt
    for i in range(0, cnt):
        value[i] = ENgetnodevalue(i+1,7)
        if value[i]==-1:
            value[i]=None
        else:
            value[i] = TYPESOURCE[value[i]]
    return value

def getNodesConnectingLinksIndex():
    #Retrieves the indexes of the from/to nodes of all links.
    value = []
    for i in range(1, getLinkCount()+1):
        value.append(ENgetlinknodes(i))
    return value

def getNodesCoords():
    #Retrieves the indexes of the from/to nodes of all links.
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetcoord(i))
    return value


def getNodesConnectingLinksID():
    #Retrieves the id of the from/to nodes of all links.
    value = []; linknodes = getNodesConnectingLinksIndex()
    for i in range(0, getLinkCount()):
        value.append([getNodeNameID(linknodes[i][0]), getNodeNameID(linknodes[i][1])])
    return value

# node dynamics
def getNodeActualDemand():
    #Retrieves the computed value of all actual demands
    value=[]
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i,9))
    return value

def getNodeActualDemandSensingNodes(*arg):
    #Retrieves the computed demand values at some sensing nodes
    value=[]
    for i in range(0,len(arg[0])):
        value.append(ENgetnodevalue(arg[0][i], 9))

def getNodeHydaulicHead():
    #Retrieves the computed values of all hydraulic heads
    value=[]
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i,10))
    return value

def getNodePressure():
    #Retrieves the computed values of all node pressures
    value=[]
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i,11))
    return value

def getNodeActualQuality():
    #Retrieves the computed values of the actual quality for all nodes
    value=[]
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i,12))
    return value
def getNodeMassFlowRate():
    #Retrieves the computed mass flow rates per minute of chemical sources
    value = []
    for i in range(1, getNodeCount()+1):
        value.append(ENgetnodevalue(i,13))
    return value


## Get all tank data
def getNodeTankInitialLevel():
    #Retrieves the value of all tank initial water levels
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 8)
    return value

def getNodeTankInitialWaterVolume():
    #Retrieves the tank initial volume
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 14)
    return value

def getNodeTankMixiningModelCode():
    #Retrieves the tank mixing mode (mix1, mix2, fifo, lifo)
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value.append(ENgetnodevalue(nodetankindex, 15))
    return value

def getNodeTankMixiningModel():
    #Retrieves the tank mixing mode (mix1, mix2, fifo, lifo)
    value = [None] * getNodeCount()
    v = getNodeTankMixiningModelCode()
    for index, nodetankindex in enumerate(getNodeTankIndex()):
        if getNodeTankCount()==1:
            value.append(TYPEMIXMODEL[v[nodetankindex]])
        else:
            value.append(TYPEMIXMODEL[v[nodetankindex+1]])
    return value

def getNodeTankMixZoneVolume():
    #Retrieves the tank mixing zone volume
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 16)
    return value

def getNodeTankDiameter():
    #Retrieves the tank diameters
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 17)
    return value

def getNodeTankMinimumWaterVolume():
    #Retrieves the tank minimum volume
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 18)
    return value

def getNodeTankVolumeCurveIndex():
    #Retrieves the tank volume curve index
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 19)
    return value

def getNodeTankMinimumWaterLevel():
    #Retrieves the tank minimum water level
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 20)
    return value

def getNodeTankMaximumWaterLevel():
    #Retrieves the tank maximum water level
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 21)
    return value

def getNodeTankFraction():
    #Retrieves the tank Fraction of total volume occupied by the inlet/outlet zone in a 2-compartment tank
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 22)
    return value

def getNodeTankBulkReactionCoeff():
    #Retrieves the tank bulk rate coefficient
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 23)
    return value

def getNodeTankVolume():
    #epanet20013.dll
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 24)
    return value

def getNodeTankMaxVolume():
    #epanet20013.dll
    value = [None] * getNodeCount()
    for i, nodetankindex in enumerate(getNodeTankIndex()):
        value[nodetankindex-1]=ENgetnodevalue(nodetankindex, 25)
    return value


## Get all options
def getOptionsMaxTrials():
    #Retrieve maximum number of analysis trials
    return ENgetoption(EN_TRIALS)

def getOptionsAccuracyValue():
    #Retrieve the analysis convergence criterion (0.001)
    return ENgetoption(EN_ACCURACY)

def getOptionsQualityTolerance():
    #Retrieve the water quality analysis tolerance
    return ENgetoption(EN_TOLERANCE)

def getOptionsEmitterExponent():
    #Retrieve power exponent for the emmitters (0.5)
    return ENgetoption(EN_EMITEXPON)

def getOptionsPatternDemandMultiplier():
    #Retrieve the demand multiplier (x1)
    return ENgetoption(EN_DEMANDMULT)

## Get pattern data
def getPatternNameID(*args):
    #Retrieves the ID label of all or some time patterns indices
    patternnameid=[]
    if len(args) == 0:
        for i in range(1, getPatternCount()+1, 1):
            patternnameid.append(ENgetpatternid(i))
        return patternnameid
    else:
        for i in range(0, len(args), 1):
            patternnameid.append(ENgetpatternid(args[i]))
        return patternnameid

def getPatternIndex(*args):
    #Retrieves the index of all or some time patterns IDs
    value = []
    if len(args) == 0:
        value = range(1, getPatternCount()+1)
        return value
    else:
        for i in range(0, len(args), 1):
            value.append(ENgetpatternindex(args[i]))
        return value

def getPatternLengths():
    #Retrieves the number of time periods in all or some patterns
    value = []
    for i in range(0, getPatternCount(), 1):
        value.append(ENgetpatternlen(i+1))
    return value

def getPattern():
    #Retrieves the multiplier factor for all patterns and all times
    import numpy
    tmpmaxlen=max(getPatternLengths())
    value = numpy.zeros(shape=(getPatternCount(),tmpmaxlen))
    for i in range(0,getPatternCount()):
        tmplength=getPatternLengths()[i]
        for j in range(1,tmplength+1):
            value[i][j-1]=ENgetpatternvalue(i+1, j)

        if tmplength<tmpmaxlen:
            for j in range((tmplength),tmpmaxlen):
                value[i][j]=value[i][j-tmplength]
    return value

def getPatternValue(patternIndex, patternStep):
    #Retrieves the multiplier factor for a certain pattern and time
    return ENgetpatternvalue(patternIndex, patternStep)


## Get quality types
def getQualityTypeCode():
    #Retrieves the type of water quality analysis type
    return ENgetqualtype()

def getQualityType():
    #Retrieves the type of water quality analysis type
    v = ENgetqualtype()
    value = []
    if len(str(v)) > 1:
        value.append([TYPEQUALITY[v[0]], getNodeNameID(v[1])])
    else:
        value.append(TYPEQUALITY[v])
    return value[0]

def getQualityTraceNodeIndex():
    v = ENgetqualtype()
    if len(str(v)) > 1:
        return v[1]

def ENgetqualtype():
    #Retrieves the type of water quality analysis type.
    typecode= ctypes.c_int()
    nodeindex= ctypes.c_int()
    ierr= _lib.ENgetqualtype(ctypes.byref(typecode), ctypes.byref(nodeindex))
    if ierr!=0: raise ENtoolkitError(ierr)
    if typecode.value < 3:
        return typecode.value
    else:
        return [typecode.value, nodeindex.value] # (type code, node index) trace node


## Get time parameters
def getTimeSimulationDuration():
    #Retrieves the value of simulation duration
    return ENgettimeparam(EN_DURATION)

def getTimeHydraulicStep():
    #Retrieves the value of the hydraulic time step
    return ENgettimeparam(EN_HYDSTEP)

def getTimeQualityStep():
    #Retrieves the value of the water quality time step
    return ENgettimeparam(EN_QUALSTEP)

def getTimePatternStep():
    #Retrieves the value of the pattern time step
    return ENgettimeparam(EN_PATTERNSTEP)

def getTimePatternStart():
    #Retrieves the value of pattern start time
    return ENgettimeparam(EN_PATTERNSTART)

def getTimeReportingStep():
    #Retrieves the value of the reporting time step
    return ENgettimeparam(EN_REPORTSTEP)

def getTimeReportingStart():
    #Retrieves the value of the reporting start time
    return ENgettimeparam(EN_REPORTSTART)

def getTimeRuleControlStep():
    #Retrieves the time step for evaluating rule-based controls
    return ENgettimeparam(EN_RULESTEP)

def getTimeReportingPeriods():
    #Retrieves the number of reporting periods saved to the binary
    return ENgettimeparam(EN_PERIODS)

def getTimeStatisticsType():
    #Retrieves the type of time series post-processing ('NONE','AVERAGE','MINIMUM','MAXIMUM', 'RANGE')
    return TYPESTATS[ENgettimeparam(EN_STATISTIC)]

def getTimeStatisticsCode():
    return ENgettimeparam(EN_STATISTIC)

def getVersion():
    return ENgetversion()

def addPattern(*args):
    valueIndex=-1
    if len(args)==1:
        ENaddpattern(args[0])
        valueIndex = getPatternIndex(args[0])
    elif len(args)==2:
        ENaddpattern(args[0])
        valueIndex = getPatternIndex(args[0])
        setPattern(valueIndex[0],args[1])
    return valueIndex


## Units: US Customary - SI metric
def getNodePressureUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'pounds per square inch'
    elif code == EN_LPS or code == EN_LPM or code == EN_MLD or code == EN_CMH or code == EN_CMD:
        return 'meters'

def getPatternDemandsUnits():
    code = getFlowUnitsCode()
    return FlowUnits[code]

def getLinkPipeDiameterUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'inches'
    else:
        return 'millimeters'

def getNodeTankDiameterUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'feet'
    else:
        return 'meters'

def getEnergyEfficiencyUnits():
    return 'percent'

def getNodeElevationUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'feet'
    else:
        return 'meters'

def getNodeEmitterCoefficientUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'flow units @ 1 psi drop'
    else:
        return 'flow units @ 1 meter drop'

def getEnergyUnits():
    return 'kwatt-hours'

def getLinkFrictionFactorUnits():
    return 'unitless'

def getNodeHeadUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'feet'
    else:
        return 'meters'

def getLinkLengthsUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'feet'
    else:
        return 'meters'

def getLinkMinorLossCoeffUnits():
    return 'unitless'

def getLinkPumpPowerUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'horsepower'
    else:
        return 'kwatts'

def getQualityReactionCoeffBulkUnits():
    return '1/day (1st-order)'

def getQualityReactionCoeffWallUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'mass/sq-ft/day (0-order), ft/day (1st-order)'
    else:
        return 'mass/sq-m/day(0-order), meters/day (1st-order)'

def getLinkPipeRoughnessCoeffUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'millifeet(Darcy-Weisbach), unitless otherwise'
    else:
        return 'mm(Darcy-Weisbach), unitless otherwise'

def getQualitySourceMassInjectionUnits():
    return 'mass/minute'

def getLinkVelocityUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'ft/sec'
    else:
        return 'meters/sec'

def getNodeTankVolumeUnits():
    code = getFlowUnitsCode()
    if code == EN_CFS or code == EN_GPM or code == EN_MGD or code == EN_IMGD or code == EN_AFD:
        return 'cubic feet'
    else:
        return 'cubic meters'

def getQualityWaterAgeUnits():
    return 'hours'


def getCurvesInfo():
    value = []
    for i in range(1,getCurveCount()+1):
        value.append(ENgetcurve(i))
    return value

def getHeadCurveIndex():
    value=[]
    for i, pumpindex in enumerate(getLinkPumpIndex()):
        value.append(ENgetheadcurveindex(pumpindex))
    return value

## Hydraulic analysis
def openHydraulicAnalysis():
    return ENopenH()

def initializeHydraulicAnalysis():
    return ENinitH(1)

def runHydraulicAnalysis():
    return ENrunH() # tstep

def nextHydraulicAnalysisStep():
    return ENnextH()

def closeHydraulicAnalysis():
    return ENcloseH()

# Quality analysis
def openQualityAnalysis():
    return ENopenQ()

def initializeQualityAnalysis():
    return ENinitQ(1)

def runQualityAnalysis():
    return ENrunQ()

def nextQualityAnalysisStep():
    return ENnextQ()

def closeQualityAnalysis():
    return ENcloseQ()


# def saveHydraulicFile(obj,hydname):
#     ENsavehydfile(hydname)
#
# def useHydraulicFile(obj,hydname):
#     ENusehydfile(hydname)

def saveHydraulicsOutputReportingFile():
    ENsaveH()

def stepQualityAnalysisTimeLeft():
     return ENstepQ() # tleft

def closeNetwork():
    return ENclose()


def setQualityType(*args):
    qualcode=0;chemname="";chemunits="";tracenode=0
    if EN_NONE==args[0]:
        ENsetqualtype(qualcode,chemname,chemunits,tracenode)
    elif EN_AGE==args[0]:
        qualcode=2
        ENsetqualtype(qualcode,chemname,chemunits,tracenode)
    elif EN_CHEM==args[0]:
        qualcode=1
        chemname=args[0]
        if len(args)<3:
            chemunits='mg/L'
        else:
            chemunits=args[1]
        ENsetqualtype(qualcode,chemname,chemunits,tracenode)
    elif EN_TRACE==args[0]:
        qualcode=3
        tracenode=args[1]
        ENsetqualtype(qualcode,chemname,chemunits,tracenode)
    else:
        qualcode=1
        chemname=args[0]
        if len(args)<3:
            chemunits='mg/L'
        else:
            chemunits=args[1]
        ENsetqualtype(qualcode,chemname,chemunits,tracenode)

def setPattern(patInd,patternVector):
    ENsetpattern(patInd, patternVector)

def setControl(controlRuleIndex,controlTypeCode,linkIndex,controlSettingValue,nodeIndex,controlLevel):
    # Example: d.setControl(1,1,13,1,11,150) controlRuleIndex must exist
    if controlRuleIndex<=getControlRulesCount():
        ENsetcontrol(controlRuleIndex,controlTypeCode,linkIndex,controlSettingValue,nodeIndex,controlLevel)
    else:
        print('New rules cannot be added in this epanet version')

## Set link parameters
def setLinkDiameter(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 0, value[i])

def setLinkLength(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 1, value[i])

def setLinkRoughnessCoeff(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 2, value[i])

def setLinkMinorLossCoeff(value):
    for i in range(0,getLinkCount()):
        if value[i]==0:
            ENsetlinkvalue(i+1, 3, float(0))
        else:
            ENsetlinkvalue(i+1, 3, value[i])

def setLinkInitialStatus(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 4, value[i])

def setLinkInitialSetting(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 5, value[i])

def setLinkBulkReactionCoeff(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 6, value[i])

def setLinkWallReactionCoeff(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 7, value[i])

def setLinkStatus(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 11, value[i])

def setLinkSettings(value):
    for i in range(0,getLinkCount()):
        ENsetlinkvalue(i+1, 12, value[i])

## Set node parameters
def setNodeElevations(value):
    for i in range(0,getNodeCount()):
        ENsetnodevalue(i+1, 0, value[i])

def setNodeBaseDemands(value):
    for i in range(0,getNodeCount()):
        ENsetnodevalue(i+1, 1, value[i])

def setNodeDemandPatternIndex(value):
    for i in range(0,getNodeCount()):
        ENsetnodevalue(i+1, 2, value[i])

def setNodeEmitterCoeff(value):
    for i in range(0,getNodeJunctionsCount()):
        ENsetnodevalue(i+1, 3, value[i])

def setNodeInitialQuality(value):
    for i in range(0,getNodeCount()):
        ENsetnodevalue(i+1, 4, value[i])

def setNodeTankInitialLevel(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 8, value[i])

def setNodeTankMixingModel(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 15, value[i])

def setNodeTankDiameter(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 17, value[i])

def setNodeTankMinimumWaterLevel(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 20, value[i])

def setNodeTankMinimumWaterVolume(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 18, value[i])

def setNodeTankMaximumWaterLevel(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 21, value[i])

def setNodeTankFraction(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 22, value[i])

def setNodeTankBulkReactionCoeff(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 23, value[i])

## Set source parameters
def setNodeSourceTypeCode(value):
    for i in range(0,getNodeCount()):
        if value[i]!=-1:
            ENsetnodevalue(i+1, 7, value[i])

def setNodeSourceQuality(value):
    for i in range(0,getNodeCount()):
        if value[i]!=-1:
            ENsetnodevalue(i+1, 5, value[i])

def setNodeSourcePatternIndex(value):
    for i in range(0,getNodeCount()):
        if value[i]!=None:
            ENsetnodevalue(i+1, 6, value[i])


## Set options
def setOptionsMaxTrials(value):
    ENsetoption(0,value)

def setOptionsAccuracyValue(value):
    ENsetoption(1,value)

def setOptionsQualityTolerance(value):
    ENsetoption(2,value)

def setOptionsEmitterExponent(value):
    ENsetoption(3,value)

def setOptionsPatternDemandMultiplier(value):
    ENsetoption(4,value)

## Set time parameters
def setTimeSimulationDuration(value):
    ENsettimeparam(0,value)

def setTimeHydraulicStep(value):
    ENsettimeparam(1,value)

def setTimeQualityStep(value):
    ENsettimeparam(2,value)

def setTimePatternStep(value):
    ENsettimeparam(3,value)

def setTimePatternStart(value):
    ENsettimeparam(4,value)

def setTimeReportingStep(value):
    ENsettimeparam(5,value)

def setTimeReportingStart(value):
    ENsettimeparam(6,value)

def setTimeRuleControlStep(value):
    ENsettimeparam(7,value)

def setTimeStatisticsType(value):
    ENsettimeparam(8,value)

## Node Coordinates
def getNodeCoordinates():
    global inpname
    coord=[]
    file = open(inpname,'r')
    u=0
    while True:
        s1=file.readline()
        u+=1
        if s1=="[END]\n":
            break

    file = open(inpname,'r')
    a=0;k=0
    x=[]
    y=[]
    # Create a list.
    vertx=[];verty=[]
    # Append empty lists in first two indexes.
    for i in range(0,getLinkCount()):
        vertx.append([])
        verty.append([])
    node=getNodesConnectingLinksIndex()
    for i in range(0, u):
        if a==0:
            s=file.readline()
            ss=";Node            \tX-Coord         \tY-Coord\n"
        if s == ss or a==1:
            s=file.readline()
            coord.append(s)
            a=1;m=0
            if s=="[VERTICES]\n":
                s=file.readline()
                ss=";Link               \tX-Coord           \tY-Coord\n"
                a=2
            if s!="\n" and a!=2:
                pp = s.split()
                x.append(float(pp[1]))
                y.append(float(pp[2]))
                k+=1
        if s == ss or a==2:
            s=file.readline()
            if s=="[LABELS]\n":
                break
            if s!="\n":
                pp = s.split()
                linkIndex = getLinkIndex(pp[0])
                # Add elements to empty lists.
                vertx[linkIndex[0]-1].append(float(pp[1]))
                verty[linkIndex[0]-1].append(float(pp[2]))
                k+=1


    nlink = getLinkCount()
    #nnodes = getNodeCount()
    x1 = []
    y1 = []
    x2 = []; ToNode = []
    y2 = []; FromNode = []
    for i in range(0,nlink):
        fr = node[i][0]
        FromNode.append(fr)
        t0 = node[i][1]
        ToNode.append(t0)
        x1.append(x[FromNode[i]-1])
        y1.append(y[FromNode[i]-1])
        x2.append(x[ToNode[i]-1])
        y2.append(y[ToNode[i]-1])
    return x,y,x1,y1,x2,y2,vertx,verty

def plot():
    import matplotlib.pyplot as plot
    global inpname
    x,y,x1,y1,x2,y2,vertx,verty=getNodeCoordinates()
    plot.plot([x1,x2],[y1,y2],'b')
    plot.plot(x,y,'bo')
    plot.title('Inputfile: '+ inpname)
    plot.show()

def getLinkPumpPower():
    global inpname
    file = open(inpname,'r')
    value=[]
    while True:
        s1=file.readline()
        pp = s1.split()
        if s1=="[END]\n":
            return value
        elif len(pp)>3:
            if pp[3]=='POWER' or pp[3]=='power':
                value.append((pp[0],pp[4])) #return pump id with Power value
        elif s1=="[VALVES]\n":
            return value

def getError(ierr):
    return ENtoolkitError(ierr)

class ENtoolkitError(Exception):
    def __init__(self, ierr):
      self.warning= ierr < 100
      self.args= (ierr,)
      self.message= ENgeterror(ierr)
      if self.message=='' and ierr!=0:
         self.message='ENtoolkit Undocumented Error '+str(ierr)+': look at text.h in epanet sources'
    def __str__(self):
      return self.message

EN_ELEVATION     = 0      # /* Node parameters */
EN_BASEDEMAND    = 1
EN_PATTERN       = 2
EN_EMITTER       = 3
EN_INITQUAL      = 4
EN_SOURCEQUAL    = 5
EN_SOURCEPAT     = 6
EN_SOURCETYPE    = 7
EN_TANKLEVEL     = 8
EN_DEMAND        = 9
EN_HEAD          = 10
EN_PRESSURE      = 11
EN_QUALITY       = 12
EN_SOURCEMASS    = 13
EN_INITVOLUME    = 14
EN_MIXMODEL      = 15
EN_MIXZONEVOL    = 16

EN_TANKDIAM      = 17
EN_MINVOLUME     = 18
EN_VOLCURVE      = 19
EN_MINLEVEL      = 20
EN_MAXLEVEL      = 21
EN_MIXFRACTION   = 22
EN_TANK_KBULK    = 23

EN_DIAMETER      = 0      # /* Link parameters */
EN_LENGTH        = 1
EN_ROUGHNESS     = 2
EN_MINORLOSS     = 3
EN_INITSTATUS    = 4
EN_INITSETTING   = 5
EN_KBULK         = 6
EN_KWALL         = 7
EN_FLOW          = 8
EN_VELOCITY      = 9
EN_HEADLOSS      = 10
EN_STATUS        = 11
EN_SETTING       = 12
EN_ENERGY        = 13

EN_DURATION      = 0      # /* Time parameters */
EN_HYDSTEP       = 1
EN_QUALSTEP      = 2
EN_PATTERNSTEP   = 3
EN_PATTERNSTART  = 4
EN_REPORTSTEP    = 5
EN_REPORTSTART   = 6
EN_RULESTEP      = 7
EN_STATISTIC     = 8
EN_PERIODS       = 9

EN_NODECOUNT     = 0      # /* Component counts */
EN_TANKCOUNT     = 1
EN_LINKCOUNT     = 2
EN_PATCOUNT      = 3
EN_CURVECOUNT    = 4
EN_CONTROLCOUNT  = 5

EN_JUNCTION      = 0      # /* Node types */
EN_RESERVOIR     = 1
EN_TANK          = 2

EN_CVPIPE        = 0      # /* Link types */
EN_PIPE          = 1
EN_PUMP          = 2
EN_PRV           = 3
EN_PSV           = 4
EN_PBV           = 5
EN_FCV           = 6
EN_TCV           = 7
EN_GPV           = 8

EN_NONE          = 0      # /* Quality analysis types */
EN_CHEM          = 1
EN_AGE           = 2
EN_TRACE         = 3

EN_CONCEN        = 0      # /* Source quality types */
EN_MASS          = 1
EN_SETPOINT      = 2
EN_FLOWPACED     = 3

EN_CFS           = 0      # /* Flow units types */
EN_GPM           = 1
EN_MGD           = 2
EN_IMGD          = 3
EN_AFD           = 4
EN_LPS           = 5
EN_LPM           = 6
EN_MLD           = 7
EN_CMH           = 8
EN_CMD           = 9

EN_TRIALS        = 0      # /* Misc. options */
EN_ACCURACY      = 1
EN_TOLERANCE     = 2
EN_EMITEXPON     = 3
EN_DEMANDMULT    = 4

EN_LOWLEVEL      = 0      # /* Control types */
EN_HILEVEL       = 1
EN_TIMER         = 2
EN_TIMEOFDAY     = 3

EN_AVERAGE       = 1      # /* Time statistic types.    */
EN_MINIMUM       = 2
EN_MAXIMUM       = 3
EN_RANGE         = 4

EN_MIX1          = 0      # /* Tank mixing models */
EN_MIX2          = 1
EN_FIFO          = 2
EN_LIFO          = 3

EN_NOSAVE        = 0      # /* Save-results-to-file flag */
EN_SAVE          = 1
EN_INITFLOW      = 10     # /* Re-initialize flow flag   */

Open             = 1
Closed           = 0

# Constants for units
FlowUnits= { EN_CFS :"cfs"   ,
             EN_GPM :"gpm"   ,
             EN_MGD :"a-f/d" ,
             EN_IMGD:"mgd"   ,
             EN_AFD :"Imgd"  ,
             EN_LPS :"L/s"   ,
             EN_LPM :"Lpm"   ,
             EN_MLD :"m3/h"  ,
             EN_CMH :"m3/d"  ,
             EN_CMD :"ML/d"  }

# Constants for links
TYPELINK= {  EN_CVPIPE :"CV" ,
             EN_PIPE :"PIPE" ,
             EN_PUMP :"PUMP" ,
             EN_PRV:"PRV"    ,
             EN_PSV :"PSV"   ,
             EN_PBV :"PBV"   ,
             EN_FCV :"FCV"   ,
             EN_TCV :"TCV"   ,
             EN_GPV :"GPV"   }

# Constants for nodes
TYPENODE= {  EN_JUNCTION :"JUNCTION"  ,
             EN_RESERVOIR :"RESERVOIR",
             EN_TANK :"TANK"      }

# Constants for controls
TYPECONTROL= {  EN_LOWLEVEL :"LOWLEVEL"  ,
                EN_HILEVEL :"HIGHLEVEL"  ,
                EN_TIMER :"TIMER"        ,
                EN_TIMEOFDAY :"TIMEOFDAY"}

# Constants for mixing models
TYPEMIXMODEL= { EN_MIX1 :"MIX1" ,
                EN_MIX2 :"MIX2" ,
                EN_FIFO :"FIFO" ,
                EN_LIFO :"LIFO" }

# Constants for quality
TYPEQUALITY= { EN_NONE :"NONE"  ,
               EN_CHEM :"CHEM"  ,
               EN_AGE :"AGE"    ,
               EN_TRACE :"TRACE"}

# Constants for sources
TYPESOURCE= { EN_CONCEN :"CONCEN"      ,
              EN_MASS :"MASS"          ,
              EN_SETPOINT :"SETPOINT"  ,
              EN_FLOWPACED :"FLOWPACED"}

# Constants for statistics
TYPESTATS= { EN_NONE :"NONE"      ,
             EN_AVERAGE :"AVERAGE",
             EN_MINIMUM :"MINIMUM",
             EN_MAXIMUM :"MAXIMUM",
             EN_RANGE :"RANGE"    }