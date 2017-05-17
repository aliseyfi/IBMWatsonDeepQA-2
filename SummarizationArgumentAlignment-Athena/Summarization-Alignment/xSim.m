%Author: Mohamed Elbadrashiny
%Date: 04/25/2017
function [Z,SR]=xSim(pahts, encoding, nGram_size, restrictedList)
%if encoding=1 ==> Ansi
%if encoding=2 ==> UTF8
% Files_Location=Read_Paths('paths.txt');
%nGram_size=1;
Files_Location=Read_Paths(pahts);
No_of_training_files = length(Files_Location);

%%%%%%%%%%%%%%%%Building the Occurrence Matrix (M)%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%where each row in this matrix represents a single document and each
%%%column represents a single word and each cell(i,j) represents the number of
%%%occurence of word number (j) in the document number (i)
words = [];
for i=1:No_of_training_files
    words_in_file=readFile(encoding,Files_Location{i});
    R=reshape_ngram(words_in_file,nGram_size);
    All_Files{i}=Strcat_ngram(R,nGram_size);   
    words = [words All_Files{i}'];   
end
unique_words = unique(words);
no_of_unique_words =  length(unique_words);
Occurrence_Matrix_temp = zeros(no_of_unique_words,No_of_training_files);

for i=1:No_of_training_files
  Occurrence_Matrix_temp(:,i) = Occurrence_Matrix_temp(:,i) + FileToWordCount(All_Files{i}, unique_words);  
end

M=Occurrence_Matrix_temp;
number_of_words_per_each_document=sum(M);
M=M';
word_count_for_all_documents=sum(M);

%%%%%%%%%%%%%%%%%%%%%%calculating the similarity matrix using X-sim algorithm%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% where the number is high when the similarity is high
%%%%%%%%%%%%%%%%%%%%%%1- initialization %%%
SR=eye(No_of_training_files); %%Documents similarity matrix
% SC=eye(no_of_unique_words-1);   %%Words similarity matrix
SC=eye(no_of_unique_words);   %%Words similarity matrix

NR=repmat(number_of_words_per_each_document,No_of_training_files,1);
NR=(NR.*NR').^(-1);

% NC=repmat(word_count_for_all_documents,no_of_unique_words-1,1);
NC=repmat(word_count_for_all_documents,no_of_unique_words,1);
NC=(NC.*NC').^(-1);

%%%%%%%%%%%%%%%%%%%%%%2- Iterations %%%
for i=1:4
    SR_t=SR;
    SC_t=SC;
    SR=(M*SC_t*M').*NR;
    SC=(M'*SR_t*M).*NC;
    %%%% setting the diagonal with 1%%%%
    SR(logical(eye(size(SR)))) = 1;
    SC(logical(eye(size(SC)))) = 1;
end
%%%%%%%%%%%%%%%%%%%%%%calculating the dissimilarity matrix %%%%%%%%%%%%%%%%%%%%%%%%%%%
%% where the number is low when the similarity is high
SR=1-SR;
SR=restrict(SR,restrictedList);%% maximize the distance between the points in the restricted list

%%%%%%%%%%%%%%%Agglomerative hierarchical cluster tree%%%%%%%%%%%%%%%%%%%%%%
Y=squareform(SR);
Z = linkage(Y);

%% Uncomment if you want to see the clusters tree
%[H,T,perm] =dendrogram(Z);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function Files_Location=Read_Paths(paths)
fid=fopen(paths);
i=1;
while 1
    tline = fgetl(fid);
    if ~ischar(tline),   break,   end
    Files_Location{i} = tline;
    i=i+1;
end
fclose(fid);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function v = FileToWordCount(File, unique_words)
%F=reshape_ngram(File,nGram_size);
%F=Strcat_ngram(F,nGram_size);
v = zeros(length(unique_words),1);
for j=1:length(File)
    k = strmatch(File(j), unique_words, 'exact');
    v(k) = v(k) + 1;
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function r=reshape_ngram(words,nGram_size)
words=words';
L=length(words);
for i=1:nGram_size
    
    r(:,i)=words(i:L-nGram_size+i,1);
    
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function u=unique_ngram(words,nGram_size)
u=Strcat_ngram(words,nGram_size);
u=unique(u);
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
function S=Strcat_ngram(words,nGram_size)
S=words(:,1);
for i=2:nGram_size
    S=strcat(S,words(:,i));
end
end
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% Maximize the distance between the points in the restricted list
function simMat=restrict(simMat,restrictedList)
    for i=1:length(restrictedList) %% restrictedList may contain multiple lists
        list=restrictedList{i};
        for j=1:length(list)
            for k=j+1:length(list)
                simMat(list(j),list(k))=9;%% big distance
                simMat(list(k),list(j))=9;%% becuase this matrix is symmetric 
            end
        end
    end
    
end
