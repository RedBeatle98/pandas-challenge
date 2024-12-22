import pandas as pd
import numpy as np

school_data_to_load = "raw_data/schools_complete.csv"
student_data_to_load = "raw_data/students_complete.csv"

school_data = pd.read_csv(school_data_to_load)
student_data = pd.read_csv(student_data_to_load)

school_data_complete = pd.merge(student_data, school_data, how="left", on=["school_name", "school_name"])


# District Summary

total_number_of_unique_schools = len(school_data_complete["school_name"].unique)
total_students = school_data_complete["Student ID"].count
total_budget = school_data_complete["budget"].sum
average_math_score = school_data_complete["math_score"].mean
average_reading_score = school_data_complete["reading_score"].mean
percentage_passing_math = school_data_complete[(school_data_complete["math_score"] >= 70)].count()["student_name"] / total_students * 100
percentage_passing_reading = school_data_complete[(school_data_complete["reading_score"] >= 70)].count()["student_name"] / total_students * 100
percentage_overall_passing = school_data_complete[(school_data_complete["math_score"] >= 70) & (school_data_complete["reading_score"] >= 70)].count()["student_name"] / total_students * 100

district_summary = pd.DataFrame({"Total Number of Unique Schools": [total_number_of_unique_schools], "Total Students": [total_students], "Total Budget": [total_budget], "Average Math Score": [average_math_score], "Average Reading Score": [average_reading_score], "% Passing Math": [percentage_passing_math], "% Passing Reading": [percentage_passing_reading], "% Overall Passing": [percentage_overall_passing]})


# School Summary

school_name = school_data_complete.set_index('school_name').groupby(['school_name'])
school_type = school_data.set_index('school_name')['type']
total_student = school_name['Student ID'].count()
total_school_budget = school_data.set_index('school_name')['budget']
budget_per_student = (school_data.set_index('school_name')['budget']/school_data.set_index('school_name')['size'])
average_math_score = school_name['math_score'].mean()
average_reading_score = school_name['reading_score'].mean()
pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('school_name')['Student ID'].count() / total_student * 100
pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('school_name')['Student ID'].count() / total_student * 100
overall_pass = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('school_name')['Student ID'].count() / total_student * 100

school_summary = pd.DataFrame({"School Type": school_type, "Total Students": total_student, "Per Student Budget": budget_per_student, "Total School Budget": total_school_budget, "Average Math Score": average_math_score, "Average Reading Score": average_reading_score, "% Passing Math": pass_math_percent, "% Passing Reading": pass_read_percent, "% Overall Passing": overall_pass})

# Highest-Performing Schools (by % Overall Passing)

top_perform = school_summary.sort_values("% Overall Passing", ascending = False)

# Lowest-Performing Schools (by % Overall Passing)

bottom_perform = top_perform.tail()

# Math Scores by Grade

ninth_math = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["math_score"].mean()
tenth_math = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["math_score"].mean()
eleventh_math = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["math_score"].mean()
twelfth_math = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["math_score"].mean()

math_scores = pd.DataFrame({
        "9th": ninth_math,
        "10th": tenth_math,
        "11th": eleventh_math,
        "12th": twelfth_math
})
math_scores = math_scores[['9th', '10th', '11th', '12th']]
math_scores.index.name = "School Name"


# Reading Scores by Grade

ninth_reading = student_data.loc[student_data['grade'] == '9th'].groupby('school_name')["reading_score"].mean()
tenth_reading = student_data.loc[student_data['grade'] == '10th'].groupby('school_name')["reading_score"].mean()
eleventh_reading = student_data.loc[student_data['grade'] == '11th'].groupby('school_name')["reading_score"].mean()
twelfth_reading = student_data.loc[student_data['grade'] == '12th'].groupby('school_name')["reading_score"].mean()

reading_scores = pd.DataFrame({
        "9th": ninth_reading,
        "10th": tenth_reading,
        "11th": eleventh_reading,
        "12th": twelfth_reading
})
reading_scores = reading_scores[['9th', '10th', '11th', '12th']]
reading_scores.index.name = "School Name"

# Scores by School Spending

bins = [0, 584, 629, 644, 675]
group_name = ["<$584", "$585-629", "$630-644", "$645-675"]

school_data_complete['spending_bins'] = pd.cut(school_data_complete['budget']/school_data_complete['size'], bins, labels = group_name)

#group by spending

by_spending = school_data_complete.groupby('spending_bins')


avg_math = by_spending['math_score'].mean()

avg_read = by_spending['reading_score'].mean()
pass_math = school_data_complete[school_data_complete['math_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
pass_read = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('spending_bins')['Student ID'].count()/by_spending['Student ID'].count()*100
         
scores_by_spend = pd.DataFrame({
    "Average Math Score": avg_math,
    "Average Reading Score": avg_read,
    "% Passing Math": pass_math,
    "% Passing Reading": pass_read,
    "% Overall Passing": overall
            
})
            
scores_by_spend = scores_by_spend[[
    "Average Math Score",
    "Average Reading Score",
    "% Passing Math",
    "% Passing Reading",
    "% Overall Passing"
]]

scores_by_spend.index.name = "Per Student Budget"

# Scores by School Size

bins = [0, 1000, 1999,5000]
group_name = ["Small (<1000)", "Medium (1000-2000)" , "Large (2000-5000)"]
school_data_complete['size_bins'] = pd.cut(school_data_complete['size'], bins, labels = group_name)

by_size = school_data_complete.groupby('size_bins')

average_math_score = by_size['math_score'].mean()
average_reading_score = by_size['math_score'].mean()
pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100
pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('size_bins')['Student ID'].count()/by_size['Student ID'].count()*100
        
scores_by_size = pd.DataFrame({
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math_percent,
    '% Passing Reading': pass_read_percent,
    '% Overall Passing': overall
            
})
            
scores_by_size = scores_by_size[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    '% Overall Passing'
]]

scores_by_size.index.name = "Total Students"
scores_by_size = scores_by_size.reindex(group_name)

# Scores by School Type

schoo_type = school_data_complete.groupby("type")

average_math_score = schoo_type['math_score'].mean()
average_reading_score = schoo_type['math_score'].mean()
pass_math_percent = school_data_complete[school_data_complete['math_score'] >= 70].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100
pass_read_percent = school_data_complete[school_data_complete['reading_score'] >= 70].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100
overall = school_data_complete[(school_data_complete['reading_score'] >= 70) & (school_data_complete['math_score'] >= 70)].groupby('type')['Student ID'].count()/schoo_type['Student ID'].count()*100
          
scores_school_type = pd.DataFrame({
    "Average Math Score": average_math_score,
    "Average Reading Score": average_reading_score,
    '% Passing Math': pass_math_percent,
    '% Passing Reading': pass_read_percent,
    "% Overall Passing": overall})
    

scores_school_type = scores_school_type[[
    "Average Math Score",
    "Average Reading Score",
    '% Passing Math',
    '% Passing Reading',
    "% Overall Passing"
]]
scores_school_type.index.name = "Type of School"
