from utils.email_util import send_email

def send_user_registration_email(to_email: str, emp_id: str, password: str):
    subject = "Welcome to the Company"
    body = (
        f"Dear User, \n\n"
        f"Your account has been successfully created.\n\n"
        f"Employee ID: {emp_id} \n\n"
        f"Temporary Password: {password}\n\n"
        f"Please Log in and change your password at your earliest convenience. \n\n"
        f"Best Regard, \nCompany Team"
    ) 
    send_email(to_email=to_email, subject=subject, body=body)