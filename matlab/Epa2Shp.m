function Epa2Shp(inpname)
% which -all mapgate
    format long g;
    d=epanet(inpname);
    warning off;
    Sjunctions=struct;
    Spipes=struct;
    Svalves=struct;
    Spumps=struct;
    Stanks=struct;
    Sreservoirs=struct;
    
    % Write Junction Shapefile
    ndcoords=d.getNodeCoordinates;
    if d.NodeJunctionCount
        for i=1:d.NodeJunctionCount
            Sjunctions(i).('ID')=d.NodeNameID{i};
            Sjunctions(i).('Elevation')=d.NodeElevations(i);
            for u=1:length(d.NodeBaseDemands)
                Sjunctions(i).(['Demand',num2str(u)])=d.NodeBaseDemands{u}(i);
                if ~isempty(d.getPatternNameID{1})
                    if ~isempty(d.NodeDemandPatternNameID{u})
                        Sjunctions(i).(['Pattern',num2str(u)])=d.NodeDemandPatternNameID{u};
                    else
                        Sjunctions(i).(['Pattern',num2str(u)])='None';
                    end
                else
                    Sjunctions(i).(['Pattern',num2str(u)])='None';
                end
            end
            Sjunctions(i).X=ndcoords{1}(i);
            Sjunctions(i).Y=ndcoords{2}(i);
            Sjunctions(i).Geometry='Point';
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Sjunctions, ['results/',f,'_junctions.shp']);
    end
    % Write Pipe Shapefile

    if d.LinkCount
        mm=0;qq=0;
        for i=1:d.LinkCount %d.LinkPipeCount
            if sum(i==d.LinkPumpIndex)
                for p=i+mm:i+1+mm
                    if p==i+mm
                        Spipes(p).('ID')=[d.LinkNameID{p-mm},'_pump1'];
                        Spipes(p).('NodeFrom')=d.NodesConnectingLinksID{p-mm,1};
                        Spipes(p).('NodeTo')=Spipes(p).('ID');
                        indN1 = d.getNodeIndex(Spipes(p).('NodeFrom'));
                        indN2 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm,2));

                        Spipes(p).X=[ndcoords{1}(indN1) sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2];
                        Spipes(p).Y=[ndcoords{2}(indN1) sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2];                        
                        
                    elseif p==i+1+mm
                        Spipes(p).('ID')=[d.LinkNameID{p-mm-1},'_pump2'];
                        Spipes(p).('NodeFrom')=Spipes(p).('ID');
                        Spipes(p).('NodeTo')=d.NodesConnectingLinksID{p-1-mm,2};
                        indN1 = d.getNodeIndex(d.NodesConnectingLinksID(p-1-mm,1));
                        indN2 = d.getNodeIndex(Spipes(p).('NodeTo'));

                        Spipes(p).X=[(sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2) ndcoords{1}(indN2)];
                        Spipes(p).Y=[(sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2) ndcoords{2}(indN2)];                        
                    end
                    Spipes(p).('Status')='Open';
                    Spipes(p).('Length')=0;
                    Spipes(p).('Diameter')=0;
                    Spipes(p).('Roughness')=0;
                    Spipes(p).('MinorLoss')=0;    
                    Spipes(p).Geometry='Line';
                end
                mm=mm+1;
            elseif sum(i==d.LinkValveIndex)
                for p=i+mm+qq:i+mm+qq+1
                    if p==i+mm+qq
                        Spipes(p).('ID')=[d.LinkNameID{p-mm-qq},'_valve1'];
                        Spipes(p).('NodeFrom')=d.NodesConnectingLinksID{p-mm-qq,1};
                        Spipes(p).('NodeTo')=Spipes(p).('ID');
                        indN1 = d.getNodeIndex(Spipes(p).('NodeFrom'));
                        indN2 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm-qq,2));

                        Spipes(p).X=[ndcoords{1}(indN1) sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2];
                        Spipes(p).Y=[ndcoords{2}(indN1) sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2];                        
                        
                    elseif p==i+mm+1+qq
                        Spipes(p).('ID')=[d.LinkNameID{p-mm-qq-1},'_valve2'];
                        Spipes(p).('NodeFrom')=Spipes(p).('ID');
                        Spipes(p).('NodeTo')=d.NodesConnectingLinksID{p-mm-qq-1,2};
                        indN1 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm-qq-1,1));
                        indN2 = d.getNodeIndex(Spipes(p).('NodeTo'));

                        Spipes(p).X=[(sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2) ndcoords{1}(indN2)];
                        Spipes(p).Y=[(sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2) ndcoords{2}(indN2)];                        
                    end
                    Spipes(p).('Status')='Open';
                    Spipes(p).('Length')=0;
                    Spipes(p).('Diameter')=0;
                    Spipes(p).('Roughness')=0;
                    Spipes(p).('MinorLoss')=0;    
                    Spipes(p).Geometry='Line';
                end
                qq=qq+1;
            else
                Spipes(i).('ID')=d.LinkNameID{i};
                Spipes(i).('NodeFrom')=d.NodesConnectingLinksID{i,1};
                Spipes(i).('NodeTo')=d.NodesConnectingLinksID{i,2};
                if d.LinkInitialStatus(i)==1
                    Spipes(i).('Status')='Open';
                else
                    Spipes(i).('Status')='Closed';
                end
                Spipes(i).('Length')=d.LinkLength(i);
                Spipes(i).('Diameter')=d.LinkDiameter(i);
                Spipes(i).('Roughness')=d.LinkRoughnessCoeff(i);
                Spipes(i).('MinorLoss')=d.LinkMinorLossCoeff(i);

                indN1 = d.getNodeIndex(Spipes(i).('NodeFrom'));
                indN2 = d.getNodeIndex(Spipes(i).('NodeTo'));

                % Coordinates for pipes
                Spipes(i).X=[ndcoords{1}(indN1) ndcoords{3}{i} ndcoords{1}(indN2) ];
                Spipes(i).Y=[ndcoords{2}(indN1) ndcoords{4}{i} ndcoords{2}(indN2) ];
                Spipes(i).Geometry='Line';
            end
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Spipes, ['results/',f,'_pipes.shp']);
    end
    % Write Tank Shapefile

    if d.NodeTankCount
        u=1;
        for i=d.getNodeTankIndex
            Stanks(u).('ID')=d.NodeNameID{i};        
            Stanks(u).('Elevation')=d.NodeElevations(i);
            Stanks(u).('InitLevel')=d.NodeTankInitialLevel(i);
            Stanks(u).('MinLevel')=d.NodeTankMinimumWaterLevel(i);
            Stanks(u).('MaxLevel')=d.NodeTankMaximumWaterLevel(i);
            Stanks(u).('Diameter')=d.NodeTankDiameter(i);
            Stanks(u).('MinVolume')=d.NodeTankMinimumWaterVolume(i);
            Stanks(u).('VolumeCurve')=d.NodeTankVolumeCurveIndex(i);

            % Coordinates for tanks
            Stanks(u).X=ndcoords{1}(i);
            Stanks(u).Y=ndcoords{2}(i);

            Stanks(u).Geometry='Point';
            u=u+1;
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Stanks, ['results/',f,'_tanks.shp']);
    end
    % Write Reservoir Shapefile
        
    if d.NodeReservoirCount
        u=1;
        for i=d.getNodeReservoirIndex
            Sreservoirs(u).('ID')=d.NodeNameID{i};        
            Sreservoirs(u).('Head')=d.NodeElevations(i);

            % Coordinates for reservoirs
            Sreservoirs(u).X=ndcoords{1}(i);
            Sreservoirs(u).Y=ndcoords{2}(i);

            Sreservoirs(u).Geometry='Point';
            u=u+1;
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Sreservoirs, ['results/',f,'_reservoirs.shp']);
    end
    
    % Write Pump Shapefile
    if d.LinkPumpCount
        u=1;
        ch=0;
        for i=d.getLinkPumpIndex
            Head='';Flow=''; 
            Spumps(u).('ID')=d.LinkNameID{i};        
            Spumps(u).('NodeFrom')=d.NodesConnectingLinksID{i,1};
            Spumps(u).('NodeTo')=d.NodesConnectingLinksID{i,2};
            headIndex = d.getHeadCurveIndex;
            if sum(headIndex)==0
                Spumps(u).Head=Head;
                Spumps(u).Flow=Flow;
                Spumps(u).Curve='';
                if ch==0
                    linksInfo=d.getBinLinksInfo;
                    ch=1;
                end
                Spumps(u).Power=linksInfo.BinLinkPumpPower(u);
            else
                curveXY = d.getCurveXY(headIndex(u));

                for p=1:length(curveXY(:,1))
                    Head = curveXY(p,1);
                    Flow = curveXY(p,2);
                    Spumps(u).(['Head',num2str(p)])=Head;
                    Spumps(u).(['Flow',num2str(p)])=Flow;
                end
                Spumps(u).Power=0;
                Spumps(u).Curve=d.getCurveNameID(headIndex(u));
            end
            indN1 = d.getNodeIndex(Spumps(u).('NodeFrom'));
            indN2 = d.getNodeIndex(Spumps(u).('NodeTo'));

            % Coordinates for pipes
            Spumps(u).X=sum([ndcoords{1}(indN1) ndcoords{3}{i} ndcoords{1}(indN2) ])/2;
            Spumps(u).Y=sum([ndcoords{2}(indN1) ndcoords{4}{i} ndcoords{2}(indN2) ])/2;

            Spumps(u).Geometry='Point';
            u=u+1;
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Spumps, ['results/',f,'_pumps.shp']);
    end
    % Write Valve Shapefile

    if d.LinkValveCount
        u=1;
        for i=d.getLinkValveIndex
            Svalves(u).('ID')=d.LinkNameID{i};        
            Svalves(u).('NodeFrom')=d.NodesConnectingLinksID{i,1};
            Svalves(u).('NodeTo')=d.NodesConnectingLinksID{i,2};

            Svalves(u).('Diameter')=d.LinkDiameter(i);
            Svalves(u).('Type')=d.LinkType{i};
            Svalves(u).('Setting')=d.LinkInitialSetting(i);
            Svalves(u).('MinorLoss')=d.LinkMinorLossCoeff(i);

            indN1 = d.getNodeIndex(Svalves(u).('NodeFrom'));
            indN2 = d.getNodeIndex(Svalves(u).('NodeTo'));

            % Coordinates for pipes
            Svalves(u).X=sum([ndcoords{1}(indN1) ndcoords{3}{i} ndcoords{1}(indN2) ])/2;
            Svalves(u).Y=sum([ndcoords{2}(indN1) ndcoords{4}{i} ndcoords{2}(indN2) ])/2;

            Svalves(u).Geometry='Point';
            u=u+1;
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Svalves, ['results/',f,'_valves.shp']);
    end
    d.unload;
    warning on;
