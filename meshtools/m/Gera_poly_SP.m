% gera Poly grid_SP

%limites do grid de SP
P1 = [-47.18,-24.48];
P2 = [-44.63,-24.48];
P3 = [-44.63,-23.31];
P4 = [-47.18,-23.31];

% carrega Linha de costa SMC
% load ~/Documentos/dados/batimetria_SMC_BR/sur.xy.mat
% f=find( (xy(:,2)<-23.31) & (xy(:,2)>-24.48) );
% SP_XY=xy(f,:);
% save('SP_XYi.txt','-ascii','SP_XY')
% SP_XY=xy(f,1:2);
% save('SP_XY.i2s','-ascii','SP_XY')

%carrega no goole_earth para gerar os poligono
%python open_bat_select2.py 'SP_XY.txt' 'SP' -48 -44 -25 -23

%% carrega e verifica arquivo de contornos
% Editar linhas no bluekenue.

% linha de costa = SP_coastline_c
% Ilhas fechadas = SP_ilhas_c

%% carrega linha de costa
Cline=load('SP_coastline_c20m_C2.txt');
%ilhas=load('SP_ilhas_c_IBela20m.txt');
ilhas_c=load('ilhas_corrigidas.txt');
%ilhas_c=load('ilhas_reduzidas.txt');
%ilhas_c=load('ilhabela20m.txt');
%figure; plot(Cline(:,1),Cline(:,2));
%hold on; plot(Cline(1,1),Cline(1,2),'ok');
%plot(Cline(end,1),Cline(end,2),'or');

%% verifica ilhas e corrige ilhas
% deleta pontos duplicado 
%[a,b,c]=unique(ilhas(f(i)+1:end,:),'rows');
%plot(a(:,1),a(:,2),'.'); hold on
f=find(ilhas(:,2)==0);

!rm ilhas_corrigidas.txt
fidc=fopen('ilhas_corrigidas2.txt','w');
%ilhas_c=[];
load('ilhas_c.m')
for i=209:length(f);
    d=0;d2=1;
    while ((d+d2)~=0) & ((d+d2)~=2) % enquanto nao for verificado 2 vezes
    if i==length(f)
       Ilha1=ilhas(f(i)+1:end,:);
    else
       Ilha1=ilhas(f(i)+1:f(i+1)-1,:);
    end
    figure(1)
    plot(Ilha1(:,1),Ilha1(:,2)); hold on
    scatter(Ilha1(:,1),Ilha1(:,2))
    plot(Cline(:,1),Cline(:,2));
    axmin=min(Ilha1(:,1))-0.025;
    axmax=max(Ilha1(:,1))+0.025;
    aymin=min(Ilha1(:,2))-0.025;
    aymax=max(Ilha1(:,2))+0.025;
    axis([axmin axmax aymin aymax])
    title(['F =  ',num2str(f(i)),', i = ',num2str(i),', npots = ',num2str(ilhas(f(i)))]);
    plot_google_map('maptype','satellite')
    % pergunta sobre manter ou nao a ilhas
    [d]=input('Deseja manter a ilha? [1=Yes/0=No] ');
    [d2]=input('Tem certesa? [1=Yes/0=No] ');
    if (d+d2)==2; % manter a ilha
        ilhas_c=[ilhas_c;length(Ilha1),0;Ilha1];
        fprintf(fidc,[num2str(length(Ilha1)),'   ',num2str(0),'\n']);
        for j=1:length(Ilha1)
           fprintf(fidc,[num2str(Ilha1(j,1),'%4.16f'),'   ',num2str(Ilha1(j,2),'%4.16f'),'\n']);
        end
    else        
    end
    close(figure(1))
    end
end

save('ilhas_c.m','ilhas_c')

fclose(fidc)
% figure(1)
% hold on
% plot(Cline(:,1),Cline(:,2));
% for i=1:length(f);
%     if i==length(f)
%        plot(ilhas(f(i)+1:f(end),1),ilhas(f(i)+1:f(end),2))
%     else
%        plot(ilhas(f(i)+1:f(i+1)-1,1),ilhas(f(i)+1:f(i+1)-1,2))
%     end
% end
% plot_google_map('maptype','satellite')
%problemas
%p=[14376,21363,18868,19307,21246,21836,22901,23009,23022]

%% cria oceano
%-----------------
% define limites
ymin=Cline(end,2);
ymax=Cline(1,2);
xmin1=Cline(end,1);
xmin2=Cline(1,1);
xmax=-44.00;

% cria borda oceanicas
dx=0.1; dy=0.1;

% borda SUL
xS=xmin1+dx:dx:xmax-dx;
yS=ymin*ones(1,length(xS));
BS=[xS',yS'];

% borda LESTE
yE=ymin:dy:ymax;
xE=xmax*ones(1,length(yE));
BE=[xE',yE'];

% borda NORTE
xN=xmax:-dx:xmin2+dx;
yN=ymax*ones(1,length(xN));
BN=[xN',yN'];
%BN=[BN;Cline(1,:)]; % para fechar o poligono quando juntar

