clear all 
set more off
set matsize 800
cd  "/Users/kdonova6/Desktop/Papers/Dandora Mentors/"

* This file creates all tables included in the online appendix.


use "datasets/BDJ_Dandora_Data.dta", clear
global controls "lage_b secondaryedu_b sec0_b sec1_b sec2_b sec3_b sec4_b I_emp_b"
xtset id wave


log using "logged_results/BDJ_Appendix", replace



* ------- APPENDIX A: FURTHER BALANCE TESTS


// Wave-by-wave balance tests (Tables 11 -- 17)
forvalues ii = 1/7 {

display("Balance Test: Wave = `ii'")

by treat, sort: sum profit_b businessage_b I_emp_b emp_b2 /*
*/ credit_b bankaccount_b loan_b formalaccount_b advert_b /*
*/ manu_b retail_b food_b serv_b /*
*/ age_b secondaryedu_b  if wave == `ii'

}


// Correlates with number of surveys taken (Table 18)

pwcorr count profit_b businessage_b I_emp_b emp_b2 /*
*/ credit_b bankaccount_b loan_b formalaccount_b advert_b /*
*/ manu_b retail_b food_b serv_b /*
*/ age_b secondaryedu_b  if wave == 0, star(0.01)

pwcorr count profit_b businessage_b I_emp_b emp_b2 /*
*/ credit_b bankaccount_b loan_b formalaccount_b advert_b /*
*/ manu_b retail_b food_b serv_b /*
*/ age_b secondaryedu_b  if wave == 0, star(0.05)

pwcorr count profit_b businessage_b I_emp_b emp_b2 /*
*/ credit_b bankaccount_b loan_b formalaccount_b advert_b /*
*/ manu_b retail_b food_b serv_b /*
*/ age_b secondaryedu_b  if wave == 0, star(0.1)






* ------- APPENDIX B: Baseline Learning Methods

use "datasets/BDJ_Baseline_Data.dta", clear

sort bl
drop if bl[_n] == bl[_n-1]
destring(binl), replace
drop if bl ==".-0"

#delimit ;
 label define ages 
            1 "< 1"
            2 "1-5"
            3 "5-10"
            4 "10-15"
            5 "> 15";	
#delimit cr			
			
label values binl ages			

* Figure 8a-c
twoway(connected lavg_profit_learn binl if self_taught == 0) /*
*/ (connected lavg_profit_learn binl if self_taught == 1,lpattern(--)), /*
*/ ytitle("Log average profit (Ksh)") xtitle("Business Age (years)") graphregion(color(white) ilwidth(none)) name(Figure8a) /*
*/ legend(label(1 "Learned") label(2 "Self-Taught")) xlabel(1/5,valuelabel) ylabel(9(0.5)10.5)
graph export "plots/Figure8a_appendix.eps", as(eps) preview(off) replace

twoway(connected avg_I_emp_learn binl if self_taught == 0) /*
*/ (connected avg_I_emp_learn binl if self_taught == 1,lpattern(--)), /*
*/ ytitle("Share with hired workers") xtitle("Business Age (years)") graphregion(color(white) ilwidth(none)) name(Figure8b) /*
*/ legend(label(1 "Learned") label(2 "Self-Taught")) xlabel(1/5,valuelabel)
graph export "plots/Figure8b_appendix.eps", as(eps) preview(off) replace

twoway(connected lavg_wagebill_learn binl if self_taught == 0) /*
*/ (connected lavg_wagebill_learn binl if self_taught == 1,lpattern(--)), /*
*/ ytitle("Log total monthly wage bill (Ksh)") xtitle("Business Age (years)") graphregion(color(white) ilwidth(none)) name(Figure8c) /*
*/ legend(label(1 "Learned") label(2 "Self-Taught")) xlabel(1/5,valuelabel)
graph export "plots/Figure8c_appendix.eps", as(eps) preview(off) replace








* ------- APPENDIX C: Details of Mentor Selection
use "datasets/RD_Dataset.dta", clear


// Differences between mentees and non-mentees (Table 19)

replace employeesnumber = . if employees == 0

#delimit ; 

sum profit businessage employees employeesnumber 
credit bankaccount loan account marketing 
age secondaryedu if treat == 1;


sum profit businessage employees employeesnumber 
credit bankaccount loan account marketing 
age secondaryedu if treat == 0;

# delimit cr



// Cut-off density (Figure 9)
twoway(kdensity err_log), xline(.0168324) xtitle("Residual") ytitle("Density") graphregion(color(white) ilwidth(none)) name(Figure9)
graph export "plots/Figure9_appendix.eps", as(eps) preview(off) replace



// Using MSE-Optimal Bandwidth (Table 20)
foreach x in tprofit tinventory marketing keeps_some_records {

	display in red "MSE-Optimal Bandwidth. VAR = `x' ... Poly = 0"
	rdrobust `x'_endline ce_std, p(0)
	
	display in red "MSE-Optimal Bandwidth. VAR = `x' ... Poly = 1"
	rdrobust `x'_endline ce_std, p(1)
	
	display in red "MSE-Optimal Bandwidth. VAR = `x' ... Poly = 2"	
	rdrobust `x'_endline ce_std, p(2)
	
	qui sum `x'_endline if treat == 1
	display in red "Treatment Avg = `r(mean)'"
	qui sum `x'_endline if treat == 0
	display in red "Control Avg = `r(mean)'"

}





