%% Author: Mohamed Elbadrashiny
%% Date: 05/13/2017
function align(inDir, outDir)

%% creating a working directory
workingDirectory='workingDirectory';
if exist(workingDirectory, 'dir')
  rmdir (workingDirectory, 's');
end
mkdir (workingDirectory);

%% creating the output directory
if exist(outDir, 'dir')
  rmdir (outDir, 's');
end
mkdir (outDir);

%% Reading the files from the input directory
filesPaths = dir(inDir);
for i=1:length(filesPaths)
    fileName=filesPaths(i).name;
    tmp=strfind(filesPaths(i).name,'.');
    if(~isempty(tmp) && tmp(1)==1)%%this is the root pointer of the directory. We will skip it
        continue;
    end
    [lines,points,counterPoints]=loadFile(strcat(inDir,'/',fileName));
    restrictedList{1}=points;
    restrictedList{2}=counterPoints;    
    if (mod(length(lines),2) == 0)% i.e. even number. Whic means that the points # = counterpoints #
        tmpPaths='lines_paths.txt';
        exportLines(lines,workingDirectory, tmpPaths);%% write each setnece in a seprate file before sending them to xSim clustering algorithm
        [clusters,similarityMat]=xSim(tmpPaths, 2, 1,restrictedList);%% 2 means utf8 encoding and 1 means use 1-gram
        cleanUp(tmpPaths,workingDirectory); %% empty the working direcroty and delete the lines_paths.txt
        exportClusters(similarityMat,clusters(:,1:2), strcat(outDir,'/',fileName),length(lines)); %% write the creatued clusters into the output file
    end 
end
end

%% Load file into lines and remove the prefix:
%  Point:
%  Counterpoint:
function [lines,points,counterPoints] =loadFile(filePath)
fid=fopen(filePath);
i=1;
points=[];
counterPoints=[];
while 1
    tline = fgetl(fid);
    if ~ischar(tline),   break,   end
    tline = regexprep(tline, '^[Pp]oint\s?:\s?', '');    
    tmp = regexprep(tline, '^[Cc]ounterpoint\s?:\s?', '');
    if(length(tmp)<length(tline)) %%i.e. Counterpoint
        counterPoints=[counterPoints;i];
    else %% i.e. point
        points=[points;i];
    end
    tline=tmp;
    lines{i} = strtrim(tline);
    i=i+1;
end
fclose(fid);
end

%% Export lines into files for xSim
function exportLines(lines,dirPath,pointsPaths)

fid=fopen(pointsPaths,'wt');
phrases_paths=cell(length(lines));
for i=1:length(lines)
    phrases_paths{i}=strcat(dirPath,'/',int2str(i),'.txt');
    fprintf(fid,'%s\n',phrases_paths{i});
    fp=fopen(phrases_paths{i},'wt');
    fprintf(fp,'%s',lines{i});
    fclose(fp);    
end
fclose(fid);
end

%% clean the working direcorty and the temp paths file
function cleanUp(tmpPaths,workingDirectory)
delete(tmpPaths);
if exist(workingDirectory, 'dir')
  rmdir (workingDirectory, 's');
end
mkdir (workingDirectory);
end

%% Export the created clusters into the output file
function exportClusters(similarityMat,clusters, outFile,pointsNo)
[m,n]=size(clusters);
clusters=[clusters zeros(m,4)];%% We added 4 columns as follwos:
                                              %1st column: 1 if the cluster contains 2 sentences, 0 if one sentence and one cluster, and -1 if 2 clusters
                                              %2nd column: if the 1st column is 0, this clolumn will contain the column index that contains the sentence
                                              %3rd column: if the 1st column is 0, this clolumn will contain the column index that contains the cluster
                                              %4th cloumn: if the 1st column is 0, this clolumn indicates if this point is connected to other point or not. 1 if connected and 0 if not 
for i=1:m
    if (clusters(i,1)<=pointsNo && clusters(i,2)<=pointsNo)%%i.e. 2 sentences;                                                            
        clusters(i,3)=1;
    elseif (clusters(i,1)>pointsNo && clusters(i,2)>pointsNo)%% i.e. 2 clusters
        clusters(i,3)=-1;
    else %% i.e one point and one cluster
        clusters(i,3)=0;        
        if(clusters(i,1)<=pointsNo)
            clusters(i,4)=1;
            clusters(i,5)=2;
        else
            clusters(i,4)=2;
            clusters(i,5)=1;
        end
        clusters(i,6)=0; %initialize by "not yet connected"
    end    
end
fid=fopen(outFile,'wt');
for i=1:m
     if (clusters(i,3)==1)%%i.e. 2 sentences;                                                      
        fprintf(fid,'%s\t%s\n',int2str(clusters(i,1)), int2str(clusters(i,2)));
     elseif(clusters(i,3)==0 && clusters(i,6)==0) %% i.e. ones sentence and one cluster and the sentence is not yet connected
             currentPoint=clusters(i,clusters(i,4));
             nextCluster=clusters(i,clusters(i,5))-pointsNo;%%Now this cluster is pointing to the row that contains this cluster
             [clusters,match]=findMatch(similarityMat,pointsNo,clusters,currentPoint,nextCluster);
             if(match~=-1)
                 clusters(i,6)=1;%% the point is now connected
                 fprintf(fid,'%s\t%s\n',int2str(clusters(i,clusters(i,4))), int2str(match));
             end
     end    
end
fclose(fid);
end

%% applis breadth first tree search to find the first empty child to match with
function [clusters,match]=findMatch(similarityMat,pointsNo,clusters,originalPoint,nextCluster)
    if(clusters(nextCluster,3)==1)%%i.e. 2 points and already connected together
        match=-1;
    elseif(clusters(nextCluster,3)==0)%% i.e. 1 point and one cluster
        if(clusters(nextCluster,6)==0)%% i.e. the sentence is not connected
            newPoint=clusters(nextCluster,clusters(nextCluster,4));
            if(similarityMat(originalPoint,newPoint)~=9)%% if the similarity distance is not 9, this means these 2 points can be together
                match=newPoint;
                clusters(nextCluster,6)=1;%% i.e. th point is connected now
            else%%i.e. there is a restriction on these 2 sentences to be together. So we will search under the cluster
                nextCluster=clusters(nextCluster,clusters(nextCluster,5))-pointsNo;%%Now this cluster is pointing to the row that contains this cluster
                [clusters,match]=findMatch(similarityMat,pointsNo,clusters,originalPoint,nextCluster);
            end
        else%% i.e. the sentence in this cluster is already connected. So we will search under the cluster
             nextCluster=clusters(nextCluster,clusters(nextCluster,5))-pointsNo;%%Now this cluster is pointing to the row that contains this cluster
             [clusters,match]=findMatch(similarityMat,pointsNo,clusters,originalPoint,nextCluster);
        end
    elseif(clusters(nextCluster,3)==-1)%% i.e. 2 clusters
        leftCluster=clusters(nextCluster,1)-pointsNo;
        rightCluster=clusters(nextCluster,2)-pointsNo;
        [clusters,match]=findMatch(similarityMat,pointsNo,clusters,originalPoint,leftCluster);
        if(match==-1)%%i.e. no match found
            [clusters,match]=findMatch(similarityMat,pointsNo,clusters,originalPoint,rightCluster);
        end        
    end
end