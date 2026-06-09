import pandas as pd

def export_students(data):

    df = pd.DataFrame(data)

    file_name = "student_data/students.xlsx"

    df.to_excel(file_name, index=False)

    return file_name