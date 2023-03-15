%% GWSG2ML - assistant rotine
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fid = fopen('folder.txt','wt');
fprintf(fid,'%s',folder_results);
fclose(fid);
%% save parameters to export for python
parameters=[t_tot,time_interval_monitoring,time_interval_history,time_interval_field,pm_u1,pm_u2,size_defect,number_defect]; 
csvwrite('parameters.csv',parameters)
tone_burst
%% run ABAQUS
logical=1;
if logical == 1;
    script = ' script';
else
    script = ' noGUI';
end
pathl=strcat('abaqus cae ',script,'="',folder_files,'\','strips.py','"');
dos(pathl);

%% storage of the signals 
cd(folder_results)
u0= importdata('u0.txt'); 
figure 
hold on
plot(u0.data(:,1),u0.data(:,2))
plot(u0.data(:,1),u0.data(:,3))

%% clear the folder results
dinfo = dir(folder_results);
dinfo([dinfo.isdir]) = [];  
filenames = fullfile(folder_results, {dinfo.name});
delete( filenames{:} )
cd(folder_files)
delete('folder.txt','abaqus.rpy','abaqus_acis.log','parameters.csv','tb.csv')