% verifica
% figure; plot(Cline(:,1),Cline(:,2));
% hold on; plot(Cline(1,1),Cline(1,2),'ok');
% plot(Cline(end,1),Cline(end,2),'or');
% plot(BS(:,1),BS(:,2),'g');
% plot(BE(:,1),BE(:,2),'y');
% plot(BN(:,1),BN(:,2),'c');

% oceano
Cocean=[BS;BE;BN];

% verifica
% figure; plot(Cline(:,1),Cline(:,2));
% hold on; plot(Cline(1,1),Cline(1,2),'ok');
% plot(Cline(end,1),Cline(end,2),'or');
% plot(Cocean(:,1),Cocean(:,2),'g');


%% cria arquivo .poly com as ilhas
% descobre quantas ilhas tem 
f=find(ilhas_c(:,2)==0);

% cria contorno
xy=[Cline;Cocean];
c=ones(length(xy),1);
c(length(Cline)+1:end)=2; % controno oceanico
% verifica
figure; scatter(xy(:,1),xy(:,2),5,c); colormap(summer); caxis([1 2])

% cria contornos poly
!rm SP_UN.poly
fid=fopen('SP_UN.poly','w');
% -----------
% cabecalio
% -----
fprintf(fid,'#<n vertices> < 2 = n dimencion>  < 0 = n of atributs > < 0 = n of boundary marks > \n');
fprintf(fid,'#section of positions \n');
% -----------
% Pontos
% First line: <# of vertices> <dimension (must be 2)> <# of attributes> <# of boundary markers (0 or 1)>
% Following lines: <vertex #> <x> <y> [attributes] [boundary marker]
% -----
fprintf(fid,[num2str(length(xy)+(length(ilhas_c)-2*length(f))),'   ',num2str(2),'   ',num2str(0),'   ',num2str(0)','\n']);
for i=1:length(xy); 
    k=i;
    fprintf(fid,[num2str(k),'   ',num2str(xy(i,1),'%4.16f'),'   ',num2str(xy(i,2),'%4.16f'),'\n']);
end
% -----------
% insere as ilhas
% -----------
fprintf(fid,'#section of island positions \n');
for i=1:length(f);
   for j=1: (ilhas_c(f(i),1) -1) % -1 para ele nao fechar a ilha
       k=k+1;
       fprintf(fid,[num2str(k),'   ',num2str(ilhas_c(f(i)+j,1),'%4.16f'),'   ',num2str(ilhas_c(f(i)+j,2),'%4.16f'),'\n']);
   end
end
% -----------
% arquivo de ligacao
% One line: <# of segments> <# of boundary markers (0 or 1)>
% Following lines: <segment #> <endpoint> <endpoint> [boundary marker]
% -----
fprintf(fid,[num2str(length(xy)+(length(ilhas_c)-2*length(f))),'   ',num2str(1),'\n']);
for i=1:length(xy); % nao usar todo o comprimento para poder retirar a lagoa
    k=i;
    if i==length(xy); % liga fim no comeco
        fprintf(fid,[num2str(k),'   ',num2str(k),'   ',num2str(1),'   ',num2str(c(i)),'\n']);
    else
        fprintf(fid,[num2str(k),'   ',num2str(k),'   ',num2str(k+1),'   ',num2str(c(i)),'\n']);
    end
end
% -----------
% insere ligacao entreas ilhas
% -----------
fprintf(fid,'#section of island conection \n');
for i=1:length(f); % for nas ilhas
    fprintf(fid,['#section of island ',num2str(i),'\n']);
   for j=1: (ilhas_c(f(i),1) -1) % for nos potos das ilhas -1 para ele nao fechar a ilha
       k=k+1;
       if j==(ilhas_c(f(i),1) -1); % liga fim no comeco
            fprintf(fid,[num2str(k),'   ',num2str(k),'   ',num2str(k-(ilhas_c(f(i),1))+2),'   ',num2str(1),'\n']);
       else
            fprintf(fid,[num2str(k),'   ',num2str(k),'   ',num2str(k+1),'   ',num2str(1),'\n']);
       end
   end
end
% ----------
% secao de ilhas
%One line: <# of holes>
%Following lines: <hole #> <x> <y>
% -----
fprintf(fid,'#number of holes \n');
fprintf(fid,[num2str(length(f)),'\n']);
fprintf(fid,'#one point inside each the hole \n');
for i=1:length(f); % for nas ilhas
    if i==length(f)
        fprintf(fid,[num2str(i),'   ',num2str(mean(ilhas_c(f(i)+1:end,1))),'   ',num2str(mean(ilhas_c(f(i)+1:end,2))),'\n']);
    else
        fprintf(fid,[num2str(i),'   ',num2str(mean(ilhas_c(f(i)+1:f(i+1)-1,1))),'   ',num2str(mean(ilhas_c(f(i)+1:f(i+1)-1,2))),'\n']);
    end
end
% fim
fclose(fid);


%% cria grid com o trianlgle
%area1=(dx*dy)/2=0.0050
!triangle -pqn45a0.0050 SP_UN.poly
figure; plotgrid('SP_UN.1')

% remover na mao pontos duplicados se existir ! MUITO IMPORTANTE
% se deletar um ponto nao esquecer de mudar o numero no indicador
% abrir aquivos ilhas_corrigidas ou outros para procurar os pontos de
% conflito