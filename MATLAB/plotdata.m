fig = figure;
% 3FF
y = [25.23,33.06,38.74,43.89, 48.81,52.71, 55.32, 56.98, 58.23, 58.6 ,58.74 58.69, 55.8];
x = 2.*[0.005,0.01,0.015,0.02,0.025,0.03, 0.04, 0.05, 0.06, 0.066,0.068, 0.07, 0.08];
p1 = plot(x,y,'-s');
hold on
% 1F
y = [25.03, 33.09, 38.80, 44.03, 48.67,51.6, 53.47, 56.28, 56.94, 58.43, 58.86, 59.37, 59.6,59.58, 58.22];
x = 2.*[0.005,0.01,0.015,0.02,0.025,0.03, 0.04, 0.05, 0.06, 0.07, 0.08,0.088, 0.09, 0.092, 0.1];
p2 =plot(x,y,'-*');
% F
y = [25.04, 32.94,38.16, 43.41,47.99, 52.04, 54.59, 56.54, 57.94, 58.71, 59.52, 60.13, 60.37,60.51,60.46 59.94];
x = 2.*[0.005,0.01,0.015,0.02,0.025,0.03, 0.04, 0.05, 0.06, 0.07, 0.08,0.09, 0.1,0.102, 0.104, 0.11];
p3 = plot(x,y,'-x');
% 7
y = [24.72,32.72,38.08,43.08,47.64, 51.75, 54.29, 56.05, 57.41, 58.23, 59.08, 59.84,60.19, 60.93, 61.15,61.34,61.38 61.28, 59.86];
x = 2.*[0.005,0.01,0.015,0.02,0.025,0.03, 0.04, 0.05, 0.06, 0.07, 0.08,0.09, 0.1, 0.11, 0.12,0.126, 0.128, 0.13,0.14];
p4 =plot(x,y,'-d');
% 3
y = [54.89, 56.36, 56.77, 58.23, 58.69, 59.64, 59.9, 60.69, 61.16, 61.54, 61.81, 62.24, 62.6];
x = 2.*[0.05, 0.06, 0.07, 0.08,0.09, 0.1, 0.11, 0.12,0.13,0.14,0.15,0.16,0.17];
p5 = plot(x,y,'-o');
title("SNDR vs Input Full Scale")
ylabel("SNDR (dB)")
xlabel("Input Full Scale")
lgd = legend([p1, p2, p3, p4, p5],["Gain = 10","Gain = 5","Gain = 4","Gain = 3","Gain = 2"],'AutoUpdate','off');
lgd.Location = 'southeast';
set(fig,'defaultLegendAutoUpdate','off')
xline(2*0.17, Label='CI-Bias Limit')