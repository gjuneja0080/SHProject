clear all 
set more off
set matsize 800
cd  "/Users/kdonova6/Desktop/Papers/Dandora Mentors/"


* Set colors for graphs
local color_green_bar "132 186 91"
local color1 "127 201 127"
local color2 "190 174 212"
local color3 "253 192 134"
local color4 "255 255 153"

* Load data
use "datasets/BDJ_Dandora_Data.dta", clear
xtset id wave

tempfile data1 
save `data1'




* ---------------------------------------------
* HOW PERSISTENT ARE PROBLEMS? 
* (discussion at beginning of Section 5.3.1.)
* ---------------------------------------------

use `data1', clear
keep if wave == 0 | wave == 5
drop treat
rename treat2 treat

by id, sort: gen count5 = _N
keep if count5 == 2
drop count5
sort treat id wave
order treat

sort treat id wave
split difficulties, gen(tough)
destring(tough*), replace

sort id wave
forvalues i = 0/11 {
	gen istough_`i' = 0
	replace istough_`i' = 1 if tough1 == `i' | tough2 == `i' | tough3 == `i' | tough4 == `i' | tough5 == `i'	
	
	gen _hold = istough_`i' if wave == 0
	by id: egen istough0_`i' = max(_hold)
	drop _hold
	
	gen _hold = istough_`i' if wave == 5
	by id: egen istough5_`i' = max(_hold)
	drop _hold	
}

drop istough_*

sort id
drop if id[_n] == id[_n-1]
drop difficulties wave tough*

forvalues i = 0/11 {
	gen new_`i' = 0
	replace new_`i' = 1 if istough0_`i' == 0 & istough5_`i' == 1
	replace new_`i' = . if istough0_`i' != 0
	
	gen dropped_`i' = 0
	replace dropped_`i' = 1 if istough0_`i' == 1 & istough5_`i' == 0
	replace dropped_`i' = . if istough0_`i' != 1
}


egen probs0 = rsum(istough0_*)
egen probs5 = rsum(istough5_*)


sort treat
order treat id new_* dropped_* probs0 probs5

sort id
egen any_new = rmax(new_*)
egen any_drop = rmax(dropped_*)
egen sum_drop = rsum(dropped_*)
egen sum_new = rsum(new_*)
gen share_drop = sum_drop/probs0
gen share_new = sum_new/probs5


label var any_new " = 1 if mentions any issues at t=7 that aren't at t=1"
label var any_drop " = 1 if does not mention an issue at t=7 is mentioned at t=1"
label var share_new "Fraction of issues mentioned at t=7 that are not at t=1"
label var share_drop "Fraction of issues not mentioned at t=7 that are at t=1"

display in red "------------------------------------------------------ "
display in red "------------ SUMMARIZE FOR CONTROL ------------------- "
display in red "------------   (section 5.3.1.)    ------------------- "
display in red "------------------------------------------------------ "

sum any_new any_drop share_drop share_new if treat == 2








* ---------------------------------- 
* HOW DOES MENTOR ADVICE LINE UP WITH BASELINE DIFFICULTIES? (FIGURE 5A)
* ----------------------------------

use `data1', clear
keep if treat2 == 4


// Baseline difficulties
split difficulties, gen(tough)
destring(tough*), replace

sort id wave
forvalues i = 0/11 {
	gen _hold1 = 0 if wave == 0
	replace _hold1 = 1 if (tough1 == `i' | tough2 == `i' | tough3 == `i' | tough4 == `i' | tough5 == `i') & wave == 0	
	
	by id: egen diff0_`i' = max(_hold1)
	drop _hold1 
}



// Discuss with mentors: One year later. Asked to all mentees.
split discussever, p(" ")
destring(discussever*), replace

sort id
forvalues i = 1/10 {
	gen hold = 0
	replace hold = 1 if discussever1 == `i' | discussever2 == `i' | discussever3 == `i' | discussever4 == `i' | discussever5 == `i' 
	replace hold = 1 if discussever6 == `i' | discussever7 == `i' | discussever8 == `i' | discussever9 == `i' | discussever10 == `i'
	
	by id: egen discussever_`i' = max(hold)
	drop hold

}

keep if wave == 0
order id diff0_* discussever_*
keep id diff0_* discussever_*


forvalues j = 1/10 {

	egen mean_discussever_`j' = mean(discussever_`j')

	forvalues i = 0/11 {
		
		gen hold = discussever_`j' if diff0_`i' == 1
		egen mean_discussever_`j'_if`i' = mean(hold)
		drop hold
		
	}
}


// Set up dataset 
keep if _n == 1
keep mean_discussever_* 

gen discussever = 1
order discussever 
forvalues i = 0/11 {
	gen prob0_`i' = mean_discussever_1_if`i'
	drop mean_discussever_1_if`i'
}

gen allprobs = mean_discussever_1

order discussever prob0_* allprobs


forvalues j = 2/10 {
	local new = _N + 1
	set obs `new'
	
	replace discussever = `j' if missing(discussever)
	forvalues i = 0/11 {
		egen hold = max(mean_discussever_`j'_if`i')
		replace prob0_`i' = hold if missing(prob0_`i')
		drop mean_discussever_`j'_if`i' hold
	}
	
	egen hold = max(mean_discussever_`j')
	replace allprobs = hold if missing(allprobs)
	drop mean_discussever_`j' hold
	
}



