%Author: Mohamed Elbadrashiny
%Date: 04/25/2017
function [words_in_file,string] =readFile(encoding,file_path)
fid = fopen(file_path, 'r');
if(encoding==1)%%Ansi
    string = native2unicode(fgetl(fid));
    string = regexprep(string, '[.!@#$%^&*()_-+=~{};:,<.>?|/''"[]', ' EOP ');
    string = regexprep(string, '[‘÷×’]', ' EOP ');
end
if(encoding==2)%%UTF8
    bytes = fread(fid, '*uint8');
    string = native2unicode(bytes, 'utf8')';
    string = regexprep(string, '\n', ' EOP ');
    string = regexprep(string, '.!.?', ' EOP ');    
end
words_in_file = regexp(string, '(\w+)', 'match');
fclose(fid);
end