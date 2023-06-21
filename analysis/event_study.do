*Open Log
capture log 
log using Universal_Background_Checks_Event_Study, replace

//EVENT STUDY
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


*Close Log
log close
