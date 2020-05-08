
README file for Gopal Juneja, "Mentors or Teachers? Microenterprise Training in Kenya,” 
Program used: Stata,Python


There are 4 .py files included. They run separately and do not interact with each other.

1. MainTables - Main tables in text. At the end of the do file, figures from main text are created.
2. MenteeDiscussions - About mentor-mentee discussions.
3. Appendix - All appendix regression results and figures
4. Visualisations - for the visualisations to run.

There are 2 ipynb files:
1. Appendix.ipynb
2. mainTables.ipynb

There is a tableau workbook:
1. SHProject.twbx

All figures are saved in */visualsations/ and are named according to the figure number in the text.


There are 3 .csv files included in the */datasets/ folder:

1. BDJ_Dandora_data: This is the main times series data file from the RCT. It gets called by all 3 do files.
2. RD_Dataset: This file gets called for anything related to the regression discontinuity on mentors. It include the followup data from mentors and those below the cutoff. It gets used in MainTables.do and Appendix.do
3. BDJ_Baseline_data: This is the sectoral composition from the larger baseline survey. It gets used to create Figures 1 and 2 in the main text and also in the appendix. 

