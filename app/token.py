from itsdangerous import URLSafeTimedSerializer


def generate_token(email):
    serializer = URLSafeTimedSerializer("x0Ak1SguEk")
    return serializer.dumps(email, salt="fkslkfsdlkfnsdfnsfd")


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer("x0Ak1SguEk")
    try:
        email = serializer.loads(token, salt="fkslkfsdlkfnsdfnsfd", max_age=expiration)
        return email
    except Exception:
        return False
