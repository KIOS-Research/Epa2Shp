function Epa2Shp(inpname)
% which -all mapgate
    format long g;
    d=epanet(inpname);
    warning off;

    % Write Junction Shapefile
    load templates/Sjunctions.0 'Sjunctions' -mat

    ndcoords=d.getNodeCoordinates;
    if d.NodeJunctionCount
        for i=1:d.NodeJunctionCount
            Sjunctions(i).demand=d.NodeBaseDemands{1}(i);
            Sjunctions(i).elevation=d.NodeElevations(i);
            Sjunctions(i).dc_id=d.NodeNameID{i};
            if ~isempty(d.getPatternNameID{1})
                if ~isempty(d.NodeDemandPatternNameID{i})
                    Sjunctions(i).pattern=d.NodeDemandPatternNameID{i};
                else
                    Sjunctions(i).pattern='None';
                end
            else
                Sjunctions(i).pattern='None';
            end
            Sjunctions(i).X=ndcoords{1}(i);
            Sjunctions(i).Y=ndcoords{2}(i);
            Sjunctions(i).Geometry='Point';
        end
        [~,f]=fileparts(d.inputfile);
        shapewrite(Sjunctions, ['results/',f,'_junctions.shp']);
    end
    % Write Pipe Shapefile
    load templates/Spipes.0 'Spipes' -mat

    if d.LinkCount
        mm=0;qq=0;
        for i=1:d.LinkCount %d.LinkPipeCount
            if sum(i==d.LinkPumpIndex)
                for p=i+mm:i+1+mm
                    if p==i+mm
                        Spipes(p).dc_id=[d.LinkNameID{p-mm},'_pump1'];
                        Spipes(p).node1=d.NodesConnectingLinksID{p-mm,1};
                        Spipes(p).node2=Spipes(p).dc_id;
                        indN1 = d.getNodeIndex(Spipes(p).node1);
                        indN2 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm,2));

                        Spipes(p).X=[ndcoords{1}(indN1) sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2];
                        Spipes(p).Y=[ndcoords{2}(indN1) sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2];                        
                        
                    elseif p==i+1+mm
                        Spipes(p).dc_id=[d.LinkNameID{p-mm-1},'_pump2'];
                        Spipes(p).node1=Spipes(p).dc_id;
                        Spipes(p).node2=d.NodesConnectingLinksID{p-1-mm,2};
                        indN1 = d.getNodeIndex(d.NodesConnectingLinksID(p-1-mm,1));
                        indN2 = d.getNodeIndex(Spipes(p).node2);

                        Spipes(p).X=[(sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2) ndcoords{1}(indN2)];
                        Spipes(p).Y=[(sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2) ndcoords{2}(indN2)];                        
                    end
                    Spipes(p).status='Open';
                    Spipes(p).length=0;
                    Spipes(p).diameter=0;
                    Spipes(p).roughness=0;
                    Spipes(p).minorloss=0;    
                    Spipes(p).Geometry='Line';
                end
                mm=mm+1;
            elseif sum(i==d.LinkValveIndex)
                for p=i+mm+qq:i+mm+qq+1
                    if p==i+mm+qq
                        Spipes(p).dc_id=[d.LinkNameID{p-mm-qq},'_valve1'];
                        Spipes(p).node1=d.NodesConnectingLinksID{p-mm-qq,1};
                        Spipes(p).node2=Spipes(p).dc_id;
                        indN1 = d.getNodeIndex(Spipes(p).node1);
                        indN2 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm-qq,2));

                        Spipes(p).X=[ndcoords{1}(indN1) sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2];
                        Spipes(p).Y=[ndcoords{2}(indN1) sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2];                        
                        
                    elseif p==i+mm+1+qq
                        Spipes(p).dc_id=[d.LinkNameID{p-mm-qq-1},'_valve2'];
                        Spipes(p).node1=Spipes(p).dc_id;
                        Spipes(p).node2=d.NodesConnectingLinksID{p-mm-qq-1,2};
                        indN1 = d.getNodeIndex(d.NodesConnectingLinksID(p-mm-qq-1,1));
                        indN2 = d.getNodeIndex(Spipes(p).node2);

                        Spipes(p).X=[(sum([ndcoords{1}(indN1) ndcoords{1}(indN2)])/2) ndcoords{1}(indN2)];
                        Spipes(p).Y=[(sum([ndcoords{2}(indN1) ndcoords{2}(indN2)])/2) ndcoords{2}(indN2)];                        
                    end
                    Spipes(p).status='Open';
                    Spipes(p).length=0;
                    Spipes(p).diameter=0;
                    Spipes(p).roughness=0;
                    Spipes(p).minorloss=0;    
                    Spipes(p).Geometry='Line';
                end
                qq=qq+1;
            else
                Spipes(i).dc_id=d.LinkNameID{i};
                Spipes(i).node1=d.NodesConnectingLinksID{i,1};
                Spipes(i).node2=d.NodesConnectingLinksID{i,2};
                if d.LinkInitialStatus(i)==1
                    Spipes(i).status='Open';
                else
                    Spipes(i).status='Closed';
                end
                Spipes(i).length=d.LinkLength(i);
                Spipes(i).diameter=d.LinkDiameter(i);
                Spipes(i).roughness=d.LinkRoughnessCoeff(i);
                Spipes(i).minorloss=d.LinkMinorLossCoeff(i);

                indN1 = d.getNodeIndex(Spipes(i).node1);
                indN2 = d.getNodeIndex(Spipes(i).node2);

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
    load templates/Stanks.0 'Stanks' -mat

    if d.NodeTankCount
        u=1;
        for i=d.getNodeTankIndex
            Stanks(u).dc_id=d.NodeNameID{i};        
            Stanks(u).elevation=d.NodeElevations(i);
            Stanks(u).initiallev=d.NodeTankInitialLevel(i);
            Stanks(u).minimumlev=d.NodeTankMinimumWaterLevel(i);
            Stanks(u).maximumlev=d.NodeTankMaximumWaterLevel(i);
            Stanks(u).diameter=d.NodeTankDiameter(i);
            Stanks(u).minimumvol=d.NodeTankMinimumWaterVolume(i);
            Stanks(u).volumecurv=d.NodeTankVolumeCurveIndex(i);

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
    
    load templates/Sreservoirs.0 'Sreservoirs' -mat
    
    if d.NodeReservoirCount
        u=1;
        for i=d.getNodeReservoirIndex
            Sreservoirs(u).dc_id=d.NodeNameID{i};        
            Sreservoirs(u).head=d.NodeElevations(i);

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
    load templates/Spumps.0 'Spumps' -mat


    if d.LinkPumpCount
        u=1;
        ch=0;
        for i=d.getLinkPumpIndex
            Head='';Flow='';Power='';
            Spumps(u).dc_id=d.LinkNameID{i};        
            Spumps(u).node1=d.NodesConnectingLinksID{i,1};
            Spumps(u).node2=d.NodesConnectingLinksID{i,2};
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
                    Head = [Head,' ', num2str(curveXY(p,1))];
                    Flow = [Flow,' ', num2str(curveXY(p,2))];
                end

                Spumps(u).Head=Head;
                Spumps(u).Flow=Flow;
                Spumps(u).Curve=d.getCurveNameID(headIndex(u));
            end
            indN1 = d.getNodeIndex(Spumps(u).node1);
            indN2 = d.getNodeIndex(Spumps(u).node2);

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
    load templates/Svalves.0 'Svalves' -mat

    if d.LinkValveCount
        u=1;
        for i=d.getLinkValveIndex
            Svalves(u).dc_id=d.LinkNameID{i};        
            Svalves(u).node1=d.NodesConnectingLinksID{i,1};
            Svalves(u).node2=d.NodesConnectingLinksID{i,2};

            Svalves(u).diameter=d.LinkDiameter(i);
            Svalves(u).type=d.LinkType(i);
            Svalves(u).setting=d.LinkInitialSetting(i);
            Svalves(u).minorloss=d.LinkMinorLossCoeff(i);

            indN1 = d.getNodeIndex(Svalves(u).node1);
            indN2 = d.getNodeIndex(Svalves(u).node2);

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
