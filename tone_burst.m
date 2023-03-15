%%%%%%% FUNÇÃO TONE BURST - Eduardo Becker Groth %%%%%%%%%%%%%%%%
w1=(frequency)*2*pi; %frequência de excitação (Hz) [rad/s]  
nc=number_cycles; %número de ciclos
f1=2e6;
passo=1/f1*1; %passo de tempo
t=0:passo:2*pi*(nc/w1);
w2=w1/nc;

%% tone_burst por seno e cosseno 
for i=1:size(t,2)
y=cos(w1*t).*(cos(w2*(t)+pi)+1)/2;
end

figure
plot(t,y);
axis([0 2*pi*(nc/w1) -1 1])

%% fft 
delta_x=size(t,2)*4; 
f=1/passo; %frequencia de aquisição
w = 0:f/delta_x:f-f/delta_x;
X=abs(fft(y,delta_x));

figure
plot(w*2*pi/2*pi,X/max(X))%,w*2*pi,X2/max(X2),'k',w*2*pi,X3/max(X3),'r'); % descomentar para todas as ffts
legend('cosseno')%,'gaussian','normal')
axis([0 w1*2 0 1.5]);

txt1=1;   % to abaqus python scripts 
if txt1 == 1;
A=[t;y];    
csvwrite('tb.csv',A)
end















