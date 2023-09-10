class GroupDataFilters:
    def __init__(self, group_name, group_data):
        """
        Constructor for the GroupDataFilters class.

        :param group_name: The name of the cattle group.
        :param group_data: A list of dictionaries where each dictionary represents data about an individual cattle in the group.
        """
        self.group_name = group_name
        self.group_data = group_data

    def filter_active_cattle_data_by_date(self, cattle_data_by_date, reference_date):
        """
        Filter active cattle data for a specific date.

        :param cattle_data_by_date: A dictionary of cattle data grouped by a specific date (e.g., entry or end date).
        :param reference_date: The reference date for filtering active cattle data.
        :return: A list where each item is a dictionary representing data about individual cattle in the group.
        """
        group_data_by_date = cattle_data_by_date.get(self.group_name, [])
        active_cattle_data = [cattle for cattle in group_data_by_date if cattle['end_date'] is None
                              or reference_date < cattle['end_date']]
        return active_cattle_data

    def get_active_cattle_data_at_start_date(self, cattle_data_by_start_date, start_date):
        """
        Get active cattle data for a specified start date.

        :param cattle_data_by_start_date: A dictionary of cattle data grouped by the start date.
        :param start_date: The start date for filtering active cattle data.
        :return: A list of active cattle data dictionaries for the specified start date.
        """
        return self.filter_active_cattle_data_by_date(cattle_data_by_start_date, start_date)

    def get_active_cattle_data_at_end_date(self, cattle_data_by_end_date, end_date):
        """
        Get active cattle data for a specified end date.

        :param cattle_data_by_end_date: A dictionary of cattle data grouped by the end date.
        :param end_date: The end date for filtering active cattle data.
        :return: A list of active cattle data dictionaries for the specified end date.
        """
        return self.filter_active_cattle_data_by_date(cattle_data_by_end_date, end_date)

    def filter_cattle_data_by_entry_date_range(self, start_date, end_date):
        """
        Filter cattle data based on entry dates within a date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        :return: A list of cattle data dictionaries with entry dates within the specified range.
        """
        filtered_data_entry_date = [cattle for cattle in self.group_data if
                                    'entry_date' in cattle and cattle['entry_date']
                                    is not None and start_date <= cattle['entry_date'] < end_date]
        return filtered_data_entry_date

    def filter_cattle_data_by_end_date_range(self, start_date, end_date):
        """
        Filter cattle data based on end dates within a date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        :return: A list of cattle data dictionaries with end dates within the specified range.
        """
        filtered_data_end_date = [cattle for cattle in self.group_data if
                                  'end_date' in cattle and cattle['end_date']
                                  is not None and start_date <= cattle['end_date'] < end_date]
        return filtered_data_end_date


class GroupNumbers(GroupDataFilters):
    def __init__(self, group_name, group_data):
        super().__init__(group_name, group_data)
        self.start_date_count = 0
        self.end_date_count = 0
        self.count_difference = 0

    def calculate_start_date_stats(self, start_date_groups, start_date):
        self.start_date_count = len(self.get_active_cattle_data_at_start_date(start_date_groups, start_date))

    def calculate_end_date_stats(self, end_date_groups, end_date):
        self.end_date_count = len(self.get_active_cattle_data_at_end_date(end_date_groups, end_date))

    def calculate_difference(self):
        self.count_difference = self.end_date_count - self.start_date_count


class AcquisitionLossCalculator(GroupDataFilters):
    def __init__(self, group_name, group_data):
        """
        Constructor for the AcquisitionLossCalculator class.

        :param group_name: The name of the cattle group.
        :param group_data: A list of dictionaries containing cattle data for the group.
        """
        super().__init__(group_name, group_data)
        self.birth_count = 0
        self.purchase_count = 0
        self.gift_count = 0
        self.death_count = 0
        self.sold_count = 0
        self.consumed_count = 0
        self.gifted_count = 0

    def calculate_acquisition(self, start_date, end_date):
        """
        Calculate acquisition counts for cattle within a specified date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        """
        filtered_acquisition_data = self.filter_cattle_data_by_entry_date_range(start_date, end_date)

        for cattle in filtered_acquisition_data:
            acquisition_method = cattle.get('acquisition_method', '')
            if acquisition_method == 'Birth':
                self.birth_count += 1
            elif acquisition_method == 'Purchase':
                self.purchase_count += 1
            elif acquisition_method == 'Gift':
                self.gift_count += 1

    def calculate_loss(self, start_date, end_date):
        """
        Calculate loss counts for cattle within a specified date range.

        :param start_date: The start date of the date range.
        :param end_date: The end date of the date range.
        """
        filtered_loss_data = self.filter_cattle_data_by_end_date_range(start_date, end_date)

        for cattle in filtered_loss_data:
            loss_method = cattle.get('loss_method', '')
            if loss_method == 'Death':
                self.death_count += 1
            elif loss_method == 'Sold':
                self.sold_count += 1
            elif loss_method == 'Consumed':
                self.consumed_count += 1
            elif loss_method == 'Gifted':
                self.gifted_count += 1


class MovementCalculator(GroupDataFilters):
    def __init__(self, group_name, group_data):
        """
        Constructor for the MovementCalculator class.

        :param group_name: The name of the cattle group.
        :param group_data: A list of dictionaries containing cattle data for the group.
        """
        super().__init__(group_name, group_data)

        self.moved_in = 0
        self.moved_out = 0

    def get_cattle_moved_between_groups(self, data_from, start_date, data_to, end_date):
        """
        Calculate cattle that have moved between groups within a specified date range.

        :param data_from: Cattle data at the start of the date range.
        :param start_date: The start date of the date range.
        :param data_to: Cattle data at the end of the date range.
        :param end_date: The end date of the date range.
        :return: List of cattle that have moved between groups.
        """
        acquisition_loss_data = self.filter_cattle_data_by_entry_date_range(start_date, end_date).copy()
        acquisition_loss_data.extend(self.filter_cattle_data_by_end_date_range(start_date, end_date))

        moved_cattle = [cattle for cattle in data_from if
                        cattle not in data_to and cattle not in acquisition_loss_data]

        return moved_cattle

    def calculate_movement_in_and_out(self, start_date_groups, start_date, end_date_groups, end_date):
        """
        Calculate the number of cattle that moved into and out of the group within a specified date range.

        :param start_date_groups: Cattle data at the start of the date range grouped by some criteria.
        :param start_date: The start date of the date range.
        :param end_date_groups: Cattle data at the end of the date range grouped by the same criteria as start_date_groups.
        :param end_date: The end date of the date range.
        """
        start_date_data = self.get_active_cattle_data_at_start_date(start_date_groups, start_date)
        end_date_data = self.get_active_cattle_data_at_end_date(end_date_groups, end_date)

        moved_in_cattle = self.get_cattle_moved_between_groups(end_date_data, start_date, start_date_data, end_date)
        self.moved_in = len(moved_in_cattle)

        moved_out_cattle = self.get_cattle_moved_between_groups(start_date_data, start_date, end_date_data, end_date)
        self.moved_out = len(moved_out_cattle)