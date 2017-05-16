%% Author: Mohamed Elbadrashiny
%%Date: 05/14/2017
function summarize(inFile, OutFile)
%% creating a working directory
workingDirectory='workingDirectory';
if exist(workingDirectory, 'dir')
  rmdir (workingDirectory, 's');
end
mkdir (workingDirectory);

%% summarizing the inout file
lines=loadFile(inFile);
tmpPaths='lines_paths.txt';
exportLines(lines,workingDirectory, tmpPaths);%% write each setnece in a seprate file before sending them to xSim clustering algorithm
clusters=xSim(tmpPaths, 2, 1,{});
cleanUp(tmpPaths,workingDirectory); %% empty the working direcroty and delete the lines_paths.txt
exportSummary(clusters(:,1:2), OutFile,lines); %% analyse the clusters and export the summary into the output file

end




%% Load file into lines and remove the prefix:
%  Point:
%  Counterpoint:
function [lines] =loadFile(filePath)
fid=fopen(filePath);
i=1;
while 1
    tline = fgetl(fid);
    if ~ischar(tline),   break,   end
    tline = regexprep(tline, '^Point: ', '');
    tline = regexprep(tline, '^Counterpoint: ', '');
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
function exportSummary(clusters, outFile, sentences)
sentencesNo=length(sentences);
fid=fopen(outFile,'wt');
[m,n]=size(clusters);
for i=1:m
    
    %% if 2 lines are found in the same cluster. this means they are redundants.
    %  So we remove the shorter line since it has fewer information
    if (clusters(i,1)<=sentencesNo && clusters(i,2)<=sentencesNo)%%i.e. 2 lines;
                                                           %%Not 2 clusters or (one line and one cluster)
        firstSent=sentences{clusters(i,1)};
        secondSent=sentences{clusters(i,2)};        
        if(length(firstSent) < length(secondSent))
            fprintf(fid,'%s\n',secondSent);
        else
            fprintf(fid,'%s\n',firstSent);
        end
    %% if 2 clusters are connected together, we do nothing    
    elseif (clusters(i,1)>sentencesNo && clusters(i,2)>sentencesNo)%% i.e. 2 clusters
        continue;
    %% if 1 line and 1 cluster, we export the line becuase it has differnt inofrmation 
    %  than the points in the cluster
    elseif (clusters(i,1)<=sentencesNo)
        fprintf(fid,'%s\n',sentences{clusters(i,1)});
    elseif (clusters(i,2)<=sentencesNo)
        fprintf(fid,'%s\n',sentences{clusters(i,2)});
    end
end
fclose(fid);
end
