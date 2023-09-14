from dateutil.relativedelta import relativedelta


def calculate_age(birth_date, estimation_date):
    """
    Calculates the age in months based on the birthdate and estimation date.

    :param birth_date: The birthdate.
    :param estimation_date: The estimation date for the calculation.
    :return: The age in months.
    """
    if estimation_date < birth_date:
        return -1
    else:
        age = relativedelta(estimation_date, birth_date)
        age_in_months = age.years * 12 + age.months
        return age_in_months

