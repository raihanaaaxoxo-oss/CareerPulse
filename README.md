# CareerPulse

CareerPulse is a web-based job application tracking system built with Flask, MySQL, HTML, CSS and JavaScript.

The application allows users to create an account, securely log in, record job applications, search their applications, update application statuses and view application statistics from a dashboard.

---

## Features

### User Authentication

- User registration
- Secure password hashing using Werkzeug
- User login and logout
- Session-based authentication
- Protected application routes
- Duplicate email prevention

### Application Tracking

Users can record:

- Company name
- Role title
- Application date
- Application status

Available application statuses:

- Applied
- Screening
- Interviewing
- Offer
- Rejected

### Application Management

Users can:

- View their applications
- Add new applications
- Search applications by company or role
- Update application status without refreshing the page
- Delete applications

### Dashboard

The dashboard displays:

- Total applications
- Interview rate
- Total offers

Dashboard metrics are retrieved through the CareerPulse API.

### API

CareerPulse provides API endpoints for:

- Updating application status
- Retrieving dashboard metrics

See [API.md](API.md) for complete API documentation.

---

## Technologies Used

### Backend

- Python
- Flask
- PyMySQL
- Werkzeug
- python-dotenv

### Frontend

- HTML5
- CSS3
- JavaScript
- Jinja2 templates
- Fetch API

### Database

- MySQL

---

## Project Structure

```text
CareerPulse/
│
├── static/
│   ├── css/
│   │   └── main.css
│   │
│   └── javascript/
│       └── main.js
│
├── templates/
│   ├── add_applications.html
│   ├── applications.html
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   └── register.html
│
├── .env
├── .gitignore
├── API.md
├── app.py
├── db.py
├── README.md
├── requirements.txt
└── schema.sql
```

---

## Database Structure

CareerPulse uses a MySQL database called `careerpulse_db`.

The database contains two main tables: `users` and `applications`.

### users

Stores registered CareerPulse users.

| Column | Description |
|---|---|
| `id` | Unique user ID |
| `email` | User email address |
| `password_hash` | Securely hashed password |
| `created_at` | Account creation timestamp |

### applications

Stores job applications belonging to users.

| Column | Description |
|---|---|
| `id` | Unique application ID |
| `user_id` | ID of the user associated with the application |
| `company` | Company name |
| `role_title` | Position applied for |
| `status` | Current application status |
| `applied_date` | Date the application was submitted |
| `created_at` | Application creation timestamp |

The relationship between the tables is:

```text
users
  │
  │ 1
  │
  │ many
  ▼
applications
```

Each application is associated with a user through the `user_id` foreign key.

The database uses `ON DELETE CASCADE`, meaning applications belonging to a deleted user are automatically removed.

---

## Application Statuses

CareerPulse supports five application statuses:

```text
Applied
Screening
Interviewing
Offer
Rejected
```

The status can be changed directly from the Applications page.

---

## Installation

### 1. Clone the Repository

```bash
git clone <your-repository-url>
```

Navigate into the project:

```bash
cd CareerPulse
```

### 2. Create a Virtual Environment

On Windows:

```powershell
python -m venv .venv
```

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

### 3. Install Dependencies

Install the required Python packages:

```powershell
pip install -r requirements.txt
```

---

## Database Setup

Open MySQL and run the SQL contained in:

```text
schema.sql
```

This creates the:

```text
careerpulse_db
```

database along with the required:

- `users` table
- `applications` table
- Foreign key relationship

---

## Environment Configuration

CareerPulse uses environment variables to keep sensitive configuration out of the source code.

Create a file called:

```text
.env
```

in the project root.

Add:

```text
SECRET_KEY=your-secret-key

DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your-mysql-password
DB_NAME=careerpulse_db
```

Replace the placeholder values with your own local configuration.

### Important

The `.env` file contains sensitive information and must not be committed to Git.

It is excluded through `.gitignore`.

---

## Running the Application

Activate the virtual environment:

```powershell
.venv\Scripts\activate
```

Start the Flask application:

```powershell
python app.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

---

## Using CareerPulse

### 1. Register

Navigate to:

```text
/register
```

Create an account using an email address and password.

Passwords are hashed before being stored in the database.

### 2. Login

Navigate to:

```text
/login
```

Enter your registered email and password.

Successful authentication creates a user session.

### 3. Dashboard

After logging in, the dashboard displays:

- Total applications
- Interview rate
- Total offers

### 4. Add an Application

Navigate to:

```text
/applications/new
```

Enter:

- Company
- Role
- Application date

The application is associated with the currently logged-in user.

### 5. View Applications

Navigate to:

```text
/applications
```

The Applications page displays the user's job applications.

### 6. Search Applications

Use the search field on the Applications page to search by:

- Company
- Role title

### 7. Update Application Status

Use the status dropdown beside an application.

The status is updated asynchronously using JavaScript and the CareerPulse API without requiring a page refresh.

### 8. Delete an Application

Applications can be deleted from the Applications page.

### 9. Logout

Logging out ends the current user session and prevents access to protected application routes.

---

## Authentication and Security

CareerPulse uses several security measures:

- Passwords are hashed using Werkzeug
- Passwords are never stored as plain text
- User sessions are used to authenticate protected routes
- Database credentials are stored in environment variables
- Flask's secret key is stored in the `.env` file
- `.env` is excluded from version control
- User emails are unique in the database
- SQL queries use parameterized values
- Application records are associated with authenticated users

---

## API

CareerPulse currently provides the following API endpoints.

### Update Application Status

```text
PATCH /api/applications/<id>/status
```

Updates the status of an application.

### Dashboard Metrics

```text
GET /api/metrics
```

Returns:

- Total applications
- Interview rate
- Total offers

For complete request and response documentation, see:

[API Documentation](API.md)

---

## Error Handling

The application handles common errors including:

- Invalid login credentials
- Duplicate email registration
- Invalid application statuses
- Invalid API responses
- Failed API requests
- Database errors
- Unauthorized access to protected routes

Frontend API requests also check HTTP response status codes and handle network or response errors.

---

## Development

CareerPulse was developed as a Flask-based full-stack application using a relational MySQL database.

### Backend

The backend handles:

- Routing
- Authentication
- Database operations
- Application management
- API endpoints

### Frontend

The frontend handles:

- User forms
- Application tables
- Status controls
- Dashboard display
- Asynchronous API requests

---

## Files

### `app.py`

Contains the Flask application, routes, authentication logic, application management and API endpoints.

### `db.py`

Contains the MySQL database connection function.

### `schema.sql`

Contains the SQL required to create the CareerPulse database and tables.

### `main.js`

Handles frontend JavaScript functionality including:

- Application status updates
- Dashboard metric retrieval
- API error handling

### `main.css`

Contains the application's frontend styling.

### `API.md`

Contains detailed documentation for the CareerPulse API.

### `requirements.txt`

Contains the Python dependencies required to run the application.

---

## License

This project was created for educational and development purposes.