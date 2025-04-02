# -*- coding: utf-8 -*-

__author__ = "Konstantinos Vlachas"
__email__ = "vlachask@ibk.baug.ethz.ch"


import numpy as np
import time

def NewmarkTimeIntegration(Kstiff, MassM, DampingC, ExternalForce, dt, beta=1/4, gamma=1/2):
        """"
        This function implements the Newmark time integration scheme

        Arguments:
            dt (float): Time increment of the integration.
            beta,gamma (float): Newmark parameters.
            Kstiff (np.array): Stiffness matrix.
            MassM (np.array): Mass matrix.
            DampingC (np.array): Damping matrix.
            ExternalForce (np.array): External force time history matrix (as many rows as degrees of freedom, as many columns as time steps).
        """

        # Newmark parameters        
        a1 = 1 / (beta * (dt ** 2))
        a2 = 1 / (beta * dt)
        a3 = (1 - 2 * beta) / (2 * beta)
        a4 = gamma / (beta * dt)
        a5 = 1 - gamma / beta
        a6 = (1 - gamma / (2 * beta)) * dt

        number_of_dofs = np.shape(Kstiff)[0]
        number_of_time_steps = np.shape(ExternalForce)[1]


        # Initialize
        a1M, a4C = a1 * MassM, a4 * DampingC
        DisplacementsU = np.zeros((number_of_dofs, number_of_time_steps))
        VelocitiesV = np.zeros_like(DisplacementsU)
        AccelerationsA = np.zeros_like(DisplacementsU)
        fint = np.zeros((number_of_dofs, 1))

        # Assume zero initial conditions
        v0 = VelocitiesV[:, 0]
        u0 = DisplacementsU[:, 0]

        # Convergence norm
        col_index = np.argmax(np.max(abs(ExternalForce), axis=0))
        fnorm = np.linalg.norm(ExternalForce[:, col_index])

        # Evaluate initial acceleration
        f0 = ExternalForce[:, 0]
        a0 = np.linalg.inv(MassM).dot((f0 - Kstiff.dot(u0) - DampingC.dot(v0)))

        uk = u0
        uik = uk
        vk = v0
        ak = a0

        tol, maxit = 1e-03, 50
        # Start iterations
        converge=True
        for i in range(number_of_time_steps-1):
            fi = ExternalForce[:, i+1]

            va1 = a2 * vk + a3 * ak
            va2 = a5 * vk + a6 * ak

            # Compute residual
            R = MassM.dot(-va1) + DampingC.dot(va2) + fint[:, 0] - fi

            Rnorm = np.linalg.norm(R)
            nit = 0
            ui = uk
            uik = ui - uk

            while (Rnorm > tol * fnorm) and (nit <= maxit):
                Keff = a1M + a4C + Kstiff
                # Correct displacement based on residual
                du = np.linalg.inv(Keff).dot(-R)
                ui = ui + du
                uik = ui - uk

                fint = Kstiff.dot(ui)

                # Re-compute residual
                R = MassM.dot(a1 * uik - va1) + DampingC.dot(a4 * uik + va2) + fint[:, 0] - fi
                Rnorm = np.linalg.norm(R)

                nit = nit + 1

            if nit <= maxit:
                print(
                    "Step %i converged after %i iterations, residual %f \n"
                    % (i, nit, Rnorm / fnorm)
                )
            else:
                print(
                    "Step %i did not converge after %i iterations, residual %f \n"
                    % (i, nit, Rnorm / fnorm)
                )

            DisplacementsU[:, i + 1] = ui
            uk = ui
            ak = a1 * uik - va1
            vk = a4 * uik + va2
            VelocitiesV[:, i + 1] = vk
            AccelerationsA[:, i + 1] = ak

        return DisplacementsU, VelocitiesV, AccelerationsA

