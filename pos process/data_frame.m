clear all
clc
close all
load signals 
load output
for i=1:size(signals,2)
dt(i,:)= signals(i).u(:,2);
end
writematrix(dt, 'M.txt');
writematrix(output', 'output.txt');