* ------- APPENDIX D: More results 

* ------- D1. Table 21, column 3
use "datasets/BDJ_Dandora_Data.dta", clear
xtset id wave

sum sec0_b sec1_b sec2_b sec3_b sec4_b if wave == 0 
sum sec0_* if wave == 0
sum sec1_* if wave == 0
sum sec2_* if wave == 0
sum sec3_* if wave == 0


* ------- D1. Table 21, column 2
use "datasets/BDJ_Baseline_Data.dta", clear

sum sec0 sec1 sec2 sec3
sum sec0_* 
sum sec1_* 
sum sec2_* 
sum sec3_* 


* -------- D1. Table 21, column 3
sum gender if sec0 == 1
sum gender if sec1 == 1
sum gender if sec2 == 1
sum gender if sec3 == 1


forvalues ii = 0/10 {
	sum gender if sec0_`ii' == 1

}

// within each sector -- production.
forvalues ii = 1/6 {
	sum gender if sec1_`ii' == 1

}


// within each sector -- services. 
forvalues ii = 0/7 {
	sum gender if sec2_`ii' == 1

}

// within each sector -- food. 
forvalues ii = 0/7 {
	sum gender if sec3_`ii' == 1

}







* ------- D2. Fixed Effects for Pooled Profit Regression (Table 22)
use "datasets/BDJ_Dandora_Data.dta", clear
xtset id wave


* Panel A, Table 22: Fixed effects
xtreg tprofits i.treat i.wave if wave>=0 & wave<=7, fe cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum tprofits if wave >= 0 & wave <= 7 & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
	* Note: no per-period results, because can't use FE in the 1-period model.

	
	
	
* Panel B, Table 22: no controls

display in red "----- VARIABLE: PROFIT ... WAVE = POOLED ... CONTROLS = NO -----"

