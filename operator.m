%% GWSG2ML - assistant rotine
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
j=0;
for k=1:size(number_defect,2)
for l=1:2
fid = fopen('folder.txt','wt');
fprintf(fid,'%s',folder_results);
fclose(fid);
%% save parameters to export for python

cd(folder_files)
parameters=[t_tot,time_interval_monitoring,time_interval_history,time_interval_field,pm_u1,pm_u2,size_defect,number_defect(k)]; 
csvwrite('parameters.csv',parameters)
tone_burst
%% run ABAQUS
logical=0;
if logical == 1;
    script = ' script';
else
    script = ' noGUI';
end
pathl=strcat('abaqus cae ',script,'="',folder_files,'\','strips.py','"');

rr=1;
while rr>0
clear rr 
dos(pathl);
rr=ans;
end

%% storage of the signals 
cd(folder_results)
u0= importdata('u0.txt'); 
figure 
hold on
plot(u0.data(:,1),u0.data(:,2))
plot(u0.data(:,1),u0.data(:,3))

j=j+1;

cd('C:\Users\Groth\Desktop\models_ml\Golden eggs chicken\plane_strip\pos process')
signals(j).u=u0.data;
output(j)=outputs(k);
%% clear the folder results
dinfo = dir(folder_results);
dinfo([dinfo.isdir]) = [];  
filenames = fullfile(folder_results, {dinfo.name});
delete( filenames{:} )
save('signals')
save('output')
cd(folder_files)
delete('folder.txt','abaqus.rpy','abaqus_acis.log','parameters.csv','tb.csv')
end
end

