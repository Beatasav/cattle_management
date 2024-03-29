from datetime import date, datetime
from django.shortcuts import render, redirect
from django.views import View
from .cattle_groups import GroupsManagement
from .report_calculations import AcquisitionLossCalculator, MovementCalculator, GroupNumbers


class GenerateReportView(View):
    """
    A view class for generating a report.

    Inherits from View.

    Attributes:
        generate_report_template (str): The template for rendering the generate report page.

    Methods:
        __init__(): Initializes the class and sets initial values.
        get(request): Handles the GET request for displaying the generate report page.
        post(request): Handles the POST request for generating a report.
    """

    generate_report_template = 'my_farm/generate_report.html'

    def __init__(self):
        """
        Initializes the GenerateReportView class.
        Sets initial values for start_date and end_date attributes.
        Calls the __init__ method of the super class.
        """
        super().__init__()
        self.start_date = None
        self.end_date = None

    def get(self, request):
        """
        Handles the GET request for displaying the generate report page.

        :param: request (HttpRequest): The HTTP request object.
        :return: HttpResponse: The rendered HTTP response for the generate report page.
        """
        return render(request, self.generate_report_template)

    def post(self, request):
        """
        Handles the POST request for generating a report.

        :param: request (HttpRequest): The HTTP request object.
        :return:HttpResponse: The redirect HTTP response to the report page.
        """
        start_date = datetime.fromisoformat(request.POST.get('start_date')).date()
        end_date = datetime.fromisoformat(request.POST.get('end_date')).date()

        # Store the data in session
        request.session['report_data'] = {
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
        }

        return redirect('my_farm:report')


class LivestockMovementReportView(GroupsManagement, GenerateReportView, View):
    """
    A view class for generating and displaying the livestock movement report.

    Inherits from GroupsManagement, GenerateReportView, and View.

    Attributes:
        report_template (str): The template for rendering the report.

    Methods:
        __init__(): Initializes the class and sets initial values.
        load_report_data(request): Loads the report data from the session.
        get(request): Handles the GET request for generating and displaying the report.
    """

    report_template = 'my_farm/livestock_movement_report.html'

    def __init__(self):
        """
        Initializes the LivestockMovementReportView class.

        Calls the __init__ methods of the super classes and sets initial values for groups and encoder_class attributes.
        """
        super(GroupsManagement, self).__init__()
        super(GenerateReportView, self).__init__()
        super(View, self).__init__()
        self.groups = []

    def load_report_data(self, request):
        """
        Loads the report data from the session.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            bool: True if the report data is loaded successfully, False otherwise.
        """
        report_data = request.session.get('report_data')
        if not report_data:
            return False

        self.start_date = date.fromisoformat(report_data['start_date'])
        self.end_date = date.fromisoformat(report_data['end_date'])

        return True

    def get(self, request):
        """
        Handles the GET request for generating and displaying the livestock movement report.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            HttpResponse: The rendered HTTP response with the generated report.
        """
        # Check if report data can be loaded, or redirect if not
        if not self.load_report_data(request):
            return redirect('my_farm:generate_report')

        # Initialize the GroupsManagement instance
        groups_manager = GroupsManagement()

        # Calculate groups data for estimation, start date, and end date
        estimation_date = groups_manager.calculate_groups(reference_date=self.end_date)
        start_date_groups = groups_manager.calculate_groups(reference_date=self.start_date)
        end_date_groups = groups_manager.calculate_groups(reference_date=self.end_date)

        # Initialize the groups list to store group statistics
        self.groups = []

        for group_name, cattle_data in estimation_date.items():
            # Create a GroupNumbers instance and calculate statistics
            group = GroupNumbers(group_name, cattle_data)
            group.calculate_start_date_stats(start_date_groups, self.start_date)
            group.calculate_end_date_stats(end_date_groups, self.end_date)
            group.calculate_difference()

            # Create an instance of AcquisitionLossCalculator and calculate acquisition and loss statistics
            acquisition_loss_calculator = AcquisitionLossCalculator(group_name, cattle_data)
            acquisition_loss_calculator.calculate_acquisition(self.start_date, self.end_date)
            acquisition_loss_calculator.calculate_loss(self.start_date, self.end_date)

            # Assign acquisition and loss statistics to the group
            group.acquisition_stats = acquisition_loss_calculator

            # Create an instance of MovementCalculator and calculate movement statistics
            movement_calculator = MovementCalculator(group_name, cattle_data)
            movement_calculator.calculate_movement_in_and_out(start_date_groups, self.start_date, end_date_groups,
                                                              self.end_date)

            # Assign movement statistics to the group
            group.movement_stats = movement_calculator

            # Add the group to the list of groups
            self.groups.append(group)

        # Prepare context for rendering the report template
        context = {
            'start_date': self.start_date.isoformat(),
            'end_date': self.end_date.isoformat(),
            'groups': self.groups,
        }

        # Render the report template and return the HTTP response
        return render(request, self.report_template, context)