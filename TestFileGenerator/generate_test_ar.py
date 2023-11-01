import pandas as pd
import random

# 生成单个学生的学术成绩数据
sid = '12345678'
subjects = ['Math', 'English', 'Science']
semesters = ['第一学期', '第二学期']
grades = [random.choice(['A', 'B', 'C', 'D', 'E', 'F']) for _ in range(len(subjects) * len(semesters))]

# 创建 Excel 文件
excel_file = f'Online-Learning-Platform/data/academicRecordsData/ar{sid}.xlsx'
writer = pd.ExcelWriter(excel_file)

# 填充数据框并写入不同工作表
subject_num = 1
for semester in semesters:
    # 创建数据框
    data = pd.DataFrame({'学科编号': [subject_num] * len(subjects),
                         '成绩': grades[(len(subjects) * (semesters.index(semester))):(len(subjects) * (semesters.index(semester) + 1))]})
    
    # 将数据写入工作表
    data.to_excel(writer, sheet_name=semester, index=False)

# 保存 Excel 文件
writer._save()

print("学术成绩试算表已生成并保存。")