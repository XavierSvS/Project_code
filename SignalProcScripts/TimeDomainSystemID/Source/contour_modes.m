function contour_modes(phi,x,y)
phi
[Xgrid Ygrid] = meshgrid(min(x):1:max(x),min(y):.5:max(y));

    [cfun_fdd,gof,output]  = fit([x, y], phi,'cubicinterp');
    set(gcf,'PaperOrientation','portrait','papertype','A4',...
    'paperunits','centimeters','paperPosition',[0.63, 7.75, 19.72, 14.17])
    surface_fdd = cfun_fdd(Xgrid,Ygrid);
    surface_fdd = surface_fdd/max(max(abs(surface_fdd)));
    mesh(Xgrid,Ygrid,surface_fdd)
    shading interp
    axis equal
    view([-220 35])
    box on
    grid on
    xlabel('x-axis (m)','Fontsize',10,'Fontname','TimesnewRoman')
    ylabel('y-axis (m)','Fontsize',10,'Fontname','TimesnewRoman')
    zlabel('Norm. displacement','Fontsize',10,'Fontname','TimesnewRoman')
    set(gca,'Fontsize',7,'Fontname','TimesnewRoman')
