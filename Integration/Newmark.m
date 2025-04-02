function [dis, vel , acc] = Newmark(M, C, K, S, R, gamma, beta, dt)

    a1 = 1/(beta*dt^2)*M+gamma/(beta*dt)*C;
    a2 = 1/(beta*dt)*M+(gamma/beta-1)*C;
    a3 = (1/(2*beta)-1)*M+dt*(gamma/(2*beta)-1)*C;

    [L, U, P] = lu(K+a1);
    F = sparse(S*R);

    c1 = gamma/(beta*dt);
    c2 = 1-gamma/beta;
    c3 = dt*(1-gamma/(2*beta));
    c4 = 1/(beta*dt^2);
    c5 = -1/(beta*dt);
    c6 = -(1/(2*beta)-1);

    dis_k = zeros(size(K, 1), 1);
    vel_k = zeros(size(K, 1), 1);
    acc_k = M\F(:, 1);

    dis = zeros(size(K, 1), size(F, 2));
    vel = zeros(size(K, 1), size(F, 2));
    acc = zeros(size(K, 1), size(F, 2));

    acc(:, 1) = acc_k;

    for j = 1:size(F, 2)-1

        eForces = F(:, j+1)+a1*dis_k+a2*vel_k+a3*acc_k;

        dis(:, j+1) = U\(L\(P*eForces));
        vel(:, j+1) = c1*(dis(:, j+1)-dis_k)+c2*vel_k+c3*acc_k;
        acc(:, j+1) = c4*(dis(:, j+1)-dis_k)+c5*vel_k+c6*acc_k;

        dis_k = dis(:, j+1);
        vel_k = vel(:, j+1);
        acc_k = acc(:, j+1);

    end

end

