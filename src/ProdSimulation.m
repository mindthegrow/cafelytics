function [Year, Yield] = ProdSimulation(data,
                            num_years,
                            PurchaseYear_Borbon,
                            PurchaseYear_Catuai,
                            Intercrop_Catuai,
                            Intercrop_Borbon)
% runs a simulation for r years, stepping through the year n. 
% this simulation tests strategies to minimize yield losses

Borbon=data(1,12); % number of years until full yield
Catuai=data(2,12);
E14=data(3,12);
Catura=data(4,12);

Age=data(:,2);                 % age of plots
Species=data(:,3:6);
Prod=data(:,7:9);              % production data

sz=size(data);
numplots=sz(1); % number of plots
Exp=zeros(numplots,1);         % expected harvest
Year=zeros(num_years,1);
Yield=zeros(num_years,1);
for j=1:num_years
    Year(j)=2011+j;
end

sz=size(data); numplots=sz(1); % number of plots
for n=1:num_years
    % Uncomment the following to simulate early pruning
%     if n==18 
%         data(1,13)=20;
%         data(1,14)=20;
%     elseif n==33 
%         data(1,13)=25;
%         data(1,14)=23;
%     end

    if n==PurchaseYear_Borbon % Purchasing land and planting in year n
        Prod(89,3)=Borbon;
        Age(89)=0;
    end
    if n==PurchaseYear_Catuai % Purchasing land and planting in year n
        Prod(90,3)=Catuai;
        Age(90)=0;
    end
    if n==Intercrop_Catuai % Intercropping Catuai in year n
        data(2,12)=2;
    end
    
    for j=1:numplots % stepping through each plot
        
        if Prod(j,3)==-1 % if tree will start producing in full this year,
            Prod(j,3)=NaN; % set years to prod to blank
            Prod(j,1)=max(Species(j,:)); % set all trees to 'in production'
            Prod(j,2)=0; % set 'out of production' to zero
        elseif Prod(j,3)==0 % if it's a partial harvest year
            Prod(j,1)=Prod(j,1)+Prod(j,2)*(data(5,15)/100); % set to given percentage (decimal value)
        end
        
        % Borbon
        if isnan(Species(j,1))==0                       % check for species
            if mod(Age(j),Borbon+data(1,13)) >= data(1,14)+Borbon % if land is now in decline 
                Prod(j,1)=Prod(j,1)*(1-1/(data(1,13)-data(1,14)));
            end
            if mod(Age(j),Borbon+data(1,13))==0 % if it has been producing for a full cycle,
                Prod(j,2)=Species(j,1);            % set all to out of production
                Prod(j,1)=0;                            % set in production to zero
                Prod(j,3)=Borbon-1;                 % set yrs to prod to value of years until full yield
            end
            Exp(j,n)=Prod(j,1)*data(1,15);
        
        % Catuai   
        elseif isnan(Species(j,2))==0 
            if Age(j)>= Catuai+data(2,14)
                Prod(j,1)=Prod(j,1)*(1-1/(data(2,13)-data(2,14)));
            end
            
            if mod(Age(j),Catuai+data(2,13))==0
                Prod(j,2)=Species(j,2);
                Prod(j,1)=0;
                Prod(j,3)=Catuai-1;
                Age(j)=0; % tree will be replanted this year, NOT cut. Same for species below
                
                % some farmers may want to plant more productive species in this field
                if n>=Intercrop_Borbon && randi(10)<6 %after year n, plant Borbon 
                    Species(j,1)=Species(j,2);
                    Species(j,2)=NaN;
                    Prod(j,3)=Borbon-2;
                    Age(j)=2;
                end
                
            end
            Exp(j,n)=Prod(j,1)*data(2,15);
            
        % E14   
        elseif isnan(Species(j,3))==0 
            if Age(j)>= E14+data(3,14)
                Prod(j,1)=Prod(j,1)*(1-1/(data(3,13)-data(3,14)));
            end
            if mod(Age(j),E14+data(3,13))==0 
               Prod(j,2)=Species(j,3);
               Prod(j,1)=0;
               Prod(j,3)=E14-1; 
               Age(j)=0;
            end
            Exp(j,n)=Prod(j,1)*data(3,15);
            
        % Catura    
        elseif isnan(Species(j,4))==0   
            if Age(j)==Catura+data(4,14)
                Prod(j,1)=Prod(j,1)*(1-1/(data(4,13)-data(4,14)));
            end
            if mod(Age(j),Catura+data(4,13))==0 
                Prod(j,2)=Species(j,4);
                Prod(j,1)=0;
                Prod(j,3)=data(4,12)-1; 
                Age(j)=0;
            end
            Exp(j,n)=Prod(j,1)*data(4,15);
        end
        
        
    end  %end check each plot

Age=Age+1;
Prod(:,3)=Prod(:,3)-1;
end %end year

% Create vector 
for n=1:num_years
    Yield(n,1)=sum(Exp(:,n));
end

end %end function
