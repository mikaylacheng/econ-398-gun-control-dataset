//REGRESSION AND TABLES

//summary stats
ssc install estout
eststo summstats: estpost summarize  n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income 
eststo Treat: estpost summarize n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income if ever_treated==1
eststo Control: estpost summarize  n_pub_mass_shooting_victims n_pub_mass_shootings is_dem population unemployed p_white p_nonwhite median_income if ever_treated==0
esttab summstats Treat Control using summstats.rtf, replace main(mean %6.2f) aux(sd) mtitle("National" "Treatment Group" "Control Group")

//regression
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





//EVENT STUDY
//ssc install ftools
//ssc install reghdfe
gen treat_year = has_universal_background_checks * year 
replace treat_year = . if has_universal_background_checks == 0
bys statecode: egen min_treat_year= min(treat_year)

bys statecode: egen ever_treated = max(has_universal_background_checks)
gen treat_date = min_treat_year
gen yearsafter = year-treat_date if ever_treated==1 




forvalues i = 1/10{
	gen years_n`i' = 0
	replace years_n`i' = 1 if yearsafter == -`i'
}

forvalues i = 0/27{
	gen years_p`i'= 0
	replace years_p`i' = 1 if yearsafter == `i'
}


//36 vars:
reghdfe n_pub_mass_shooting_victims years_n10 years_n9 years_n8 years_n7 years_n6 years_n5 years_n4 years_n3 years_n2 years_p0 years_p1 years_p2 years_p3 years_p4 years_p5 years_p6 years_p7 years_p8 years_p9 years_p10 years_p11 years_p12 years_p13 years_p14 years_p15 years_p16 years_p17 years_p18 years_p19 years_p20 years_p21 years_p22 years_p23 years_p24 years_p25 years_p26 years_p27 education_attainment is_dem_majority population unemployed p_nonwhite median_income, a(year statecode)

//creating plot 

gen cf = 0 if yearsafter== -1
gen hi = .
gen lo = .
reghdfe n_pub_mass_shooting_victims years_n10 years_n9 years_n8 years_n7 years_n6 years_n5 years_n4 years_n3 years_n2 years_p0 years_p1 years_p2 years_p3 years_p4 years_p5 years_p6 years_p7 years_p8 years_p9 years_p10 years_p11 years_p12 years_p13 years_p14 years_p15 years_p16 years_p17 years_p18 years_p19 years_p20 years_p21 years_p22 years_p23 years_p24 years_p25 years_p26 years_p27 education_attainment is_dem_majority population unemployed p_nonwhite median_income, a(year statecode)


//for negative 2/10
forvalues i = 2/10{
	replace cf = _b[years_n`i'] if yearsafter == -`i'
	replace hi = _b[years_n`i'] + 1.96*_se[years_n`i'] if yearsafter == -`i'
	replace lo = _b[years_n`i'] - 1.96*_se[years_n`i'] if yearsafter == -`i'
}


forvalues i = 0/27{
	replace cf = _b[years_p`i'] if yearsafter == `i'
	replace hi = _b[years_p`i'] + 1.96*_se[years_p`i'] if yearsafter == `i'
	replace lo = _b[years_p`i'] - 1.96 * _se[years_p`i'] if yearsafter == `i'

}

collapse cf hi lo, by(yearsafter)
twoway(scatter cf yearsafter) (rcap hi lo yearsafter), scale (.5)
