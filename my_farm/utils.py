from .constants import FEMALE_BIRTH_WEIGHT, MALE_BIRTH_WEIGHT, FEMALE_MAX_WEIGHT, MALE_MAX_WEIGHT, DAILY_WEIGHT_GAIN
from dateutil.relativedelta import relativedelta
from .models import Cattle


def calculate_age(birth_date, estimation_date):
    """
    Calculates the age in months based on the birthdate and estimation date.

    :param birth_date: The birthdate of the cattle.
    :param estimation_date: The estimation date for the calculation.
    :return: The age in months.
    """
    if estimation_date < birth_date:
        return -1
    else:
        age = relativedelta(estimation_date, birth_date)
        age_in_months = age.years * 12 + age.months
        return age_in_months


def estimate_cattle_weight(cattle_id, estimation_date):
    """
    Estimates the weight of cattle based on its ID and the estimation date.

    :param cattle_id: The ID of the cattle.
    :param estimation_date: The estimation date for the weight calculation.
    :return: The estimated weight of the cattle.
    """
    cattle = Cattle.objects.get(id=cattle_id)
    birth_date = cattle.birth_date

    days_passed = (estimation_date - birth_date).days if estimation_date > birth_date else 0

    gender = cattle.gender

    if gender in ['Heifer', 'Cow']:
        weight = FEMALE_BIRTH_WEIGHT + (days_passed * DAILY_WEIGHT_GAIN)
        weight = min(weight, FEMALE_MAX_WEIGHT)
    elif gender == 'Bull':
        weight = MALE_BIRTH_WEIGHT + (days_passed * DAILY_WEIGHT_GAIN)
        weight = min(weight, MALE_MAX_WEIGHT)
    else:
        raise ValueError("Invalid gender. Must be 'Heifer', 'Cow', or 'Bull'.")

    return weight
