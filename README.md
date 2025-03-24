# FlyRecordKeeper - Travel Agency RMS
*A Python desktop application for managing records for clients, airlines, and flights with JSON data persistence.*

## Table of Contents
1. Project Description
2. Technologies Used
3. Challenges and Future Features
4. Installation Guide
5. Usage
6. Tests
7. Licence

**1. Project Description**

The following repository is a Record Management System designed for a specialist travel agency to facilitate admin tasks associated with case management for three record types:
- Client
- Airlines
- Flights

The key features of the system are:
- It performs CRUD (Create, Read, Update, Delete) operations.
- It persist data using JSON storage for reliable data storage.
- It employ a simplified GUI interface built with Tkinter.

 **2. Technologies Used**

- **Python**: As the core programming language for building a scalable application.
- **JSON**: As confirmed for reliable and lightweight data storage, eliminating ddatabase dependency.
- **Tkinter**: As standard GUI package for creating a simplified desktop application to function across OS.
- **Pillow**: As displayed for digital image processing, more specifically the FlyRecordKeeper logo.
- **Calendar**: As displayed for date-time entry on Flight records for intuitive selection.
- **TimePicker**: As displayed for date-time entry on Flight records for intuitive selection.

 **3. Challenges & Future Improvements**

The challenges faced:
- To ensure a user-friendly GUI layout that would adapt to screen sizes (e.g. secondary windows).
- To create an intuitive option for date-time entry that meets both form and function.
- To add a vertical and horizontal scrollbar to improve UX design.

The improvements considered:
- To improve UX design by promoting controls where user can select preferences (e.g. hide of display).

 **4. Installation Guide**

These are the steps to set up locally:
1. Clone the repository:
   ```bash
   git clone <repository-url>
   ```
2. Navigate to the source directory:
   ```bash
   cd flyrecordkeeper/src
   ```
3. Create and activate a virtual environment:
   - **Windows**:
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     python -m venv venv
     source venv/bin/activate
     ```
4. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the application:
   ```bash
   python main.py
   ```
     
 **5. Usage**

 Open the application (main.py).
 
 Access the navigation menu for selected view:
   - **Manage Clients**: Add, update, delete or search & view client records.
   - **Manage Airlines**: Add, update, delete or search & view airline records.
   - **Manage Flights**: Add, update, delete or search & view flight records.

 **6. Test**
 
 The steps to run unit tests:
1. Ensure virtual environment is active.
2. Run the test suite stored in folder
   ```bash
   python -m unittest discover tests/
   ```
The example tests include: 

 **7. Licence**
 
Copyright 2025 kn-msccs-uol, ddaniels-uni-of-liv, CM434, and kevinechevarria21
   
Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0
 
