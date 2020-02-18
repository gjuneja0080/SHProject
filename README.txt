
README file for Brooks, Donovan, and Johnson, "Mentors or Teachers? Microenterprise Training in Kenya,” AEJ:Applied
Last update: 10/30/2017
Program used: Stata 14



There are 3 do files included. They run separately and do not interact with each other.

1. MainTables - Main tables in text. At the end of the do file, figures from main text are created.
2. MenteeDiscussions - Creates Figure 5 and info for surrounding discussion in Section 5.3.1 about mentor-mentee discussion topics. Easier to do this one separately from the rest of the main results from the text. 
3. Appendix - All appendix regression results and figures

(1) and (3) create log files contained in */logged_results/ that include all regressions. (2) only creates a few numbers and graphs, so they are displayed in the command window. All figures are saved in */plots/ and are named according to the figure number in the text.


There are 3 dta files included in the */datasets/ folder:

1. BDJ_Dandora_data: This is the main times series data file from the RCT. It gets called by all 3 do files.
2. RD_Dataset: This file gets called for anything related to the regression discontinuity on mentors. It include the followup data from mentors and those below the cutoff. It gets used in MainTables.do and Appendix.do
3. BDJ_Baseline_data: This is the sectoral composition from the larger baseline survey. It gets used to create Figures 1 and 2 in the main text and also in the appendix. 

