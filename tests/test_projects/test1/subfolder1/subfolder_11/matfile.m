
%% Do some things with matlab
%% 
%% :author: My Name
%% :team: Test team
%% :project: Doing some coding
%% 
%% This script can have all kinds of features, like latex!
%% 
%% .. math::
%%   \alpha_j=\sum_{i=0}^{15}{\hat{\beta}_{i, j}^2} \forall j \in J
%% 
%% 

clear

val1 = 250;
val2 = 250;
val3 = 1000;
co = 0.9;

%define vcv matrix
cov31 = co*val1^2*ones(4590,4590)+(1-co)*val1^2*eye(4590);
cov32 = co*val2^2*ones(4590,4590)+(1-co)*val2^2*eye(4590);
cov33 = co*val3^2*ones(4590,4590)+(1-co)*val3^2*eye(4590);

vcv = blkdiag(cov31,cov32,cov33);

mu = zeros(1,13770);
draws = mvnrnd(mu,vcv,5000);
errors = transpose(draws);

corrcoef(draws(:,1:2))
corrcoef(draws(:,4590:4592))

