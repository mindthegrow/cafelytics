function data = ImportSurvey(fileToRead1)
% Import the file
pkg load io
sheetName='Relevant Data';
[numbers, strings, raw] = xlsread(fileToRead1, sheetName);
if ~isempty(numbers)
    newData1.data =  numbers;
end

data = newData1.data;

end %end function
