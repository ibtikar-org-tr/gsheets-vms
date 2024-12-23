import requests
import os

# Function to list enrolled users' mails in a Moodle course
def get_enrolled_users_emails(course_id):
    """
    Retrieve the list of enrolled user emails for a specific Moodle course.
    
    Args:
        course_id (int): The ID of the Moodle course.

    Returns:
        list: A list of email addresses of enrolled users.
    """
    # Moodle API endpoint
    endpoint = f"{os.getenv('MOODLE_BASE_URL')}/webservice/rest/server.php"
    
    # API parameters
    params = {
        'wstoken': os.getenv('MOODLE_TOKEN'),
        'wsfunction': 'core_enrol_get_enrolled_users',
        'moodlewsrestformat': 'json',
        'courseid': course_id
    }
    
    try:
        # Make the API request
        response = requests.get(endpoint, params=params)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Parse the JSON response
        users = response.json()
        
        # Extract email addresses
        emails = [user['email'] for user in users if 'email' in user]
        
        return emails
    except requests.exceptions.RequestException as e:
        print(f"Error fetching enrolled users: {e}")
        return []
    except KeyError:
        print("Unexpected response format. Check the API token or endpoint.")
        return []

# Function to enroll students to a course by email
def enroll_students_to_course_by_mail(course_id, user_email, role_id=5):
    """
    Enrolls a list of students into a Moodle course.

    Args:
        course_id (int): The ID of the Moodle course.
        user_email: The email address of the user to enroll.
        role_id (int): The role ID to assign (default is 5 for students).

    Returns:
        dict: A dictionary with success and error information.
    """
    # Moodle API endpoint
    endpoint = f"{os.getenv('MOODLE_BASE_URL')}/webservice/rest/server.php"
    
    user_id = get_user_id_by_field(user_email[0], "email")

    # API parameters for enrollment
    params = {
    "wstoken": os.getenv('MOODLE_TOKEN'),
    "wsfunction": "enrol_manual_enrol_users",
    "moodlewsrestformat": "json",
    "enrolments[0][roleid]": role_id,
    "enrolments[0][userid]": user_id,
    "enrolments[0][courseid]": course_id,
    }

    try:
        # Make the API request
        response = requests.post(endpoint, json=params)
        response.raise_for_status()
        return {"success": True, "message": "User enrolled successfully."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Error enrolling user {user_email}: {e}"}

# Function to fetch user ID by username or email
def get_user_id_by_field(input_value: str, field: str = "username"):
    # Moodle API endpoint
    endpoint = f"{os.getenv('MOODLE_BASE_URL')}/webservice/rest/server.php"

    params = {
        'wstoken': os.getenv('MOODLE_TOKEN'),
        'wsfunction': 'core_user_get_users_by_field',
        'moodlewsrestformat': 'json',
        'field': field, # field can be 'id' or 'idnumber' or 'username' or 'email'
        'values[0]': input_value
    }
    try:
        userdata = requests.post(endpoint, data=params)
        userID = userdata.json()[0]['id']
        return userID
    except Exception as e:
        print(f"Error fetching user ID for {input_value}: {e}")
        return None

# Loop through the list of emails and enroll them in the course
def check_course_mails(course_link: str, page_mails: list):
    try:
        course_id = course_link.split('id=')[1].split('&')[0]
    except Exception as e:
        print(f"Error parsing Moodle course ID {course_link}: {e}")
        return
    enrolled_users = get_enrolled_users_emails(course_id)
    
    will_be_added = [mail for mail in page_mails if mail not in enrolled_users]
    # will_be_removed = [mail for mail in enrolled_users if mail not in page_mails]
    
    for mail in will_be_added:
        response = enroll_students_to_course_by_mail(course_id = course_id, user_email = mail)
        print(response)

