function comparativeline(Year, Yields)

% Create figure
figure1 = figure('NumberTitle','off','Name','50 yr');

% Create axes
xtick_labels = [];
axes1 = axes('Parent',figure1,'YMinorTick','on','YGrid','on',...
    'XTick',[2012 2017 2022 2027 2032 2037 2042 2047 2052 2057 2061],...
    'XMinorTick','on');
% Uncomment the following line to preserve the X-limits of the axes
%xlim(axes1,[2012 2061]);
% Uncomment the following line to preserve the Y-limits of the axes
ylim(axes1,[0 35000]);
box(axes1,'on');
hold(axes1,'all');

% Create xlabel
xlabel('Year','FontSize',16);

% Create ylabel
ylabel('Yield (lbs)','FontSize',16);

% Create title
%title('Purchase 20c. of Borbon in Year 5','FontSize',16);

% Create multiple lines using matrix input to plot
plot1 = plot(Year,Yields,'LineWidth',3);
set(plot1(1),...
    'Color',[0.0392156876623631 0.141176477074623 0.415686279535294],...
    'DisplayName','getcolumn(Year vs. Yield,1)');
set(plot1(2),'LineStyle','--',...
    'Color',[0.0784313753247261 0.168627455830574 0.549019634723663],...
    'DisplayName','getcolumn(Year vs. Yield,2)');

