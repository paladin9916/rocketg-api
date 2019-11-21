

def getUserData(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id
        }
        users_data.append(user_data)

    return users_data