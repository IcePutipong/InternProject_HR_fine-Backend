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

def send_reset_password_email(to_email: str, new_password: str):
    """
    Sends an email when a user resets their password.
    """
    subject = "Your Password Has Been Reset"
    body = (
        f"Dear User,\n\n"
        f"Your password has been successfully reset.\n\n"
        f"Your new temporary password: {new_password}\n\n"
        f"Please log in and change your password immediately to ensure account security.\n\n"
        f"If you did not request this change, please contact support immediately.\n\n"
        f"Best Regards,\nCompany Team"
    ) 

    send_email(to_email=to_email, subject=subject, body=body)