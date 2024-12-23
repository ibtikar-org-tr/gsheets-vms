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
        email_list (list): A list of email addresses of the students to enroll.
        role_id (int): The role ID to assign (default is 5 for students).

    Returns:
        dict: A dictionary with success and error information.
    """
    # Moodle API endpoint
    endpoint = f"{os.getenv('MOODLE_BASE_URL')}/webservice/rest/server.php"
    
    # # Fetch user IDs for the provided email addresses
    # user_ids = [get_user_id_by_field(email, "email") for email in email_list]
    # if not user_ids:
    #     return {"success": False, "message": "No users found for the provided email addresses."}

    # # Prepare enrollment data
    # enrolments = [{'roleid': role_id, 'userid': user_id, 'courseid': course_id} for user_id in user_ids]

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
        return {"success": True, "message": "Users enrolled successfully."}
    except requests.exceptions.RequestException as e:
        return {"success": False, "message": f"Error enrolling users: {e}"}

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


def check_course_mails(course_id: int, page_mails: list):
    """
    Check the list of enrolled users in a Moodle course and compare it with a list of emails.
    Add or remove users based on the comparison.

    Args:
        course_id (int): The ID of the Moodle course.
        page_mails (list): A list of email addresses to compare with the enrolled users.

    Returns:
        tuple: A tuple containing lists of emails to be added and removed.
    """
    enrolled_users = get_enrolled_users_emails(course_id)
    
    if not enrolled_users:
        return None, None
    
    will_be_added = [mail for mail in page_mails if mail not in enrolled_users]
    will_be_removed = [mail for mail in enrolled_users if mail not in page_mails]
    
    return will_be_added, will_be_removed


