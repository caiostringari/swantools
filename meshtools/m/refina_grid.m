% Refina grid pelo triangle
cd /home/pedrog/Documentos/Broou.cast/UN_SP/

%% primeiro critrio
!triangle -pqn45a0.010 SP_UN.poly

xyz=load('~/Documentos/dados/Batimetria_BROOUCAST/bat_broou_etopo.xyz');
f=find( (xyz(:,2)>-25) & (xyz(:,2)<-23) );
extract_bot('SP_UN.1',xyz(f,1),xyz(f,2),-xyz(f,3))

%% segundo crit�rio
[x,y,k]=read_ungrid('SP_UN.1');
z=load('SP_UN.1.bot');
figure; plotgrid('SP_UN.1'); title('SP_UN.1')
% area inicial sqrt(3)*((110000/4)^2)/4
L1=0.1;
%%%%
zT=[]; % � a profundidade media entre os elementos dos nos dos triangulos
for i=1:length(k)
    pM=mean([z(k(i,1)),z(k(i,2)),z(k(i,3))]);
    zT=[zT;pM];
end
   
AR=[];
%tes=[];
for i=1:length(zT)
    if zT(i)<-500
        L=L1; % 1/4 de grau em metros
    elseif zT(i)>-500 && zT(i)<-300
        L=L1/(1);%/(1.1); 
    elseif zT(i)>-300 && zT(i)<-200
        L=L1/(1); 
    elseif zT(i)>-200 && zT(i)<-100
        L=L1/(1);  
    elseif zT(i)>-100 && zT(i)<-75
        L=L1/(1.2);
    elseif zT(i)>-75 && zT(i)<-50
        L=L1/(2);        
    elseif zT(i)>-50 && zT(i)<-25
        L=L1/(4);
    elseif zT(i)>-25 && zT(i)<-15
        L=L1/(8);
    elseif zT(i)>-15 && zT(i)<-10
        L=L1/(16);
    elseif zT(i)>-10
        L=L1/(16);  
    else
    end
    AR=[AR;sqrt(3)*(L^2)/4]; % Area em funcao da profundidade media do triangulo
    %tes=[tes;t]
end
    
%escreve .area

% .area file
%First line: <# of triangles>
%Following lines: <triangle #> <maximum area>
fid=fopen('SP_UN.1.area','w');
fprintf(fid,[num2str(length(AR)),'\n']);
for i=1:length(AR);
    %fprintf(fid,[num2str(k(i,1)),'   ',num2str(k(i,2)),'   ',num2str(k(i,3)),'   ',num2str(AR(i)),'\n']);
    fprintf(fid,[num2str(i),'   ',num2str(AR(i)),'\n']);
end


% start triangle refinement
!triangle -rpq30a SP_UN.1
figure; plotgrid('SP_UN.2'); title('SP_UN.2')

clear all;
xyz=load('~/Documentos/dados/Batimetria_BROOUCAST/bat_broou_etopo.xyz');
f=find( (xyz(:,2)>-25) & (xyz(:,2)<-23) );
extract_bot('SP_UN.2',xyz(f,1),xyz(f,2),-xyz(f,3))
%% Aplicando mais 5 uma vez o primeiro cricerio
clear all; 
xyz=load('~/Documentos/dados/Batimetria_BROOUCAST/bat_broou_etopo.xyz');

for j=2:5;

[x,y,k]=read_ungrid(['SP_UN.',num2str(j)]);
z=load(['SP_UN.',num2str(j),'.bot']);

% area inicial sqrt(3)*((110000/4)^2)/4
L1=0.1;
%%%%
zT=[]; % � a profundidade media entre os elementos dos nos dos triangulos
for i=1:length(k)
    pM=mean([z(k(i,1)),z(k(i,2)),z(k(i,3))]);
    zT=[zT;pM];
end
   
AR=[];
%tes=[];
for i=1:length(zT)
    if zT(i)<-500
        L=L1; % 1/4 de grau em metros
    elseif zT(i)>-500 && zT(i)<-300
        L=L1/(1);%/(1.1); 
    elseif zT(i)>-300 && zT(i)<-200
        L=L1/(1); 
    elseif zT(i)>-200 && zT(i)<-100
        L=L1/(1);  
    elseif zT(i)>-100 && zT(i)<-75
        L=L1/(1.2);
    elseif zT(i)>-75 && zT(i)<-50
        L=L1/(2);        
    elseif zT(i)>-50 && zT(i)<-25
        L=L1/(4);
    elseif zT(i)>-25 && zT(i)<-15
        L=L1/(8);
    elseif zT(i)>-15 && zT(i)<-10
        L=L1/(16);
    elseif zT(i)>-10
        L=L1/(16);  
    else
    end
    AR=[AR;sqrt(3)*(L^2)/4]; % Area em funcao da profundidade media do triangulo
    %tes=[tes;t]
end
    
    
%escreve .area

% .area file
%First line: <# of triangles>
%Following lines: <triangle #> <maximum area>
fid=fopen(['SP_UN.',num2str(j),'.area'],'w');
fprintf(fid,[num2str(length(AR)),'\n']);
for i=1:length(AR);
    %fprintf(fid,[num2str(k(i,1)),'   ',num2str(k(i,2)),'   ',num2str(k(i,3)),'   ',num2str(AR(i)),'\n']);
    fprintf(fid,[num2str(i),'   ',num2str(AR(i)),'\n']);
end

% start triangle refinement
eval(['!triangle -rpq30aa SP_UN.',num2str(j)])
figure
plotgrid(['SP_UN.',num2str(j+1)]);  title(['SP_UN.',num2str(j+1)])

f=find( (xyz(:,2)>-25) & (xyz(:,2)<-23) );
extract_bot(['SP_UN.',num2str(j+1)],xyz(f,1),xyz(f,2),-xyz(f,3))
end

ocean_pts(['SP_UN.',num2str(j+1)])