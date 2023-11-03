import pandas as pd
import random

# 產生單一學生的學術成績數據
sid = '12345678'
subjects = ['Math', 'English', 'Science']
semesters = ['第一學期', '第二學期']
grades = [random.choice(['A', 'B', 'C', 'D', 'E', 'F']) for _ in range(len(subjects) * len(semesters))]

# 建立 Excel 文件
excel_file = f'Online-Learning-Platform/data/academicRecordsData/ar{sid}.xlsx'
writer = pd.ExcelWriter(excel_file)

# 填充資料框並寫入不同工作表
subject_num = 1
for semester in semesters:
    # 建立資料框
    data = pd.DataFrame({'學科编號': [subject_num] * len(subjects),
                         '成績': grades[(len(subjects) * (semesters.index(semester))):(len(subjects) * (semesters.index(semester) + 1))]})
    
    # 將資料寫入工作表
    data.to_excel(writer, sheet_name=semester, index=False)

# 儲存 Excel 文件
writer._save()

print("學術成績試算表已產生並保存。")