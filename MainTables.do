clear all 
set more off
set matsize 800
cd  "/Users/kdonova6/Desktop/Papers/Dandora Mentors/"

* This file creates the main tables for the paper.
* Change current directory as needed.

global controls "lage_b secondaryedu_b sec0_b sec1_b sec2_b sec3_b sec4_b I_emp_b"
log using "logged_results/BDJ_MainTables", replace










* ------------------ Table 1: baseline characteristics ----------------------- *

use "datasets/BDJ_Baseline_Data.dta", clear

replace employeesnumber = . if employees == 0

#delimit ; 

sum tprofit businessage employees employeesnumber 
credit bankaccount loan account marketing 
age gender secondaryedu;


sum tprofit businessage employees employeesnumber 
credit bankaccount loan account marketing 
age gender secondaryedu if youngfirm == 1;

# delimit cr

replace employeesnumber = 0 if employees == 0




* ------------------ Table 2: baseline balance tests ------------------------------ *
use "datasets/BDJ_Dandora_Data.dta", clear

xtset id wave

local balancelist "profit_b businessage_b I_emp_b emp_b credit_b bankaccount_b loan_b formalaccount_b advert_b manu_b retail_b food_b serv_b age_b secondaryedu_b"


foreach x of local balancelist {
	display in red "Baseline balance: `x'"
	reg `x' i.treat2 if wave == 0
}






* --------- Table 3: baseline profit regressions ------------------------ *


// Controls

display in red "----- VARIABLE: PROFIT ... WAVE = POOLED ... CONTROLS = YES -----"

reg tprofits i.treat i.wave $controls tprofits_b if wave>=0 & wave<=7
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	
forvalues ii = 1/7 {

	display in red "----- VARIABLE: PROFIT ... WAVE = `ii' ... CONTROLS = YES -----"
	reg tprofits i.treat $controls tprofits_b if wave == `ii'
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
}
	
	



	
	
	
* --------------------- Table 4: hetereogenous effects ------------------- *


reg tprofits class mentorL mentorM mentorH i.wave tprofits_b $controls, cluster(id)
	qui test _b[mentorH] = _b[mentorL] 
	display in red "Ho: mentor_H = mentor_L  p-value = `r(p)'"
	display " "
	qui test _b[mentorL] = _b[class] 
	display in red "Ho: mentor_L = class  p-value = `r(p)'"
	display " "	

forvalues ii = 1/6 {
	reg tprofits class mentorL mentorM mentorH tprofits_b $controls if wave == `ii'
	qui test _b[mentorH] = _b[mentorL] 
	display in red "Ho: mentor_H = mentor_L  p-value = `r(p)'"
	display " "
	qui test _b[mentorL] = _b[class] 
	display in red "Ho: mentor_L = class  p-value = `r(p)'"
	display " "	
}







* ------ Table 5: RD on mentors

use "datasets/RD_Dataset.dta", clear

foreach x in tprofit tinventory marketing keeps_some_records {

	qui rd `x'_endline ce_std, mbw(100 150 200)
	qui gen band100 = 1 if ce_std <= e(w) & ce_std >= -1*e(w) 
	qui gen band150 = 1 if ce_std <= e(w150) & ce_std >= -1*e(w150)
	qui gen band200 = 1 if ce_std <= e(w200) & ce_std >= -1*e(w200) 
	
	qui replace band100 = 0 if missing(band100)
	qui replace band150 = 0 if missing(band150)
	qui replace band200 = 0 if missing(band200)

	*** LOCAL LINEAR REGRESSIONS
	rd `x'_endline ce_std, mbw(100 150 200) 
	qui sum `x'_endline if treat == 1
	display in red "Treatment Avg = `r(mean)'"
	qui sum `x'_endline if treat == 0
	display in red "Control Avg = `r(mean)'"
	
	drop band*
}




* ------- FIG 4: Regression discontinuity

qui rd tprofit_endline ce_std, mbw(100 150 200)
qui gen band100 = 1 if ce_std <= e(w) & ce_std >= -1*e(w) 
qui gen band150 = 1 if ce_std <= e(w150) & ce_std >= -1*e(w150)
qui gen band200 = 1 if ce_std <= e(w200) & ce_std >= -1*e(w200) 
	
qui replace band100 = 0 if missing(band100)
qui replace band150 = 0 if missing(band150)
qui replace band200 = 0 if missing(band200)



* Note: the labels for the graphs in the paper are updated by hand.
cmogram tprofit_endline ce_std, cut(0) scatter line(0) qfitci note histopts(bin(15)) ciopts(level(95)) 
graph export "plots/Figure4a.eps", as(eps) preview(off) replace

cmogram tprofit_endline ce_std if band100 == 1, cut(0) scatter line(0) qfitci note histopts(bin(15)) ciopts(level(95))
graph export "plots/Figure4b.eps", as(eps) preview(off) replace




* ------- Table 6: effect on revenue, output prices, and supply cost


use "datasets/BDJ_Dandora_Data.dta", clear
xtset id wave


display in red "----- TABLE 6. VARIABLE: REVENUE ... CONTROLS = NO -----"

reg trevenue i.treat i.wave, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	
display in red "----- TABLE 6. VARIABLE: REVENUE ... CONTROLS = YES -----"

reg trevenue i.treat i.wave $controls, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	

display in red "----- TABLE 6. VARIABLE: OUTPUT PRICE ... CONTROLS = NO -----"
reg price i.treat i.wave, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "		
	
display in red "----- TABLE 6. VARIABLE: OUTPUT PRICE ... CONTROLS = YES -----"
reg price i.treat i.wave $controls, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	

display in red "----- TABLE 6. VARIABLE: SUPPLIER PRICE ... CONTROLS = NO -----"
reg cprice i.treat i.wave, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "		
	
display in red "----- TABLE 6. VARIABLE: SUPPLIER PRICE ... CONTROLS = YES -----"
reg cprice i.treat i.wave $controls, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	


	

* ------ Table 7: supplier switches 

display in red "----- TABLE 7. VARIABLE: SWITCH SUPPLIER ... WAVE = 5 ... CONTROLS = YES -----"

reg supplierswitch i.treat $controls if wave == 5, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	




	
* --------- Table 8: accounting and market time series ------------------ *



foreach y in keeps_some_records marketing {

	display in red "----- TABLE 11. VARIABLE: `y' ... WAVE = POOLED ... CONTROLS = YES -----"

	reg `y' i.treat i.wave $controls `y'_b if wave>=1 & wave<=6, cluster(id)
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "		

	forvalues ii = 1/6 {
	
		display in red "----- TABLE 11. VARIABLE: `y' ... WAVE = `ii' ... CONTROLS = YES -----"
		reg `y' i.treat $controls `y'_b if wave == `ii'
		qui test _b[4.treat] = _b[3.treat] 
		display in red "Ho: mentor = class  p-value = `r(p)'"
		display " "	

	}
}	
	


	
	


* ------- Table 9: OLS effects on aggregated business practices from McKenzie and Woodruff (2016)
	
	
local practicevec2 "z_business_score z_marketing_score z_stock_score z_record_score"


foreach y of local practicevec2 {

	display in red "----- TABLE 12. VARIABLE: `y' ... WAVE = 5+6 ... CONTROLS = YES -----"
	reg `y' i.treat $controls i.wave if wave == 5 | wave == 6, robust
	qui test _b[4.treat] = _b[3.treat] 
	display in red "Ho: mentor = class  p-value = `r(p)'"
	display " "	
	qui sum `y' if (wave == 5 | wave == 6) & treat == 2
	display in red "Treatment StDev = `r(sd)'"
	display " "				
}
	
	
	
	
	
	
	
	
	
* ---------------- Figure 3: average profit timeseries graph ------------------------- *


sort treat2 wave
by treat2 wave: egen avg_profit = mean(tprofits)


local new = _N + 6
set obs `new'

sum wave
replace months_since_treat = -1 if _n == `r(N)'+1
replace months_since_treat = -1 if _n == `r(N)'+2
replace months_since_treat = -1 if _n == `r(N)'+3
replace months_since_treat = 0 if _n == `r(N)'+4
replace months_since_treat = 0 if _n == `r(N)'+5
replace months_since_treat = 0 if _n == `r(N)'+6

replace treat  = 2 if _n == `r(N)'+1
replace treat  = 3 if _n == `r(N)'+2
replace treat  = 4 if _n == `r(N)'+3
replace treat  = 2 if _n == `r(N)'+4
replace treat  = 3 if _n == `r(N)'+5
replace treat  = 4 if _n == `r(N)'+6

gen shade=3500 if months_since_treat >= -1 & months_since_treat <= 0


sort months_since_treat
twoway(area shade months_since_treat,color(gs14))/*
*/ (connected avg_profit months_since_treat if treat2 == 2, lpattern(--.) color(navy)) /*
*/ (connected avg_profit months_since_treat if treat2 == 3, lpattern(dash) color(maroon)) /*
*/ (connected avg_profit months_since_treat if treat2 == 4, color(forest_green)), /*
*/ xlabel(-2(2)18)ytitle("Average Profit (Ksh)") graphregion(color(white) ilwidth(none)) xtitle("Months since treatment") /*
*/ legend(order(2 3 4) col(3) label(2 "Control") label(3 "Class") label(4 "Mentee")) name(Figure3)

graph export "plots/Figure3.eps", as(eps) preview(off) replace

	
	
	
	
* ---------------- Figure 6: fraction still meeting with mentors ------------------------- *

	
sort wave 
by wave: egen avg_meet = mean(meet)
replace months_since_treat = . if wave == 7
replace months_since_treat = . if months_since_treat < 0
local new = _N + 1
set obs `new'

sum wave
replace months_since_treat = 0 if _n == `r(N)' + 1
replace avg_meet = 1 if months_since_treat == 0

sort months_since_treat
twoway(connected avg_meet months_since_treat), /*
*/ xlabel(0 2 4 6 8 10 12) ytitle("Fraction still meeting with mentor") graphregion(color(white) ilwidth(none)) xtitle("Months since treatment") /*
*/ xscale(r(0 12)) yscale(r(0 1.0)) ylabel(0(0.2)1) name(Figure6)

graph export "plots/Figure6.eps", as(eps) preview(off) replace

	
	
	
	
* --------- Figure 7: Proift for those that meet and those that don't
drop treat2

gen treat2 = treat
replace treat2 = 5 if treat == 4 & meet == 1

sort treat2 wave
by treat2 wave: egen avg_profitm2 = mean(tprofits)


local new = _N + 4
set obs `new'

sum wave
replace months_since_treat = 0 if _n == `r(N)'+1
replace months_since_treat = 0 if _n == `r(N)'+2
replace months_since_treat = 0 if _n == `r(N)'+3
replace months_since_treat = 0 if _n == `r(N)'+4

replace treat2  = 2 if _n == `r(N)'+1
replace treat2  = 3 if _n == `r(N)'+2
replace treat2  = 4 if _n == `r(N)'+3
replace treat2  = 5 if _n == `r(N)'+4

sort months_since_treat
twoway(connected avg_profitm2 months_since_treat if treat2 == 4, lpattern(dash) color(black))  /*
*/ (connected avg_profitm2 months_since_treat if treat2 == 5, color(forest_green)), /*
*/ xlabel(1 4 8 12)ytitle("Average Profit (Ksh)") graphregion(color(white) ilwidth(none)) xtitle("Months since treatment") xscale(r(1 12)) /*
*/ legend(order(1 2) col(2) label(1 "Mentee (no meet)") label(2 "Mentee (meet)")) name(Figure7)

graph export "plots/Figure7.eps", as(eps) preview(off) replace





* --------- Figure 1 (uses baseline data)

use "datasets/BDJ_Baseline_Data.dta", clear



twoway(kdensity lprofit if youngfirm == 0) /*
*/ (kdensity lprofit if youngfirm == 1,lpattern(--)) if lprofit <= 14, /*
*/ ytitle("Density") xtitle("Log Monthly Profit (Ksh)") graphregion(color(white) ilwidth(none)) name(Figure1) /*
*/ legend(label(1 "Experienced") label(2 "Young"))
graph export "plots/Figure1.eps", as(eps) preview(off) replace


* --------- Figure 2 (uses baseline data)

keep binf gender bf avg_profit_agegen

sort bf
drop if bf[_n] == bf[_n-1]
destring(bin), replace

sort gender binf

gen _hold = avg_profit_agegen if bin == 1
by gender, sort: egen _hold2 = max(_hold)

gen avg_profit_agegen_norm = avg_profit_agegen/_hold2
drop _hold*

#delimit ;
 label define ages 
            1 "0-1"
            2 "1-5"
            3 "5-10"
            4 "10-15"
            5 "15-20"
			6 "> 20";	
#delimit cr		
	
label values binf ages			
	

twoway(connected avg_profit_agegen binf if gender == 0,lpattern(--)) /*
*/ (connected avg_profit_agegen binf if gender == 1), /*
*/ ytitle("Monthly Profit (Ksh)") xtitle("Business Experience (years)") graphregion(color(white) ilwidth(none)) name(Figure2a) /*
*/ xlabel(1/6,valuelabel) ylabel(10000(10000)30000) legend(label(1 "Male") label(2 "Female")) 
graph export "plots/Figure2a.eps", as(eps) preview(off) replace


twoway(connected avg_profit_agegen_norm binf if gender == 0,lpattern(--)) /*
*/ (connected avg_profit_agegen_norm binf if gender == 1), /*
*/ ytitle("Monthly Profit (normalized)") xtitle("Business Experience (years)") graphregion(color(white) ilwidth(none)) name(Figure2b) /*
*/ xlabel(1/6,valuelabel) ylabel(1(0.25)2.25) legend(label(1 "Male") label(2 "Female")) 
graph export "plots/Figure2b.eps", as(eps) preview(off) replace




	
	
	

log close
translate "logged_results/BDJ_MainTables.smcl" "logged_results/BDJ_MainTables.pdf", replace
erase "logged_results/BDJ_MainTables.smcl"
