//ssc install ftools
//ssc install reghdfe
gen treat_year = is_after_brady_bill_fed_check_la * year 
replace treat_year = . if is_after_brady_bill_fed_check_la == 0
bys statecode: egen min_treat_year= min(treat_year)

bys statecode: egen ever_treated = max(is_after_brady_bill_fed_check_la)
gen treat_date = min_treat_year
gen yearsafter = year-treat_date if ever_treated==1 

//eric suggests changing these to every 3 years as well. ex: california is listed as 8 years away from treatment for years 6-8 away from treatment. this syncs these values to the fixed effects somehow to not make them collinear. 
forvalues i = 1/10{
	gen years_n`i' = 0
	replace years_n`i' = 1 if yearsafter == -`i'
}

forvalues i = 0/27{
	gen years_p`i'= 0
	replace years_p`i' = 1 if yearsafter == `i'
}

//eric told me to do this to solve the omitted variable collinearity problem with the fe (explained in line 40 below)
gen year3 = 2021 if year<=2021
replace year3=2019 if year<2020
replace year3=2016 if year<2017
replace year3=2013 if year<2014
replace year3=2010 if year<2011
replace year3=2007 if year<2008
replace year3=2004 if year<2005
replace year3=2001 if year<2002
replace year3=1998 if year<1999
replace year3=1995 if year<1996
replace year3=1992 if year<1993
replace year3=1989 if year<1990
replace year3=1986 if year<1987




//36 vars: Sara: when I ran this regression the variables were omitted due to perfect collinearity. That's why lines 23-35 code are added and the fe variable in the parantheses for year is now year3. Not sure if that's right though, may need to switch it back. 
reghdfe n_pub_mass_shooting_victims years_n10 years_n9 years_n8 years_n7 years_n6 years_n5 years_n4 years_n3 years_n2 years_p0 years_p1 years_p2 years_p3 years_p4 years_p5 years_p6 years_p7 years_p8 years_p9 years_p10 years_p11 years_p12 years_p13 years_p14 years_p15 years_p16 years_p17 years_p18 years_p19 years_p20 years_p21 years_p22 years_p23 years_p24 years_p25 years_p26 years_p27 education_attainment is_dem_majority population unemployed p_nonwhite median_income, a(year3 statecode)

//creating plot 

gen cf = 0 if yearsafter== -1
gen hi = .
gen lo = .
reghdfe n_pub_mass_shooting_victims years_n3 years_n2 years_p0 years_p1 years_p2 years_p3 education_attainment is_dem_majority population unemployed p_nonwhite median_income, a(year3 statecode)


//for negative 2/10
forvalues i = 1/10{
	replace cf = _b[years_n`i'] if yearsafter == -`i'
	replace hi = _b[years_n`i'] + 1.96*_se[years_n`i'if yearsafter == -`i'
	replace lo = _b[years_n`i'] - 1.96*_se[years_n`i'if yearsafter == -`i'
}


forvalues i = 0/27{
	replace cf = _b[years_p`i'] if yearsafter == `i'
	replace hi = _b[years_p`i'] + 1.96*_se[years_p`i'if yearsafter == `i'
	replace lo = _b[years_p`i'] - 1.96 * _se[years_p`i'] if yearsafter == `i'

}

collapse cf hi lo, by(yearsafter)
twoway(scatter cf yearsafter) (rcap hi lo yearsafter)
