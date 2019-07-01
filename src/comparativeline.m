function comparativeline(Year, Yields)

xtick_labels = [];
numYears = size(Year,1);
for y=1:5:numYears
    xtick_labels(end+1) = Year(y);
end

figure1 = figure('NumberTitle','off','Name',sprintf('%d yr', numYears));

% Create axes
axes1 = axes('Parent',figure1,...
             'YMinorTick','on',...
             'YGrid','on',...
             'XGrid', 'on',...
             'gridalpha', 0.5,...
             'XTick',xtick_labels,...
             'XMinorTick','on');

% Uncomment the following line to preserve the Y-limits of the axes
ylim(axes1,[0 35000]);
box(axes1,'on');
hold(axes1,'all');

% Create xlabel
xlabel('Year','FontSize',16);

% Create ylabel
ylabel('Yield (lbs)','FontSize',16);

% Create title [TODO: Automatic Title based on Strategy]
%title('Purchase 20c. of Borbon in Year 5','FontSize',16);

colors = ['blue'; 'red'; 'black'; 'cyan'];
linestyles = {"-", "-"};
linewidths = [5, 3, 2, 1];
% Create multiple lines using matrix input to plot
plot1 = plot(Year,Yields);
for i=1:size(Yields,2)
    displayName = sprintf('getcolumn(Year vs. Yield,%d)',i);
    ls = mod(i+1,2);
    if i==1
        c = 1;
    else
        c = 2;
    end
    set(plot1(i),...
        'LineStyle', linestyles{1+ls},...
        'Color', colors(c),...
        'LineWidth', linewidths(1+ls),...
        'DisplayName', displayName);
end

end