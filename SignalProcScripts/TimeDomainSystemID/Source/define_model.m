
%===============================================================================================
function model = init(init_args)
  global fs sys

  model.type = 'gssm';                       % object type = generalized state space model
  model.tag  = 'GSSM_LTI1';                  % ID tag

  model.ffun       = @ffun;                  % file handle to FFUN
  model.hfun       = @hfun;                  % file handle to HFUN
  model.prior      = @prior;                 % file handle to PRIOR
  model.likelihood = @likelihood;            % file handle to LIKELIHOOD
  model.linearize  = @linearize;             % file handle to LINEARIZE
  model.setparams  = @setparams;             % file handle to SETPARAMS

  model.statedim   = 6;                      %   state dimension
  model.obsdim     = 2;                      %   observation dimension
  model.U1dim      = 1;                      %   exogenous control input 1 dimension
  model.U2dim      = 0;                      %   exogenous control input 2 dimension
  model.Vdim       = model.statedim;                    %   process noise dimension
  model.Ndim       = model.obsdim;                      %   observation noise dimension
 

  Arg.type = 'gaussian';
  Arg.cov_type = 'full';
  Arg.dim = model.Vdim;
  Arg.mu = zeros( model.Vdim,1);
  Arg.cov  =1e-2*eye(model.Vdim);
  Arg.sample = @gsample;
  model.pNoise     = Arg;   % process noise : zero mean white Gaussian noise , cov=0.001

  Arg.type = 'gaussian';
  Arg.cov_type = 'full';
  Arg.dim = model.Ndim;
  Arg.mu = zeros( model.Ndim,1);
  Arg.sample = @gsample;
  Arg.cov  = 1e-4*eye(model.Ndim);
  model.oNoise     = Arg;     % observation noise : zero mean white Gaussian noise, cov=0.2


  modelDisc  = c2d(sys,1/fs);
  model.A=modelDisc.a;model.B=modelDisc.b;
  model.C=modelDisc.c;model.D=modelDisc.d;

  model.G  = [zeros(model.statedim/2,model.statedim);zeros(model.statedim/2) eye(model.statedim/2)];    %Adding Noise to the Measurement (only for velocity component affected by f1)
  model.H  = eye(model.Ndim);


%===============================================================================================
function new_state = ffun(model, state, V, U1)

  new_state  = model.A*state+ model.B*U1;    % Discrete Measurement

%===============================================================================================
function observ = hfun(model, state, N, U2)

    observ = model.C*state;                           

  

