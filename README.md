# Lab Scheduler

This is a Flask application that helps assign labs to classes without collisions. It takes an Excel file as input, which contains class information such as start time, days, course number, section, course title, faculty, and capacity.

## Features

- Reads sample data from an Excel file
- Assigns labs to classes without collisions using a constraint satisfaction problem
- Removes duplicate classes
- Prints the schedule in a table format for both Monday-Wednesday (MW) and Tuesday-Thursday (TR) classes

## Getting Started

1. Clone the repository
2. Install the required dependencies: `pip install flask openpyxl`
3. Run the Flask application: `python scheduler.py`
4. Access the application in your web browser at `http://localhost:5000`

## How to Use

1. Click the "Choose File" button and select the Excel file containing the class information
2. Click the "Upload" button
3. The application will assign labs to classes and display the schedule in a table format for both MW and TR classes

## File Structure

- `scheduler.py`: The main Flask application file
- `uploaded_file.xlsx`: The Excel file containing the class information (uploaded by the user)
- `templates/upload.html`: The HTML template for the file upload page
- `templates/schedule.html`: The HTML template for displaying the generated schedule

## Dependencies

- Flask: A lightweight Python web framework
- openpyxl: A Python library for reading and writing Excel files
- constraint: A Python library for solving constraint satisfaction problems (CSPs)

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).