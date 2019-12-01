from apis.models import Industry_locales, Country_locales


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


def getCompanyData(companies, lang):
    companies_data = []

    for company in companies:
        industryLocal = Industry_locales.objects.filter(language__startswith=lang, industry_id=company.industry.id).first()
        countryLocal = Country_locales.objects.filter(language__startswith=lang, country_id=company.country.id).first()

        company_data = {
            "id": company.id,
            "name": company.name,
            "active_employees": company.active_employees,
            "total_expenses": company.total_expenses,
            "manage": company.manage,
            "website": company.website,
            "employee_count_index": company.employee_count_index,
            "created_at": company.created_at,
            "industry_id": company.industry_id,
            "country_id": company.country_id,
            "user_id": company.user_id,
            "industry": {
                "id": company.industry.id,
                "name": industryLocal.name
            },
            "country": {
                "id": company.country.id,
                "name": countryLocal.name
            }
        }
        companies_data.append(company_data)

    return companies_data
