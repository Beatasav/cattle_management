from .utils import calculate_age, estimate_cattle_weight
from .models import Cattle
from .report_calculations import GroupNumbers

class CattleGroupData:
    """
    Represents a group of cattle data with various properties and calculations.
    """

    def __init__(self, group_name, group_data):
        self.group_name = group_name
        self.group_data = group_data
        self.id = None
        self.type = None
        self.number = None
        self.name = None
        self.gender = None
        self.breed = None
        self.birth_date = None
        self.acquisition_method = None
        self.entry_date = None
        self.comments = None
        self.active_cattle = 0
        self.cattle_list = []

    def cattle_data(self):
        """
        Extracts the cattle data from the group data and assigns it to the instance properties.
        """
        for cattle_data in self.group_data:
            if cattle_data['cattle']['end_date'] is None:
                cattle = {
                    'id': cattle_data['cattle']['id'],
                    'type': cattle_data['cattle']['type'],
                    'number': cattle_data['cattle']['number'],
                    'name': cattle_data['cattle']['name'],
                    'gender': cattle_data['cattle']['gender'],
                    'breed': cattle_data['cattle']['breed'],
                    'birth_date': cattle_data['cattle']['birth_date'],
                    'acquisition_method': cattle_data['cattle']['acquisition_method'],
                    'entry_date': cattle_data['cattle']['entry_date'],
                    'comments': cattle_data['cattle']['comments'],
                }
                self.cattle_list.append(cattle)

    def count_active_cattle(self):
        """
        Counts the number of active cattle in the group.

        The active cattle are those whose 'end_date' is None in the group data.
        """
        self.active_cattle = sum(
            1 for cattle_data in self.group_data if cattle_data['cattle']['end_date'] is None)


class GroupsManagement:
    """
    Manages groups of cattle and performs calculations on the groups.
    """

    def __init__(self):
        """
        Initializes a GroupsManagement instance with an empty list of groups.
        """
        self.groups: list[GroupNumbers] = []

    def calculate_groups(self, estimation_date):
        """
        Calculates the groups of cattle based on the provided estimation date.

        :param estimation_date: The estimation date for the calculation.
        :return: A dictionary containing the calculated groups of cattle.
        """
        cattle_list = list(Cattle.objects.filter(deleted=False).values())
        groups = {
            'Cows': [{'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'], estimation_date), 2)}
                     for cattle in cattle_list if cattle['gender'] == 'Cow'
                     and cattle['entry_date'] < estimation_date],

            'Calves': [{'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'],
                                                                                      estimation_date), 2)} for cattle
                       in cattle_list if cattle['gender'] in ['Heifer', 'Bull']
                       and 0 <= calculate_age(cattle['birth_date'], estimation_date) < 12
                       and cattle['entry_date'] < estimation_date],

            'Young_Heifer': [
                {'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'], estimation_date), 2)}
                for cattle in cattle_list if cattle['gender'] == 'Heifer'
                and 12 <= calculate_age(cattle['birth_date'], estimation_date) < 24
                and cattle['entry_date'] < estimation_date],

            'Adult_Heifer': [
                {'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'], estimation_date), 2)}
                for cattle in cattle_list if cattle['gender'] == 'Heifer'
                and calculate_age(cattle['birth_date'], estimation_date) >= 24
                and cattle['entry_date'] < estimation_date],

            'Young_Bull': [
                {'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'], estimation_date), 2)}
                for cattle in cattle_list if cattle['gender'] == 'Bull'
                and 12 <= calculate_age(cattle['birth_date'], estimation_date) < 24
                and cattle['entry_date'] < estimation_date],

            'Adult_Bull': [
                {'cattle': cattle, 'weight': round(estimate_cattle_weight(cattle['id'], estimation_date), 2)}
                for cattle in cattle_list if cattle['gender'] == 'Bull'
                and calculate_age(cattle['birth_date'], estimation_date) >= 24
                and cattle['entry_date'] < estimation_date],
        }
        return groups

    def add_group(self, group_name, estimation_date):
        """
        Adds a group with the provided group name to the groups list based on the estimation date.

        :param group_name: The name of the group to add.
        :param estimation_date: The estimation date for the group calculation.
        """
        groups = self.calculate_groups(estimation_date)
        group_data = groups.get(group_name, {})
        self.groups[group_name] = group_data

