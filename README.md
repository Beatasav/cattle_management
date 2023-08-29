# My Cattle 🐮 - Cattle Management Web Application

My Cattle is a web application designed to assist cattle farmers in managing their cattle, herds, and fields. 
The application offers a centralized platform for recording and accessing essential information about livestock and fields, as well as generating livestock movement reports. 

This README provides an overview of the application's features, including its installation process, deployment information, and guidelines for effective usage of both the live version and locally installed versions.

## 💡 Features

- **Cattle Management**: Record and manage individual cattle details, including number, name, gender, breed, acquisition, birth and entry dates, loss methods, and more. Allocate cattle to existing herds and update entries seamlessly for accurate management.

- **Herd Management**: Organize cattle into herds. Keep track of important herd details like location, start date, end date, leader, and status. Easily assign one or more cattle to a herd, select existing fields for their location, and update entries seamlessly for precise management.

- **Field Management**: Record details about fields where herds are located. Add information such as field size, location, coordinates, and any specific conditions relevant to the field. Also, assign herds to particular field.

- **Group Management**: Categorize cattle into age groups to simplify livestock oversight and reporting.

- **Dashboard**: Displays the count of cattle within each age group currently present on the farm and provides access to all cattle within their respective groups.

- **Efficient Search**: Quick access to information about cattle, herds, and fields through search functionality. 

- **Livestock Movement Report**: Generate detailed reports to track changes in livestock across different age groups. Monitor weight fluctuations, observe acquisition and loss events within selected time periods. 

- **User Authentication**: Secure access to the application with user authentication.

## 🌐 Deployment

Explore the live version of the application online. Please consider limitations:

- **Access URL**: https://mycattle.azurewebsites.net/
- **Limitations**: The deployment is hosted on a free Microsoft Azure account, which might result in a slightly longer initial loading process when accessed for the first time.
- **User Access**: To browse, please log in:
  - Username: 'guest'
  - Password: 'gu94estuzo85'

## 💾 Installation

1. Clone original project repository without deployment settings for local development and testing:
 `[https://github.comJeskevicRasa/my_cattle](https://github.com/JeskevicRasa/my_cattle)'
3. Install dependencies: `pip install -r requirements.txt`
4. Set up the database - note that this is running on SQLite by default, you will have to download and install it: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Start the development server: `python manage.py runserver`
 
## 🏃‍♀️ Usage

To use the application, follow these steps based on your preferred version:

### Deployed Version:

1. **Access the Application**: Visit the provided deployment URL: https://mycattle.azurewebsites.net/.
2. **Log in**: Use the following credentials:
   - Username: 'guest'
   - Password: 'gu94estuzo85'
3. **Explore Cattle Information**: On the main page's dashboard, access cattle details by age group, active herds, and fields.
4. **Manage Data**: Use the navigation panel to access all recorded fields, herds, and cattle. From there, execute management actions like adding new items or updating existing data.
5. **Generate Reports**: Create livestock movement reports to monitor changes in livestock across different age groups during selected time periods.

### Local Installation:

1. **Access the Application**: Open your web browser and navigate to `http://localhost:8000`.
2. **Login or Create an Account**: Log in using your superuser account or create a new account.
3. **Manage Data**: Use the navigation panel to access the interfaces for managing fields, herds, and cattle. Input relevant data for each section.
4. **Explore Cattle Information**: After inputting data, go to the main dashboard and access cattle details by age group, active herds, and fields.
5. **Generate Reports**: Create livestock movement reports to monitor changes in livestock across different age groups during selected time periods.

## 👨‍💻 Authors

This project was created as the final project for the CodeAcademy Python Programming course, collaboratively by:

- [Beata Savkaitė](https://github.com/Beatasav)
- [Rasa Jeskevič](https://github.com/JeskevicRasa)

The original version of the project that we worked on together without deployment settings is here: https://github.com/JeskevicRasa/my_cattle


Happy cattle management! 🐮
