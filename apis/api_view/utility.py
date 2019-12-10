from apis.models import Industry_locales, Country_locales, Images
from apis.serializers import ImageSerializer


def getIndustryData(industryList):
    industries_data = []

    for industry in industryList:
        industry_data = {
            "id": industry.industry_id,
            "name": industry.name,
        }
        industries_data.append(industry_data)

    return industries_data


def getCountryData(countryList):
    countries_data = []

    for country in countryList:
        country_data = {
            "id": country.country_id,
            "name": country.name,
        }
        countries_data.append(country_data)

    return countries_data


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
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency,
        }
        users_data.append(user_data)

    return users_data


def getUserDataWithPW(users):
    users_data = []

    for user in users:
        user_data = {
            "id": user.id,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "password": user.reset_password_token,
            "phone": user.phone,
            "job_title": user.job_title,
            "department": user.department,
            "language": user.language,
            "role_id": user.role_id,
            "avatar_url": user.avatar,
            "company_id": user.company_id,
            "reimbursement_cycle": user.reimbursement_cycle,
            "payments_currency": user.payments_currency,
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


def uploadImage(userId, imageInfo):
    try:
        image = Images.objects.get(user_id=userId)
        image_serializer = ImageSerializer(image, data=imageInfo)
    except Images.DoesNotExist:
        image_serializer = ImageSerializer(data=imageInfo)

    if image_serializer.is_valid():
        image_serializer.save()

    return image_serializer
