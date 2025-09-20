from django.http import JsonResponse

import re


def create_response(status, message, result=None):

    response_data = {
        "status_code" : status,
        "message": message, 
    }

    if result is not None:
        response_data["result"] = result

    return JsonResponse(response_data, safe=False)

def validate_fields(fields):
    errors = {}

    for field_name, details in fields.items():
        value = details.get('value')
        check_type = details.get('checks', [])

        if 'mobile' in check_type:
            if not re.fullmatch(r'\d{10}', value):
                errors[field_name] = "Mobile number must be exactly 10 digits."
        
        elif 'country_code' in check_type:
            if not re.fullmatch(r'\+\d{1,4}', value):
                errors[field_name] = "Country code must start with '+' followed by 1 to 4 digits."

        elif 'username' in check_type:
            if not re.fullmatch(r'[A-Za-z0-9_]{3,30}', value):
                errors[field_name] = "Username must be alphanumeric (including underscores), 3 to 30 characters long."

        elif 'full_name' in check_type:
            if not re.fullmatch(r"[A-Za-z]+([ '-][A-Za-z]+)*", value.strip()):
                    errors[field_name] = "Full name must contain only letters, spaces, hyphens or apostrophes."
            elif len(value.strip()) > 100:
                errors[field_name] = "Full name must be 100 characters or fewer."

        elif 'email' in check_type:
            email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            if not re.match(email_regex, value):
                errors[field_name] = "Invalid email format"

        elif 'password' in check_type:
            if len(value) < 8:
                errors[field_name] = "Password must be at least 8 characters long."
            elif not re.search(r'[A-Z]', value):
                errors[field_name] = "Password must contain at least one uppercase letter."
            elif not re.search(r'[a-z]', value):
                errors[field_name] = "Password must contain at least one lowercase letter."
            elif not re.search(r'\d', value):
                errors[field_name] = "Password must contain at least one digit."
            elif not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
                errors[field_name] = "Password must contain at least one special character (!@#$%^&*(),.?\":{}|<>)."

        else:
            errors[field_name] = f"Unknown validation type: {check_type}"

    if errors:
        return errors
    # return True, "Validated Successfully"

