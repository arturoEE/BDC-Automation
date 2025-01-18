% clear all;
% clc;
close all;
%% Plot Settings
plotWidth = 15.5; % multipath
plotHeight = 11.25;
plotWidth2 = 10; % geometries
plotHeight2 = 6;
plotWidth3 = 8; % Lfly tapeout
plotHeight3 = 7;
plotWidth1 = 8; % coupling
plotHeight1 = 7;
plotWidth4 = 7; % Spiral Q
plotHeight4 = 5;
posx = 0;
posy = 0;
fontsize = 14; 
fontsize_title = 14; 
diamondsize = 40;
markersize1 = 20;
markersize2 = 25;

gridwidth = 1;
gridalpha = 0.4;
resolution = 2500;
%%
nBit = 10;
vmax = 60e-3;
vmin = 0;
range = [vmin vmax];
offset = mean(range);
offset = 1;
amp = (vmax - vmin)/2 * 1;
nSample = 2^16;
fs = round(1/(sine(2,1)-sine(1,1)));
fs = 1000;
fin = 101;
fin = chooseFin(fin, fs, nSample);
t = 0:1/fs:(nSample-1)/fs;
ain = amp * sin(2*pi*fin*t) + offset;
% dout = adc(ain, nBit, range);
offset = 1;
dout = sine(offset:nSample+offset,2);

% %% fix MSB
% l = length(dout);
% s = 1:1:l;
% t = 0;
% for x = 1:1:l-1
%     if dout(x+1) - dout(x) > 300
%         t = 0;
%     end
%     if dout(x+1) - dout(x) < -300
%         t = 512;
%     end
%     add(x+1) = t;
% end
% add(1) = 0;
% dout_fixed = dout + add.';

%%
[Enob, Ydb, Ydbn, SNDR] = calcENOB(dout, fin, fs);
Ydb = Ydb - max(Ydb);
Ydbn = Ydbn - max(Ydb);
figure(4)
hold on
box on
plot(linspace(0,fs/2,nSample/2), Ydb(1:nSample/2),'LineWidth',3,'Color','black');
% plot(linspace(0,fs/2,nSample/2), Ydbn(1:nSample/2),'LineWidth',3,'Color','red');
grid on;
xlabel("Frequency [Hz]",'FontName','Verdana','FontSize',fontsize)
ylabel("PSD [dB]",'FontName','Verdana','FontSize',fontsize)
% ylim([0.09 0.14])
% % grid(gca,'minor')
% xlim([0 0.1*xscale])
% xticks([0 0.05 0.1])
ax=gca; 
ax.XAxis.Exponent = 3;
grid on
set(gca,'FontName','Verdana','FontSize',fontsize,'LineWidth',gridwidth,'GridAlpha',gridalpha,'GridColor','k','MinorGridLineStyle','-')
set(gcf,'PaperUnits','centimeters')
set(gcf,'PaperSize',[plotWidth2,plotHeight2],'PaperPosition',[0,0,plotWidth2,plotHeight2],'Position',[posx,posy,plotWidth2*37.7953,plotHeight2*37.7953])
set(gcf,'Color','w')
% export_fig([targetFolder,'240126_Energy_Schemes.png'],"-r"+resolution)
% export_fig([targetFolder,'230131_VLSI_LflyRComp.pdf'])
% export_fig([targetFolder,'230131_VLSI_LflyRComp.emf'])



% quant = ain*(2^nBit-1) - dout;
% figure(1)
% hist(quant);
% grid on;
% xlabel('Quantization noise [LSB]'); ylabel('# of hits');
% title('Histogram of quantization noise');
