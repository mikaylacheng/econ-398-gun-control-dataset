*Open Log
capture log 
log using Universal_Background_Checks_Data_Analysis, replace

**SUMMARY STATS**
ssc install estout

gen treat_year = has_universal_background_checks * year 
replace treat_year = . if has_universal_background_checks == 0
bys statecode: egen min_treat_year= min(treat_year)
bys statecode: egen ever_treated = max(has_universal_background_checks)
gen treat_date = min_treat_year
gen yearsafter = year-treat_date if ever_treated==1 


eststo summstats: estpost summarize  n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income education_attainment
eststo Treat: estpost summarize n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income education_attainment if ever_treated==1
eststo Control: estpost summarize  n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income education_attainment if ever_treated==0
esttab summstats Treat Control using summstats.rtf, replace main(mean %6.2f) aux(sd) mtitle("National" "Treatment Group" "Control Group")


**REGRESSIONS**

*Regress has_universal_background_checks on is_dem_majority
reg has_universal_background_checks is_dem_majority

*with controls
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income, r
eststo model1
*without controls
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year, r
eststo model2
*excluding democratic majority control
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment population unemployed p_nonwhite median_income, r
eststo model3
*weighted for population
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income [aweight=population], r
eststo model4
*lagged treatment year
reg n_pub_mass_shooting_victims treatyearnew education_attainment is_dem_majority population unemployed p_nonwhite median_income i.statecode i.year, r
eststo model5

*with time trend; lines 44-45 are evidence of the differing trends among states
graph twoway (lfit n_pub_mass_shooting_victims year) (scatter n_pub_mass_shooting_victims year) if statecode==5
graph twoway (qfit n_pub_mass_shooting_victims year) (scatter n_pub_mass_shooting_victims year) if statecode==35

sort statecode year
bys statecode: gen t = _n
gen trend = t * statecode
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income trend, r
eststo model6

*excluding year prior to treatment
gen yearprior = 0
replace yearprior = 1 in 159
replace yearprior = 1 in 219
replace yearprior = 1 in 237
replace yearprior = 1 in 298
replace yearprior = 1 in 1061
replace yearprior = 1 in 1175
replace yearprior = 1 in 1207
replace yearprior = 1 in 1399
replace yearprior = 1 in 1481
replace yearprior = 1 in 1706
replace yearprior = 1 in 1746
replace yearprior = 1 in 1778
preserve
drop if yearprior==1
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income, r
eststo model7
restore

esttab model1 model2 model3 model4 model5 model6 model7 using resultsfinal.rtf, replace

*stratified into democrat and republican legislative majorities
preserve
drop if is_dem_majority==1
reg n_pub_mass_shooting_victims has_universal_background_checks education_attainment  population unemployed p_nonwhite median_income i.statecode i.year,r
restore

preserve
drop if is_dem_majority==0
reg n_pub_mass_shooting_victims has_universal_background_checks education_attainment  population unemployed p_nonwhite median_income i.statecode i.year,r
restore
*# mass shootings as dependent variable
reg n_pub_mass_shootings has_universal_background_checks education_attainment is_dem_majority population unemployed p_nonwhite median_income i.statecode i.year,r

*clustered standard errors
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income, r
eststo model1
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income, cluster(statecode)
eststo model2
esttab model1 model2 using clusterresults.rtf, replace


*Close Log
log close
