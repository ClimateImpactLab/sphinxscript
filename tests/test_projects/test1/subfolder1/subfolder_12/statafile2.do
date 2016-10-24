/*

Do some things with stata

:author: My Name
:team: Test team
:project: Doing some coding

This script can have all kinds of features, like latex!

.. math::
  \alpha_j=\sum_{i=0}^{15}{\hat{\beta}_{i, j}^2} \forall j \in J

*/


clear all
set more off
set matsize 10000
set maxvar 12000


gen allage_country = 1
replace allage_country = 0
gen agegrp_country = 1
replace agegrp_country = 0

tempfile collapsed
save `collapsed', replace


