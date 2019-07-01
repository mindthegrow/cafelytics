% Load the data from our spreadsheet.
data = ImportSurvey('./data/Farmer Survey (Cleaned Up).xlsx');

% strategic intervention variables
PurchaseYear_Borbon=NaN; PurchaseYear_Catuai=NaN; 
Intercrop_Catuai=NaN; Intercrop_Borbon=NaN; 
num_years = 50;

% create baseline simulation
[Year, Yield_Orig] = ProdSimulation(data, num_years, PurchaseYear_Borbon, PurchaseYear_Catuai, Intercrop_Catuai, Intercrop_Borbon);

% Uncomment following line to purchase land at specified year
%PurchaseYear_Borbon=5;  % 20c. of Borbon
PurchaseYear_Catuai=5; % 20c. of Catuai

% Uncomment following line to intercrop Catuai in declining
% Catuai fields at specified year
%Intercrop_Catuai=5;

% Uncomment following line to start intercropping Borbon in 
% declining Catuai fields at specified year
%Intercrop_Borbon=10;


[Year, Yield] = ProdSimulation(data, num_years, PurchaseYear_Borbon, PurchaseYear_Catuai, Intercrop_Catuai, Intercrop_Borbon);

comparativeline(Year,[Yield_Orig Yield]);
