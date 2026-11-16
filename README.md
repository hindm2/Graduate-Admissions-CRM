
# Graduate Admissions CRM Simulation

A Slate-inspired graduate admissions CRM simulation developed using Python, pandas, and Streamlit.

## Project Overview

This project simulates a graduate admissions recruitment workflow, helping admissions teams manage prospective student records, track applications, document recruitment activities, and organize follow-up tasks.

The application uses fictional student data and was developed as an independent portfolio project.

## Key Features

### Recruitment Dashboard
- Track prospective students, submitted applications, and enrolled students.
- Visualize application pipeline stages.
- Analyze graduate program interest and recruitment sources.

### Student Management
- Search prospective students by name or email.
- Filter records by program and application status.
- View individual student profiles.
- Update application statuses.

### Recruitment Activity Tracking
- Record emails, phone calls, webinars, and meetings.
- Maintain a history of student interactions.

### Follow-Up Task Management
- Create follow-up tasks for prospective students.
- Edit task descriptions and due dates.
- Reschedule and delete tasks.
- Mark tasks as completed.
- Monitor overdue, due-today, upcoming, and completed tasks.

## Technologies Used

- Python
- pandas
- Streamlit
- CSV files for data storage
- Custom Streamlit theme and CSS

## How to Run the Application

1. Clone the repository.
2. Install the required libraries:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the application:

   ```bash
   streamlit run app.py
   ```

## Project Purpose

This project demonstrates how data analytics and workflow management can support graduate admissions recruitment.

It combines interactive dashboards, student engagement tracking, data management, and task prioritization in a single application.

## Limitations

- All student records are fictional.
- This is a Slate-inspired simulation, not an integration with the actual Slate CRM.
- CSV-based storage is intended for demonstration rather than production use.
- The application does not include authentication or role-based access controls.

## Future Improvements

- Database integration
- User authentication
- Automated follow-up reminders
- Additional recruitment analytics
