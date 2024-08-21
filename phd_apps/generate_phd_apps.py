import json
from datetime import datetime, timedelta

# Load the data from the JSON file
with open('programs.json', 'r') as file:
    programs = json.load(file)

# Extract deadlines from the JSON and convert them to a set of date objects
deadlines = {datetime.strptime(program['deadline'], '%Y-%m-%d').date() for program in programs}

deadline_counts = {}
for program in programs:
    deadline_date = program['deadline']
    if deadline_date in deadline_counts:
        deadline_counts[deadline_date] += 1
    else:
        deadline_counts[deadline_date] = 1

# Debug: Print parsed deadlines
print("Parsed Deadlines:", deadlines)

# Function to generate the calendar HTML for the next 60 days, organized by months
def generate_calendar(days):
    today = datetime.today()
    calendar_html = ''
    current_month = today.month
    month_days = []
    days_of_week = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    for i in range(days):
        current_date = today + timedelta(days=i)
        day = current_date.day
        day_of_week = (current_date.weekday() + 1) % 7  # Adjusting for Sunday-start week (0 = Sun, 1 = Mon, ..., 6 = Sat)

        # Check if we have moved to the next month or if it's the first day of iteration
        if current_date.month != current_month or i == 0:
            if month_days:
                calendar_html += '<tr>' + ''.join(month_days) + '</tr></table></div>'
            month_days = []
            current_month = current_date.month

            # Start a new section for the new month
            calendar_html += '<div>'
            calendar_html += '<table><tr>'
            for index, day_name in enumerate(days_of_week):
                if index == 0 or index == 6:  # Sunday or Saturday
                    calendar_html += f'<th class="weekend">{day_name}</th>'
                else:
                    calendar_html += f'<th>{day_name}</th>'
            calendar_html += '</tr><tr>'
            
            # Add empty cells if the month doesn't start on Sunday
            for _ in range(day_of_week):
                month_days.append('<td></td>')

        # Highlight the current day with a special class
        if i == 0:
            month_days.append(f'<td class="current-day">{day}</td>')
        elif current_date.date() in deadlines:
            # Link to the corresponding program div
            program_id = current_date.strftime('%Y_%m_%d')
            deadline_str = f'{day} ({deadline_counts[current_date.strftime("%Y-%m-%d")]} programs)'
            month_days.append(f'<td class="deadline-day"><a href="#{program_id}" class="deadline-link">{deadline_str}</a></td>')
        else:
            month_days.append(f'<td class="weekend">{day}</td>' if day_of_week == 0 or day_of_week == 6 else f'<td>{day}</td>')

        # Break to the next line after Saturday
        if day_of_week == 6:
            calendar_html += '<tr>' + ''.join(month_days) + '</tr>'
            month_days = []

    # Add the remaining days for the last month
    if month_days:
        calendar_html += '<tr>' + ''.join(month_days) + '</tr></table></div>'
    
    return calendar_html


# Generate the calendar HTML
calendar_html = generate_calendar(30)

# HTML template with placeholders
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PhD Application Tracker</title>
    <link rel="stylesheet" href="../styles.css">
    <style>
        .container {{ text-align: center; }}
        .title-section {{
            background-color: #fffec4;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            display: inline-block;
        }}
        .program {{
            margin: 20px auto;
            padding: 15px;
            background-color: #fffec4;
            border-radius: 10px;
            box-shadow: 2px 2px 8px rgba(0, 0, 0, 0.1);
            width: 70%;
            text-align: left;
        }}
        .program h2 {{ font-size: 1.5em; color: #333; }}
        .bold {{ font-weight: bold; }}
        .deadline-box {{
            border: 2px solid red;
            padding: 2px 5px;
            display: inline-block;
            border-radius: 5px;
        }}
        .application-link, .department-link, .overleaf-link {{ font-size: 1em; color: #007bff; }}
        .calendar {{
            margin: 20px auto;
            width: 80%;
            background-color: #fffec4;
            padding: 15px;
            border-radius: 10px;
        }}
        .calendar table {{ width: 100%; border-collapse: collapse; }}
        .calendar th, .calendar td {{ padding: 10px;
        border: 1px solid #ddd;
        text-align: center;
        width: 50px; /* Set a fixed width for all calendar cells */
        max-width: 50px; /* Ensure the width doesn't exceed this value */
        word-wrap: break-word; /* Break long words to fit the width */
        white-space: nowrap; /* Prevent text from wrapping */ }}
        .calendar th {{ background-color: #f2f2f2; }}
        .calendar .deadline-day {{
        border: 2px solid purple;
        padding: 2px 5px;
        border-radius: 5px;
        background-color: #e6e6ff; /* Optional: Light purple background */
        }}
        .calendar th.weekend, .calendar td.weekend {{
        color: red;
        }}
        .calendar .current-day {{
        border: 2px solid red;
        padding: 2px 5px;
        border-radius: 5px;
        background-color: #ffe6e6; /* Optional: Light red background */
        }}
        h3 {{
            text-align: left;
            margin-top: 20px;
            margin-bottom: 10px;
        }}
        .deadline-link {{
            color: inherit;
            text-decoration: none;
        }}
        .deadline-link:hover {{
            text-decoration: underline;
        }}
        
    </style>
</head>
<body>
    <div class="container">
        <div class="title-section">
            <h1>PhD Application Tracker</h1>
            <p>Dear Referees, please find below the details for each program I'm applying to. You can see my progress, the required documents, and find the email addresses or links to submit your recommendations. You can click on the date to jump to the program in question.</p>
        </div>

        <!-- Calendar Section -->
        <div class="calendar">
            <h2>Upcoming 30 Days</h2>
            {calendar_html}
        </div>

        {programs_html}
    </div>
</body>
</html>
"""

# Generate HTML for each program
programs_html = ""
for program in programs:
    # Convert the deadline to "14 September 2024" format
    deadline_date = datetime.strptime(program['deadline'], '%Y-%m-%d')
    formatted_deadline = deadline_date.strftime('%d %B %Y')

    # Create a unique ID for each program using its deadline
    program_id = program['deadline'].replace('-', '_')
    
    program_block = f"""
    <div id="{program_id}" class="program">
        <h2>{program['name']}</h2>
        <p><strong>Organising research institutes and universities:</strong> {program['institutes']}</p>
        <p><strong>Deadline:</strong> <span class="bold deadline-box">{formatted_deadline}</span></p>
        <p><strong>Point of contact:</strong> <span class="bold">{program['email']}</span></p>
        <p><strong>How to send reference letter:</strong> <span class="bold">{program['ref_letter']}</span></p>
        <p><strong>Link to advertisement:</strong> <a class="application-link" href="{program['ad_link']}">View Advertisement</a></p>
        <p><strong>Link to department(s):</strong> <a class="department-link" href="{program['dept_link']}">Department Website</a></p>
        <p><strong>Status:</strong> <span class="bold">{program['status']}</span></p>
        <p><strong>Cover letter and CV:</strong> <a class="overleaf-link" href="{program['cover_cv_link']}">Overleaf Link</a></p>
        <p><strong>Thoughts and comments:</strong> {program['comments']}</p>
    </div>
    """
    programs_html += program_block



# Insert the generated HTML into the template
final_html = html_template.format(programs_html=programs_html, calendar_html=calendar_html)

# Write the final HTML to a file
with open('phd_apps.html', 'w') as file:
    file.write(final_html)

print("HTML file generated successfully!")