label define newlab 1 "Attract customers" 2 "Product pricing" 3 "Lower cost" 4 "Product types" /*
*/ 5 "Location" 6 "Where to buy" 7 "Record keeping" 8 "New investments" 9 "Hours" 10 "Take out loans"
label values discussever newlab


// You can add whatever "baseline problems" you want to this graph. 
// Just make sure to update the legend.
graph hbar allprobs prob0_0 prob0_2 prob0_10, over(discussever, sort(allprobs) descending)/*
*/ ylabel(0(0.2)1.05) name(Figure_5a) blabel(discussever, position(base)) /*
*/ graphregion(color(white)) ytitle("Fraction of Businesses") /*
*/ legend(label(1 "All mentees") label(2 "Lack of funds") label(3 "Inventory/supplies") label(4 "Customers do not pay")) /*
*/ bar(1, color("`color1'") lcolor(black) lwidth(0.2)) bar(2, color("`color2'") lcolor(black) lwidth(0.2)) bar(3, color("`color3'") lcolor(black) lwidth(0.2)) bar(4, color("`color4'") lcolor(black) lwidth(0.2))

graph export "plots/Figure5a.eps", as(eps) preview(off) replace




* ---------------------------------- 
* HOW MANY TOPICS DO YOU DISCUSS WITH YOUR MENTOR? (FIGURE 5B)
* ----------------------------------

use `data1', clear
keep if treat2 == 4 & wave <= 6

gen wavem = wave if meet2 == 1
by id, sort: egen max_wave = max(wavem)
drop wavem


// Create discussion topics
split discuss, p(" ") gen(d_)
destring(d_*), replace

sort id
forvalues j = 1/10 {
	gen h = 0
	
	forvalues i = 1/11 {
		replace h = 1 if d_`i' == `j'
	}
	
	by id: egen t_`j' = max(h)
	drop h
}


gen topics = t_1 + t_2 + t_3 + t_4 + t_5 + t_6 + t_7 + t_8 + t_9 + t_10


keep if wave == 6
keep id topics max_wave

distplot bar topics if max_wave == 6 & topics >= 1, name(Figure_5b) /*
*/ xscale(r(0 10)) xlabel(0(1)10) graphregion(color(white)) ytitle("") xtitle("No. topics discussed") color("`color1'") lcolor(black) lwidth(0.2)
graph export "plots/Figure5b.eps", as(eps) preview(off) replace





* ---------------------------------- 
* HOW PERSISTENT ARE TOPICS? (FIGURE 5C)
* ----------------------------------

use `data1', clear
keep if treat2 == 4

sort id wave
drop if wave == 0 | wave == 7 /* nothing at baseline obviously, and not asked in 17-month followup */

keep if meet2 == 1
drop meet2


split(discuss), gen(d_) parse(" ")
destring(d_*), replace


forvalues i = 1/11 {
	gen discuss_`i' = 0
	replace discuss_`i' = 1 if d_1 == `i' | d_2 == `i' | d_3 == `i' | d_4 == `i' | d_5 == `i'
	replace discuss_`i' = 1 if d_6 == `i' | d_7 == `i' | d_8 == `i' | d_9 == `i' | d_10 == `i' | d_11 == `i'
}

drop d_* discuss

by id: gen diff = wave[_n] - wave[_n-1]

forvalues i = 1/11 {

	by id: gen twice0_`i' = 0 if discuss_`i'[_n-1] == 1 & diff == 1
	by id: replace twice0_`i' = 1 if discuss_`i'[_n] == 1 & discuss_`i'[_n-1] == 1 & diff == 1
	egen mean_twice0_`i' = mean(twice0_`i')
	
	by id: gen twice1_`i' = 0 if discuss_`i'[_n-1] == 1
	by id: replace twice1_`i' = 1 if discuss_`i'[_n] == 1 & discuss_`i'[_n-1] == 1 
	egen mean_twice1_`i' = mean(twice1_`i')	
}


egen mean_twice0 = rmean(twice0_*)
egen mean_twice1 = rmean(twice1_*)



// Set up dataset
keep if _n == 1
keep mean_twice0_* mean_twice1_*
gen discuss = 1
gen mean_twice0 = mean_twice0_1
gen mean_twice1 = mean_twice1_1

forvalues i = 2/10 { 
	local new = _N + 1
	set obs `new'
	replace discuss = `i' if missing(discuss)
	
	egen hold = max(mean_twice0_`i')
	replace mean_twice0 = hold if missing(mean_twice0)
	drop hold
	
	egen hold = max(mean_twice1_`i')
	replace mean_twice1 = hold if missing(mean_twice1)
	drop hold	
}


keep discuss mean_twice0 mean_twice1

label define newlab 1 "Attract customers" 2 "Product pricing" 3 "Lower cost" 4 "Product types" /*
*/ 5 "Location" 6 "Where to buy" 7 "Record keeping" 8 "New investments" 9 "Hours" 10 "Take out loans"
label values discuss newlab

graph hbar mean_twice1 mean_twice0, over(discuss, sort(mean_twice1) descending) /*
*/ ylabel(0(0.2)1.05) name(Figure_5c) blabel(prob, position(base)) /*
*/ graphregion(color(white)) ytitle("Fraction of Businesses") /*
*/ bar(1, color("`color1'") lcolor(black) lwidth(0.2)) bar(2, color("`color2'") lcolor(black) lwidth(0.2)) /*
*/ legend(label(1 "Consecutive observations") label(2 "Consecutive waves") col(1)) 
graph export "plots/Figure5c.eps", as(eps) preview(off) replace



