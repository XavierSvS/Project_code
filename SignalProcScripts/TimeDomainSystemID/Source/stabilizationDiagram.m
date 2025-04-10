function data = stabilizationDiagram(modelSet,modelCov,threshold,damping,V,eig_c)

% 
% modelSet: a cell array of structural models in ss or tf format




%
% Reference page in Help browser:
% <a href="matlab: web([docroot '/toolbox/mdac/funref/stabilizationDiagram.html'],'-helpbrowser')">doc stabilizationDiagram</a>
%

%
% Author: V. Ntertimanis
% 1st Ed: 09-04-2014
% Last Update: 13-04-2014
% ETH Zurich
% Copyright 1995-2014 V.K. Ntertimanis
%


M = length(modelSet);
% define colormap
colorMap = colormap(jet(100));
hold on;
currentOrder = zeros(1,M);

for k = 1:M
    % get model
    currentStructure = modelSet{k};
    currentCovariance = modelCov{k};
    % get model order, frequencies and dispersions
    currentOrder(k) = length(currentStructure.a);    
    [currentDelta,currentWN] = dispersionAnalysis(currentStructure,currentCovariance);
    n = size(currentDelta,3);
    % calculate L2 dispersion norms and normalize
    currentDeltaN = zeros(1,n);
    for p = 1:n
        currentDeltaN(1,p) = norm(currentDelta(:,:,p),2);
    end
    
    currentDeltaN = currentDeltaN/max(currentDeltaN);
    currentDeltaNcMap = ceil(100*currentDeltaN);
    % plot current model's modal state
    for q = 1:n
        if currentDeltaNcMap(q) > threshold
            MC_c = 0;
            data(k,2)=currentOrder(k); data(k,1)=currentWN(q);
            if damping{k}(q)<.08
              if k<M
              [~, indm] = min(abs(abs(eig_c{k}(q))/2/pi-abs(eig_c{k+1})/2/pi));
              MC_c=MAC(V{1,k}(:,q),V{1,k+1}(:,indm));
              else
              MC_c=1;  
              end
              if MC_c>.85
              line([currentWN(q) currentWN(q)],[currentOrder(k) currentOrder(k)+1],'Color',colorMap(currentDeltaNcMap(q),:),'LineWidth',3);
              else
              line([currentWN(q) currentWN(q)],[currentOrder(k) currentOrder(k)+1],'Color',[0.4, 0.4,0.4],'LineWidth',1);
              end
            else
            line([currentWN(q) currentWN(q)],[currentOrder(k) currentOrder(k)+1],'Color',[0.4, 0.4,0.4],'LineWidth',1);
            end
        end
    end
    xlabel('frequency (Hz)','FontSize',12)
    ylabel('model order','FontSize',12)
    title('Frequency Stabilization Diagram','FontSize',12)
    axis([min(currentWN)-.5 max(currentWN)+.5 min(currentOrder)-1 max(currentOrder)+2])
        
end
colorbar
caxis([0 1])
hold off;