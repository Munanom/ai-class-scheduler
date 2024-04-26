from flask import Flask, render_template, request
from constraint import Problem, AllDifferentConstraint
from collections import defaultdict
import openpyxl
import random

app = Flask(__name__)

# Define the available labs and time slots
labs = ["Lab 1", "Lab 2", "Lab 3", "Lab 4", "Lab 7", "GLab", "HLab", "SLab", "SHSS LAB"]
time_slots = ["07:00", "09:00", "11:00", "13:20", "15:30", "19:20"]

# Function to read sample data from an Excel file, reading only the first 7 columns and stopping when there's no more data
def read_sample_data(file_path):
    data = []
    wb = openpyxl.load_workbook(file_path, read_only=True)
    ws = wb.active
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[:7] == (None,) * 7:  # Stop when there are no more data in the first 7 columns
            break
        data.append(row[:7])
    return data

# Function to assign labs to classes without collisions
def assign_labs(classes):
    problem = Problem()
    class_mapping = defaultdict(bool)  # Keep track of duplicated classes
    
    # Define variables representing each class
    for class_data in classes:
        random.shuffle(labs)
        start_time, days, course_no, section, course_title, faculty, capacity = class_data
        variable_name = f"{course_no}_{section}"
        # Check if class is already added
        if not class_mapping[variable_name]:
            problem.addVariable(variable_name, labs)
            class_mapping[variable_name] = True

    # Define constraints to avoid collisions of labs
    for time_slot in time_slots:
        classes_at_same_time = [f"{class_data[2]}_{class_data[3]}" for class_data in classes if class_data[0] == time_slot]
        problem.addConstraint(AllDifferentConstraint(), classes_at_same_time)

    # Solve the problem
    solution = problem.getSolution()

    # Print message for removed duplicate classes
    for class_data in classes:
        variable_name = f"{class_data[2]}_{class_data[3]}"
        if not class_mapping[variable_name]:
            print(f"Duplicate class {class_data[4]} ({class_data[2]}_{class_data[3]}) removed.")
    
    return solution

# Function to print schedule in table format
def print_schedule(schedule, classes):
    schedule_table = []
    for time_slot in time_slots:
        classes_assigned = [class_data for class_data in classes if schedule.get(f"{class_data[2]}_{class_data[3]}") is not None and class_data[0] == time_slot]
        if classes_assigned:
            row = []
            for i, class_data in enumerate(classes_assigned):
                row.append(f"{time_slot}")
                row.append(f"{class_data[4]}")
                row.append(f"{class_data[2]}_{class_data[3]}")
                row.append(f"{class_data[5]}")
                row.append(schedule.get(f'{class_data[2]}_{class_data[3]}'))
                if (i + 1) % 5 == 0 or i == len(classes_assigned) - 1:  # Add a new row after every 5 items or if it's the last item
                    schedule_table.append(row)
                    row = []  # Reset the row for the next set of items
        else:
            schedule_table.append([time_slot, "", "", "", ""])
    
    return schedule_table


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            file.save("uploaded_file.xlsx")
            sample_data = read_sample_data('uploaded_file.xlsx')
            MW_classes = [data for data in sample_data if "MW" in data[1]]
            TR_classes = [data for data in sample_data if "TR" in data[1]]
            MW_schedule = assign_labs(MW_classes)
            TR_schedule = assign_labs(TR_classes)
            MW_schedule_table = print_schedule(MW_schedule, MW_classes)
            TR_schedule_table = print_schedule(TR_schedule, TR_classes)
            return render_template('schedule.html', MW_schedule=MW_schedule_table, TR_schedule=TR_schedule_table)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)