reg tprofits i.treat i.wave if wave>=0 & wave<=7
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	
forvalues ii = 1/7 {

	display in red "----- VARIABLE: PROFIT ... WAVE = `ii' ... CONTROLS = NO -----"
	reg tprofits i.treat if wave == `ii'
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
}
	
	
	
* ------- D3. Other Dimensions of Mentor Heterogeneity (Table 23)


reg tprofits class mentorL_ba mentorM_ba mentorH_ba i.wave tprofits_b $controls, cluster(id)
	qui test _b[mentorH_ba] = _b[mentorL_ba] 
	display in red "Ho: mentor_H = mentor_L  p-value = `r(p)'"
	display " "
	qui test _b[mentorL_ba] = _b[class] 
	display in red "Ho: mentor_L = class  p-value = `r(p)'"
	display " "	
	


reg tprofits class mentor_ps mentor_hs i.wave tprofits_b $controls, cluster(id)
	qui test _b[mentor_hs] = _b[mentor_ps] 
	display in red "Ho: mentor_hs = mentor_ps  p-value = `r(p)'"
	display " "
	qui test _b[mentor_ps] = _b[class] 
	display in red "Ho: mentor_ps = class  p-value = `r(p)'"
	display " "	

	
	
	
	
* --------- D4: Supplier Switching by business age and sector (Table 24)

display in red "---------- Switching, no controls ---------------- "

reg supplierswitch i.treat if wave == 5, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	

display in red "---------- Switching, controls ---------------- "

reg supplierswitch i.treat $controls if wave == 5, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	

	


* ------- D5. Business Exit (Table 25)	
	
	
	
display in red "---------- EXIT, no controls ---------------- "

reg exit i.treat if wave == 7, robust
	qui test _b[4.treat] = _b[3.treat] 
	qui local sign_wgt = sign(_b[4.treat]-_b[3.treat])
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	
display in red "---------- EXIT, no controls ---------------- "

reg exit i.treat $controls if wave == 7, robust
	qui test _b[4.treat] = _b[3.treat] 
	qui local sign_wgt = sign(_b[4.treat]-_b[3.treat])
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
		
	
	
* ------- D6. Product Switching (Table 26)

display in red "Product Switching (t=1-12) ... Controls = NO"

reg new_product i.treat i.wave if wave>=1 & wave<=6, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "		
	qui sum new_product if wave >= 1 & wave <=6 & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
	

display in red "Product Switching (t=1-12) ... Controls = YES"

reg new_product i.treat i.wave $controls if wave>=1 & wave<=6, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "		
	qui sum new_product if wave >= 1 & wave <=6 & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
	

	
* ------- D7. Measures of Business Scale (Table 27)

* Table 27, Panel A
foreach y in tinventorystock I_emp temployeesnumber twagebill tweekopen {
	display in red  "--------- Appendix D5 (Scale): VARIABLE = `y' ... WAVE = 5+6 ... CONTROLS = NO"
	reg `y' i.treat i.wave if wave == 5 | wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if (wave == 5 | wave == 6) & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
}


display in red  "--------- Appendix D5 (Scale): VARIABLE = BigInvestment? ... WAVE = POOLED ... CONTROLS = NO"

reg otherinvest i.treat i.wave if wave>=1 & wave<=6, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	qui local sign_wgt = sign(_b[4.treat]-_b[3.treat])
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum otherinvest if wave>=1 & wave<=6 & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
	
	
* Table 27, Panel B
foreach y in tinventorystock I_emp temployeesnumber twagebill tweekopen {
	display in red  "--------- Appendix D5 (Scale): VARIABLE = `y' ... WAVE = 5+6 ... CONTROLS = YES"
	reg `y' i.treat $controls i.wave if wave == 5 | wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if (wave == 5 | wave == 6) & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	
}


display in red  "--------- Appendix D5 (Scale): VARIABLE = BigInvestment? ... WAVE = POOLED ... CONTROLS = YES"

reg otherinvest i.treat i.wave $controls if wave>=1 & wave<=6, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	qui local sign_wgt = sign(_b[4.treat]-_b[3.treat])
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum otherinvest if wave >= 1 & wave <= 6 & treat2 == 2
	display in red "Control Mean = `r(mean)'"
	display " "	





* ------- D8. Formal and Informal Borrowing (Table 28)



* Table 28, Column (1)
display in red "---------- LOAN LAST LAST YEAR (no controls) ---------------- "
	
reg loanlastyear i.treat if wave == 6
	qui sum loanlastyear if treat == 2 & wave == 6
	display in red "Control mean = `r(mean)'"
	display " "
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	

* Table 28, Column (2)
display in red "---------- LOAN LAST LAST YEAR (controls) ---------------- "
	
reg loanlastyear i.treat $controls if wave == 6
	qui sum loanlastyear if treat == 2 & wave == 6
	display in red "Control mean = `r(mean)'"
	display " "
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	
	

	
	
* ------- D9. Decomposition of Business Scores (Tables 29-31)




// Marketing (Table 29)
foreach y in marketing_score competitorprice competitorproduct sales upsell do_advert {

	replace `y' = 0 if missing(`y')

	display " --------------------- t=7: `y'  ------------------------------ "
	reg `y' i.treat $controls if wave == 5, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 5 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "			
}

foreach y in marketing_score competitorprice competitorproduct sales upsell do_advert {
	display " --------------------- t = 12: `y'  ------------------------------ "
	replace `y' = 0 if missing(`y')

	reg `y' i.treat $controls if wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 6 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "		
}



// Stock (Table 30)
foreach y in stock_score supplierhaggle suppliercompare stockout {
	display " --------------------- `y'  ------------------------------ "
	reg `y' i.treat $controls if wave == 5, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 5 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "			
}

foreach y in stock_score supplierhaggle suppliercompare stockout {
	display " --------------------- `y'  ------------------------------ "
	reg `y' i.treat $controls if wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 6 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "			
}



// Record (Table 31)
foreach y in record_score everysale consultrecords budget {
	display " --------------------- t=7: `y'  ------------------------------ "
	reg `y' i.treat $controls if wave == 5, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 5 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "		
	
}


foreach y in record_score everysale consultrecords budget {
	display " --------------------- t=12: `y'  ------------------------------ "
	reg `y' i.treat $controls if wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if wave == 6 & treat == 2
	display in red "Control Mean = `r(mean)'"
	display " "		
			
}



* -------- D10: Relationship between meeting and previous profit realizations
	

local plist "delta_profits delta_profits_b delta_profits_c"

foreach x of local plist {

	display in red "----- TABLE 10B. INDEP VARIABLE: `x' ... WAVE = POOLED ... WAVE FE: NO -----"
	reg delta_meet L1.`x' $controls if wave>=1 & treat == 4, cluster(id)

	display in red "----- TABLE 10B. INDEP VARIABLE: `x' ... WAVE = POOLED ... WAVE FE: YES -----"
	reg delta_meet L1.`x' i.wave $controls if wave>=1 & treat == 4, cluster(id)

}
	
	

	


* ------------- D11: Self-reported usefulness (Table 32)

tab mentorbenefit if wave == 6









* ------------------ end. close log.

log close
translate "logged_results/BDJ_Appendix.smcl" "logged_results/BDJ_Appendix.pdf", replace
erase "logged_results/BDJ_Appendix.smcl"
