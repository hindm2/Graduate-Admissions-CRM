
import streamlit as st
import pandas as pd

# Configure the application
st.set_page_config(
    page_title="Graduate Admissions CRM",
    page_icon="🎓",
    layout="wide"
)

# Load student records from our CSV
students = pd.read_csv("students.csv")

# Load recruitment activity records
activities = pd.read_csv("activities.csv")

# Load follow-up tasks
followups = pd.read_csv("followups.csv")



# Dashboard title
st.title("🎓 Graduate Admissions CRM")
st.write("Slate-style recruitment and admissions simulation")

# Calculate recruitment metrics
total_students = len(students)

applications = students[
    students["application_status"].isin(
        ["Applied", "Admitted", "Enrolled"]
    )
].shape[0]

enrolled = students[
    students["application_status"] == "Enrolled"
].shape[0]


# Display dashboard metrics
st.subheader("Recruitment Dashboard")

# Custom styling for KPI cards
st.markdown("""
<style>
div[data-testid="stMetric"] {
    background-color: #D0EEE9;
    border: 1px solid #B5DDD7;
    border-left: 5px solid #087F8C;
    border-radius: 12px;
    padding: 20px;
    box-shadow: 0 3px 10px rgba(18, 60, 70, 0.08);
}

div[data-testid="stMetricLabel"] {
    color: #123C46;
    font-weight: 600;
}

div[data-testid="stMetricValue"] {
    color: #087F8C;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Prospective Students", total_students)

with col2:
    st.metric("Applications Submitted", applications)

with col3:
    st.metric("Students Enrolled", enrolled)


# Analyze students by application status
st.subheader("Application Pipeline")

status_counts = (
    students["application_status"]
    .value_counts()
)

# Display the results as a bar chart
st.bar_chart(status_counts)

# Analyze students by graduate program
st.subheader("Prospective Students by Program")

program_counts = students["program"].value_counts()

st.bar_chart(program_counts)

# Analyze recruitment sources
st.subheader("Prospective Students by Recruitment Source")

source_counts = students["recruitment_source"].value_counts()

st.bar_chart(source_counts)

# Centralized follow-up dashboard
st.subheader("Pending Follow-Up Tasks")

# Find all pending tasks across all students
all_pending = followups[
    followups["status"] == "Pending"
].copy()

# Connect tasks to student information
pending_with_students = all_pending.merge(
    students[["student_id", "first_name", "last_name", "program"]],
    on="student_id",
    how="left"
)

# Sort pending tasks by due date (earliest first)
pending_with_students["due_date"] = pd.to_datetime(
    pending_with_students["due_date"],
    format="mixed"
)

pending_with_students = pending_with_students.sort_values(
    by="due_date",
    ascending=True
)


# Display all pending tasks
if pending_with_students.empty:
    st.info("No pending follow-up tasks.")
else:
    st.dataframe(
        pending_with_students,
        use_container_width=True,
        hide_index=True
    )

# Reschedule an existing follow-up task
st.subheader("Reschedule Follow-Up Task")

if not all_pending.empty:

    task_to_reschedule = st.selectbox(
        "Select task ID to reschedule",
        all_pending["task_id"].tolist()
    )

    # Find the current due date of the selected task
    current_task = all_pending[
        all_pending["task_id"] == task_to_reschedule
    ].iloc[0]

    current_due_date = pd.to_datetime(
        current_task["due_date"],
        format="mixed"
    ).date()

    # Select a new due date
    new_due_date = st.date_input(
        "New Due Date",
        value=current_due_date
    )

    if st.button("Update Due Date"):

        # Update only the selected task
        followups.loc[
            followups["task_id"] == task_to_reschedule,
            "due_date"
        ] = new_due_date.isoformat()

        # Save the updated dataset
        followups.to_csv("followups.csv", index=False)

        st.success("Task due date updated!")
        st.rerun()

else:
    st.info("No pending tasks available to reschedule.")


# Daily task overview
st.subheader("Daily Task Overview")

# Convert due dates into datetime values
followups["due_date"] = pd.to_datetime(
    followups["due_date"],
    format="mixed"
)

# Get today's date
today = pd.Timestamp.today().normalize()

# Separate pending and completed tasks
pending_tasks_all = followups[
    followups["status"] == "Pending"
]

completed_tasks = followups[
    followups["status"] == "Completed"
]

# Pending tasks with past due dates
overdue_tasks = pending_tasks_all[
    pending_tasks_all["due_date"] < today
]

# Pending tasks due today
due_today_tasks = pending_tasks_all[
    pending_tasks_all["due_date"] == today
]

# Pending tasks due in the future
upcoming_tasks = pending_tasks_all[
    pending_tasks_all["due_date"] > today
]

# Display the four task categories
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Overdue", len(overdue_tasks))

with col2:
    st.metric("Due Today", len(due_today_tasks))

with col3:
    st.metric("Upcoming", len(upcoming_tasks))

with col4:
    st.metric("Completed", len(completed_tasks))


# Display student records
st.subheader("Student Records")


# Search students by name or email
search = st.text_input(
    "Search students by name or email"
)
#
program = st.selectbox(
    "Select program",
    ["All Programs"] + sorted(
        students["program"].unique().tolist()
    )
)

# Filter students by application status

statuses = st.multiselect(
    "Select application statuses",
    options=sorted(
        students["application_status"].unique().tolist()
    ),
    default=[]
)






# Start with all students
filtered_students = students.copy()

# Apply the search
if search:
    full_names = (
        filtered_students["first_name"] + " " +
        filtered_students["last_name"]
    )

    filtered_students = filtered_students[
        full_names.str.contains(search, case=False, regex=False) |
        filtered_students["email"].str.contains(
            search, case=False, regex=False
        )
    ]

# Apply the program filter
if program != "All Programs":
    filtered_students = filtered_students[
        filtered_students["program"] == program
    ]

# Apply the application status filter

if statuses:
    filtered_students = filtered_students[
        filtered_students["application_status"].isin(statuses)
    ]

    

st.write(f"Showing {len(filtered_students)} student(s)")


st.dataframe(
    filtered_students,
    use_container_width=True,
    hide_index=True
)

st.caption("All student records are fictional.")

# Individual student profile
st.subheader("Student Profile")

# Create a list of student IDs from the filtered records
student_ids = filtered_students["student_id"].tolist()

# Allow the user to select a student
if student_ids:
    selected_id = st.selectbox(
        "Select a student ID",
        student_ids
    )

    # Find the selected student's record
    selected_student = filtered_students[
        filtered_students["student_id"] == selected_id
    ]

    # Display the student's information
   
    # Convert the selected student's row into a Series
    student = selected_student.iloc[0]

    # Display the student profile
    st.subheader(
        f"{student['first_name']} {student['last_name']}"
    )

    st.write(f"**Student ID:** {student['student_id']}")
    st.write(f"**Email:** {student['email']}")
    st.write(f"**Program:** {student['program']}")
    st.write(
        f"**Recruitment Source:** {student['recruitment_source']}"
    )
    st.write(
        f"**Application Status:** {student['application_status']}"
    )

    # Update student application status
    st.subheader("Update Application Status")

    # Available application statuses
    status_options = [
        "Inquiry",
        "Interested",
        "Applied",
        "Admitted",
        "Enrolled"
    ]

    # Show the student's current status by default
    current_status = student["application_status"]

    new_status = st.selectbox(
        "New application status",
        status_options,
        index=status_options.index(current_status)
    )

    if st.button("Save Changes"):

        # Update the student's status in the DataFrame
        students.loc[
            students["student_id"] == selected_id,
            "application_status"
        ] = new_status

        # Save the updated dataset to CSV
        students.to_csv("students.csv", index=False)

        st.success("Student status updated successfully!")

        # Refresh the application
        st.rerun()

    # Record recruitment activities
    st.subheader("Record Recruitment Activity")

    with st.form("activity_form"):
        activity_type = st.selectbox(
            "Activity Type",
            ["Email", "Phone Call", "Webinar", "Meeting"]
        )

        activity_date = st.date_input(
            "Activity Date"
        )

        activity_notes = st.text_area(
            "Activity Notes"
        )

        save_activity = st.form_submit_button(
            "Save Activity"
        )

    # Save the recruitment activity
    if save_activity:

        # Generate a unique activity ID
        if activities.empty:
            new_activity_id = 1
        else:
            new_activity_id = int(activities["activity_id"].max()) + 1

        # Create a new activity record
        new_activity = pd.DataFrame([{
            "activity_id": new_activity_id,
            "student_id": selected_id,
            "activity_type": activity_type,
            "activity_date": activity_date.isoformat(),
            "notes": activity_notes
        }])

        # Add the new activity to existing records
        activities = pd.concat(
            [activities, new_activity],
            ignore_index=True
        )

        # Save the updated dataset
        activities.to_csv("activities.csv", index=False)

        st.success("Recruitment activity saved successfully!")
        st.rerun()

    
    # Display recruitment activity history
    st.subheader("Recruitment Activity History")

    # Find activities belonging to the selected student
    student_activities = activities[
        activities["student_id"] == selected_id
    ]

    if student_activities.empty:
        st.info("No recruitment activities recorded for this student.")
    else:
        st.dataframe(
            student_activities,
            use_container_width=True,
            hide_index=True
        )
    
    # Follow-up task management
    st.subheader("Create Follow-Up Task")

    with st.form("followup_form"):
        task_description = st.text_area(
            "Task Description",
            placeholder="Example: Send application reminder"
        )

        due_date = st.date_input(
            "Follow-Up Due Date"
        )

        save_followup = st.form_submit_button(
            "Save Follow-Up Task"
        )

    # Save the follow-up task
    if save_followup:

        if not task_description.strip():
            st.warning("Please enter a task description.")

        else:
            # Generate a unique task ID
            if followups.empty:
                new_task_id = 1
            else:
                new_task_id = int(followups["task_id"].max()) + 1

            # Create a new follow-up record
            new_followup = pd.DataFrame([{
                "task_id": new_task_id,
                "student_id": selected_id,
                "task_description": task_description.strip(),
                "due_date": due_date.isoformat(),
                "status": "Pending"
            }])

            # Add the task to existing follow-ups
            followups = pd.concat(
                [followups, new_followup],
                ignore_index=True
            )

            # Save the updated data to CSV
            followups.to_csv("followups.csv", index=False)

            st.success("Follow-up task saved successfully!")
            st.rerun()
    
    # Display follow-up tasks for the selected student
    st.subheader("Student Follow-Up Tasks")

    student_followups = followups[
        followups["student_id"] == selected_id
    ]

    if student_followups.empty:
        st.info("No follow-up tasks for this student.")
    else:
        st.dataframe(
            student_followups,
            use_container_width=True,
            hide_index=True
        )


    # Manage existing follow-up tasks for selected student
    if not student_followups.empty:

        # EDIT TASK
        st.subheader("Edit Follow-Up Task")

        edit_task_id = st.selectbox(
            "Select task ID to edit",
            student_followups["task_id"].tolist(),
            key="edit_task"
        )

        task_to_edit = student_followups[
            student_followups["task_id"] == edit_task_id
        ].iloc[0]

        edited_description = st.text_input(
            "Edit task description",
            value=str(task_to_edit["task_description"]),
            key=f"description_{edit_task_id}"
        )

        edited_due_date = st.date_input(
            "Edit task due date",
            value=pd.to_datetime(
                task_to_edit["due_date"],
                format="mixed"
            ).date(),
            key=f"date_{edit_task_id}"
        )

        if st.button("Save Task Changes"):
            if not edited_description.strip():
                st.warning("Please enter a task description.")
            else:
                mask = (
                    (followups["task_id"] == edit_task_id) &
                    (followups["student_id"] == selected_id)
                )

                followups.loc[mask, "task_description"] = (
                    edited_description.strip()
                )
                followups.loc[mask, "due_date"] = (
                    edited_due_date.isoformat()
                )

                followups.to_csv("followups.csv", index=False)
                st.rerun()

        # DELETE TASK
        st.subheader("Delete Follow-Up Task")

        delete_task_id = st.selectbox(
            "Select task ID to delete",
            student_followups["task_id"].tolist(),
            key="delete_task"
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to permanently delete this task"
        )

        if st.button(
            "Delete Selected Task",
            disabled=not confirm_delete
        ):
            followups = followups[
                ~(
                    (followups["task_id"] == delete_task_id) &
                    (followups["student_id"] == selected_id)
                )
            ].copy()

            followups.to_csv("followups.csv", index=False)
            st.rerun()

        # COMPLETE TASK
        pending_tasks = student_followups[
            student_followups["status"] == "Pending"
        ]

        if not pending_tasks.empty:
            st.subheader("Complete a Follow-Up Task")

            selected_task_id = st.selectbox(
                "Select a pending task ID",
                pending_tasks["task_id"].tolist()
            )

            if st.button("Mark Task as Completed"):
                mask = (
                    (followups["task_id"] == selected_task_id) &
                    (followups["student_id"] == selected_id)
                )

                followups.loc[mask, "status"] = "Completed"
                followups.to_csv("followups.csv", index=False)
                st.rerun()
