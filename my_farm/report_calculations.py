from .utils import estimate_cattle_weight

class GroupNumbers:
    """
    Represents a group of numbers with various calculations and data.
    """

    def __init__(self, group_name, group_data):
        """
        Initializes a GroupNumbers instance with the provided group name and group data.

        :param group_name: The name of the group.
        :param group_data: The data associated with the group.
        """
        self.filter_acquisition_loss_dates = None
        self.filter_loss_dates = None
        self.filter_acquisition_dates = None
        self.group_name = group_name
        self.group_data = group_data
        self.start_date_count = 0
        self.end_date_count = 0
        self.count_difference = 0
        self.start_date_group_weight = 0
        self.end_date_group_weight = 0
        self.weight_difference = 0
        self.birth_count = 0
        self.birth_weight = 0
        self.purchase_count = 0
        self.purchase_weight = 0
        self.gift_count = 0
        self.gift_weight = 0
        self.death_count = 0
        self.death_weight = 0
        self.sold_count = 0
        self.sold_weight = 0
        self.consumed_count = 0
        self.consumed_weight = 0
        self.gifted_count = 0
        self.gifted_weight = 0
        self.moved_in = 0
        self.moved_out = 0
        self.weight_moved_in = 0
        self.weight_moved_out = 0

    def __repr__(self):
        """
        Returns a string representation of the GroupNumbers instance.

        :return: The string representation of the instance.
        """
        return self.group_name

    def quantity(self, start_date_groups, end_date_groups, start_date, end_date):
        """

        Calculates the quantity and weight of cattle for the group based on the provided start and end date groups,
        and reports the differences in both quantity and weight between the defined dates.

        :param start_date: The start date for the period of calculation.
        :param end_date: The end d
        ate for the period of calculation.
        :param start_date_groups: A dictionary containing the group data organized by group name for the start date.
        :param end_date_groups: A dictionary containing the group data organized by group name for the end date.

        """
        start_date_list = start_date_groups.get(self.group_name, [])
        end_date_list = end_date_groups.get(self.group_name, [])

        start_date_filtered = [cattle for cattle in start_date_list if (cattle['cattle']['end_date'] is None or
                                                                        start_date < cattle['cattle']['end_date'])]

        end_date_filtered = [cattle for cattle in end_date_list if (cattle['cattle']['end_date'] is None or
                                                                    end_date <= cattle['cattle']['end_date'])]

        self.start_date_count = len(start_date_filtered)
        self.end_date_count = len(end_date_filtered)

        self.count_difference = self.end_date_count - self.start_date_count

        self.start_date_group_weight = round(sum(cattle_dict['weight'] for cattle_dict in start_date_filtered))
        self.end_date_group_weight = round(sum(cattle_dict['weight'] for cattle_dict in end_date_filtered))

        self.weight_difference = round((self.end_date_group_weight - self.start_date_group_weight))

    def check_acquisition(self, start_date, end_date):
        """
        Calculates the acquisition statistics of the group based on the provided start and end dates.

        The weight in the acquisition column will be estimated based on the acquisition date for the acquisition
        methods.

        :param start_date: The start date for the acquisition calculation.
        :param end_date: The end date for the acquisition calculation.
        """

        self.filter_acquisition_dates = [
            cattle for cattle in self.group_data
            if
            ('entry_date' in cattle['cattle'] and cattle['cattle']['entry_date'] is not None and start_date <=
                cattle['cattle']['entry_date'] < end_date)

        ]

        for item in self.filter_acquisition_dates:
            cattle = item['cattle']

            if 'acquisition_method' in cattle and cattle['entry_date'] >= start_date:
                entry_weight = round(estimate_cattle_weight(cattle['id'], cattle['entry_date']))

                if cattle['acquisition_method'] == 'Birth':
                    self.birth_count += 1
                    self.birth_weight += entry_weight
                elif cattle['acquisition_method'] == 'Purchase':
                    self.purchase_count += 1
                    self.purchase_weight += entry_weight
                elif cattle['acquisition_method'] == 'Gift':
                    self.gift_count += 1
                    self.gift_weight += entry_weight

    def check_loss(self, start_date, end_date):
        """
        Calculates loss statistics of the group based on the provided start and end dates.

        The weight in the loss column will be estimated based the end date for the loss methods.

        :param start_date: The start date for the loss calculation.
        :param end_date: The end date for the loss calculation.
        """

        self.filter_loss_dates = [
            cattle for cattle in self.group_data
            if ('end_date' in cattle['cattle'] and cattle['cattle']['end_date'] is not None
                and start_date < cattle['cattle']['end_date'] <= end_date)
        ]

        for item in self.filter_loss_dates:
            cattle = item['cattle']

            if 'loss_method' in cattle:
                end_weight = round(estimate_cattle_weight(
                    cattle['id'], cattle['end_date'])) if cattle['end_date'] is not None else 0

                if cattle['loss_method'] == 'Death':
                    self.death_count += 1
                    self.death_weight += end_weight
                elif cattle['loss_method'] == 'Sold':
                    self.sold_count += 1
                    self.sold_weight += end_weight
                elif cattle['loss_method'] == 'Consumed':
                    self.consumed_count += 1
                    self.consumed_weight += end_weight
                elif cattle['loss_method'] == 'Gifted':
                    self.gifted_count += 1
                    self.gifted_weight += end_weight

    def check_movement(self, start_date_groups, end_date_groups, start_date, end_date):
        """
        Checks the movement of the group by comparing the start and end date groups.

        :param start_date_groups: The dictionary of start date groups.
        :param end_date_groups: The dictionary of end date groups.
        :param start_date: The start date for the period of calculation.
        :param end_date: The end date for the period of calculation.
        """

        self.filter_acquisition_loss_dates = self.filter_acquisition_dates.copy()
        self.filter_acquisition_loss_dates.extend(self.filter_loss_dates)

        start_date_list = start_date_groups.get(self.group_name, [])
        end_date_list = end_date_groups.get(self.group_name, [])

        moved_out = [item for item in start_date_list if
                     item['cattle']['id'] not in [cattle['cattle']['id'] for cattle in end_date_list]
                     and item not in self.filter_acquisition_loss_dates]

        moved_in = [item for item in end_date_list if
                    item['cattle']['id'] not in [cattle['cattle']['id'] for cattle in start_date_list]
                    and item not in self.filter_acquisition_loss_dates]

        for item in self.filter_acquisition_loss_dates:
            cattle = item['cattle']
            if cattle['end_date'] is not None and cattle['entry_date'] <= start_date \
                    and cattle['id'] not in [cattle['cattle']['id'] for cattle in start_date_list] \
                    and cattle['end_date'] <= end_date:
                end_weight = round(estimate_cattle_weight(cattle['id'], cattle['end_date']))

                if item not in start_date_list:
                    moved_in.append({'cattle': cattle, 'weight': end_weight})

            if cattle['entry_date'] >= start_date \
                    and cattle['id'] not in [cattle['cattle']['id'] for cattle in end_date_list] \
                    and 'loss_method' not in cattle:
                entry_weight = round(estimate_cattle_weight(cattle['id'], cattle['entry_date']))

                if item not in start_date_list:
                    moved_out.append({'cattle': cattle, 'weight': entry_weight})

        self.moved_in = len(moved_in)
        self.moved_out = len(moved_out)

        self.weight_moved_in = round(sum(item.get('weight', 0) for item in moved_in))
        self.weight_moved_out = round(sum(item.get('weight', 0) for item in moved_out))