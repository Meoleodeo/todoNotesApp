# Todo & Notes Manager

A desktop application for managing todos and notes using Python, PyQt6, and SQL Server.

## Features

- **Todo Management**
  - Add, edit, and delete todos
  - Add optional links to todos
  - Click to open associated links
  - Chronological ordering

- **Notes Management**
  - Add, edit, and delete notes
  - Pin important notes to top
  - Full text content support
  - Chronological ordering

- **User Interface**
  - Modern, clean design
  - Tabbed interface
  - Always-on-top option
  - Teal color theme with opacity support

## Prerequisites

1. **Python 3.7+**
2. **SQL Server**
   - SQL Server 2019 or later
   - SQL Server Authentication enabled
   - TCP/IP protocol enabled

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Meoleodeo/todoNotesApp
   cd todoNotesApp
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up SQL Server**
   - Install SQL Server if not already installed
   - Enable SQL Server Authentication
   - Enable TCP/IP protocol in SQL Server Configuration Manager
   - Run the SQL setup script:
     ```bash
     sqlcmd -S localhost -i sql/setup_server.sql
     ```

## Configuration

The application uses the following default SQL Server connection settings:
- Server: localhost
- Database: TodoNotesDB
- Username: sa
- Password: 1234567

To modify these settings, update the connection string in `database.py`.

## Running the Application

```bash
python main.py
```
## Build the Application

```bash
python build_exe.py
```

## Project Structure

```
todo-notes-manager/
├── main.py              # Main application and GUI
├── database.py          # Database operations
├── requirements.txt     # Python dependencies
├── sql/
│   └── setup_server.sql # SQL Server setup script
└── README.md           # Documentation
```

## Security Note

The default credentials are for development purposes only. In a production environment:
- Use a strong password
- Create a dedicated database user with minimal permissions
- Store credentials securely
- Enable SQL Server security features

## Troubleshooting

1. **Connection Error**
   - Verify SQL Server is running
   - Check SQL Server Configuration Manager settings
   - Ensure SQL Server Authentication is enabled
   - Verify credentials in connection string

2. **Missing Dependencies**
   - Run `pip install -r requirements.txt`
   - Ensure SQL Server ODBC drivers are installed

3. **Permission Issues**
   - Check SQL Server user permissions
   - Verify database exists and is accessible
   - Check Windows firewall settings