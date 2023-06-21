//regression
// Nonwhite + single races
*nonwhite
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nonwhite median_income, r
eststo model1
*asian
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_asian median_income, r
eststo model2
*black
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_black median_income, r
eststo model3
*native american
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nativeamerican median_income, r
eststo model4
*white
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_white median_income, r
eststo model5

esttab model1 model2 model3 model4 model5 using resultsfinal.rtf, replace

// Asian
*with controls
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_asian median_income, r
eststo model11
*excluding democratic majority control
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment population unemployed p_asian median_income, r
eststo model12
*weighted for population
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_asian median_income [aweight=population], r
eststo model13

esttab model11 model12 model13 using asian.rtf, replace

// Black
*with controls
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_black median_income, r
eststo model14
*excluding democratic majority control
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment population unemployed p_black median_income, r
eststo model15
*weighted for population
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_black median_income [aweight=population], r
eststo model16

esttab model14 model15 model16 using black.rtf, replace

// Native American
*with controls
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nativeamerican median_income, r
eststo model17
*excluding democratic majority control
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment population unemployed p_nativeamerican median_income, r
eststo model18
*weighted for population
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_nativeamerican median_income [aweight=population], r
eststo model19

esttab model17 model18 model19 using native_american.rtf, replace

// Mixed 
*white + black + asian + native american
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_white p_black p_asian p_nativeamerican median_income, r
eststo model6
*white + asian + black
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_white p_asian p_black median_income, r
eststo model7
*white + black + native american
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_white p_black p_nativeamerican median_income, r
eststo model8
*white + asian + native american
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_white p_asian p_nativeamerican median_income, r
eststo model9
*asian + black + native american
reg n_pub_mass_shooting_victims has_universal_background_checks i.statecode i.year education_attainment is_dem_majority population unemployed p_black p_asian p_nativeamerican median_income, r
eststo model10

esttab model6 model7 model8 model9 model10 using results2.rtf, replace

