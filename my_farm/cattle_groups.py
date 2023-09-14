from my_farm.models import Cattle
from .report_calculations import GroupDataFilters
from .utils import calculate_age


class GroupsManagement:
    """
    Manages groups of cattle and performs calculations on the groups.
    """

    def __init__(self):
        """
        Initializes a GroupsManagement instance with an empty dictionary to store cattle groups.

        The 'groups' attribute is a dictionary where each key represents the name of a cattle group,
        and the corresponding value is a list of GroupDataFilters instances containing cattle data for that group.
        """
        self.groups: dict[str, list[GroupDataFilters]] = {}

    def calculate_groups(self, reference_date):
        """
        Calculates the groups of cattle based on the provided estimation date.

        :param reference_date: The reference date for the calculation.
        :return: A dictionary containing the calculated groups of cattle.
        """
        cattle_list = list(Cattle.objects.filter(deleted=False).values())

        groups = {
            'Cows': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] == 'Cow' and cattle['entry_date'] < reference_date
                )
            ],
            'Calves': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] in ['Heifer', 'Bull'] and
                    0 <= calculate_age(cattle['birth_date'], reference_date) < 12 and
                    cattle['entry_date'] < reference_date
                )
            ],
            'Young_Heifer': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] == 'Heifer' and
                    12 <= calculate_age(cattle['birth_date'], reference_date) < 24 and
                    cattle['entry_date'] < reference_date
                )
            ],
            'Adult_Heifer': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] == 'Heifer' and
                    calculate_age(cattle['birth_date'], reference_date) >= 24 and
                    cattle['entry_date'] < reference_date
                )
            ],
            'Young_Bull': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] == 'Bull' and
                    12 <= calculate_age(cattle['birth_date'], reference_date) < 24 and
                    cattle['entry_date'] < reference_date
                )
            ],
            'Adult_Bull': [
                cattle for cattle in cattle_list if (
                    cattle['gender'] == 'Bull' and
                    calculate_age(cattle['birth_date'], reference_date) >= 24 and
                    cattle['entry_date'] < reference_date
                )
            ],
        }
        return groups

    def add_group(self, group_name, reference_date):
        """
        Adds a group with the provided group name to the groups list based on the estimation date.

        :param group_name: The name of the group to add.
        :param reference_date: The reference date for the group calculation.
        """
        groups = self.calculate_groups(reference_date)
        group_data = groups.get(group_name, [])
        self.groups[group_name] = group_data


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
            if cattle_data['end_date'] is None:
                cattle = {
                    'id': cattle_data['id'],
                    'type': cattle_data['type'],
                    'number': cattle_data['number'],
                    'name': cattle_data['name'],
                    'gender': cattle_data['gender'],
                    'breed': cattle_data['breed'],
                    'birth_date': cattle_data['birth_date'],
                    'acquisition_method': cattle_data['acquisition_method'],
                    'entry_date': cattle_data['entry_date'],
                    'comments': cattle_data['comments'],
                }
                self.cattle_list.append(cattle)

    def count_active_cattle(self):
        """
        Counts the number of active cattle in the group.

        The active cattle are those whose 'end_date' is None in the group data.
        """
        self.active_cattle = sum(
            1 for cattle_data in self.group_data if cattle_data['end_date'] is None)

