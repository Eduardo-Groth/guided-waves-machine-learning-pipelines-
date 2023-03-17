%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%%%%%%%% GWSG2ML %%%%%%%%%%%%%%%  script by Eduardo Becker Groth
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
clc, clear all, close all
%% requeired infomation
t_tot=1e-3 ;                    % total time of simulation
time_interval_monitoring=1e-7;  % acquire step of monitoring signal(s) 
time_interval_history=5e-7;     % acquire step of default history data storage 
time_interval_field=0.5e-4;     % acquire step of defauld field data storage (use to do .gif and pictures)
pm_u1=1e-6;                     % initial excitation motion amplitud in x direction
pm_u2=0;                        % initial excitation motion apmlitud in y direction 
size_defect=0.5e-3;             % defect size (radius)
number_defect=[5,30,50];               % number of defects in the model

frequency=100e3;                % tone burst frequency
number_cycles=5;                % number of cycles 

folder_results = 'C:\Users\Groth\Desktop\models_ml\Golden eggs chicken\plane_strip\results' ;  % result files
folder_files = 'C:\Users\Groth\Desktop\models_ml\Golden eggs chicken\plane_strip' ;            % scripts 
%%
operator 