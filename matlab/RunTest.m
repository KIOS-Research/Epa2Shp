% Examples
addpath(genpath(pwd));

inpname='networks/Net2_Rossman2000.inp';
Epa2Shp(inpname);

inpname='networks/BWSN1_Ostfeld2008.inp';
Epa2Shp(inpname);

inpname='networks/ky3_Jolly2013.inp';
Epa2Shp(inpname);
    
    
disp('Check folder results.')