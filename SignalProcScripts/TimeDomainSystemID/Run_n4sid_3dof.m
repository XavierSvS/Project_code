%=============================================================================================
% This is the main file for calling the ERA function (ERA.m)

switch inptype
    case 'imp'
        
     YY=output;      %This is already impulse response
     z = iddata(YY,[],dt);

    case 'WN'
        
     YY=output;      %n4sid now works as stochastic
     z = iddata(YY,[],dt);
    
    otherwise
    YY=output;   
    input=f;
    z = iddata(YY,input,dt);

end

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
ndof=3;

sys = n4sid(z,2*ndof,'Ts',dt,'N4Weight','CVA');

ao=sys.A; bo=sys.B; co=sys.C;
 
[Vectors,Values]=eig(ao);
Lambda=diag(Values);           % roots in the Z-plane
s=log(Lambda).*fs; 
zeta=-real(s)./abs(s);        % damping factors: ksi
fd=abs(s); 

[freq_rel ind]=sort(fd);           %sort frequencies starting from lowest one
freq_rel/2/pi

modal_shapes=co*Vectors;
phi=real(modal_shapes(:,ind(1:2:end)));  %sort the eigenvectors correspondingly, and only keep them once

% Plot identified versus true (reference) modeshapes
close all
for i=1:3
subplot(1,3,i)
[mval, ind]=max(abs(phi(:,i)));
p1=plot([0 1 2 3],[0 phi(:,i)'*sign(phi(ind,i))/mval]);hold on
[mval, ind]=max(abs(V(:,i)));
p2=plot([0 1 2 3],[0 V(:,i)'*sign(V(ind,i))/mval],'r');
legend([p1 p2],'calculated','analytical')
end
