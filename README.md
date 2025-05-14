# Cancer Risk Predictor

A professional web application that predicts cancer risk based on various health parameters using machine learning. Built with Flask, MongoDB, and scikit-learn.

## Features

- User authentication and authorization
- Real-time risk prediction using machine learning
- Historical record tracking
- Responsive and modern UI
- Secure data handling
- Interactive form inputs
- Record management capabilities

## Project Structure

```
├── model/                      # Machine Learning Model Files
│   ├── columns.json           # Feature columns configuration
│   ├── log_model.pkl          # Trained logistic regression model
│   └── notebook.ipynb         # Model training and development notebook
│
├── server/                    # Backend Server
│   ├── artifacts/            # Model artifacts for production
│   │   ├── columns.json     # Production feature columns
│   │   └── log_model.pkl    # Production model
│   │
│   ├── client/              # Frontend Assets
│   │   ├── static/         # Static files
│   │   │   ├── app.css    # Application styles
│   │   │   ├── app.js     # Client-side JavaScript
│   │   │   └── bg.svg     # Background image
│   │   │
│   │   └── templates/      # HTML Templates
│   │       ├── apology.html    # Error page template
│   │       ├── app.html        # Main application template
│   │       ├── history.html    # History view template
│   │       ├── login.html      # Login page template
│   │       ├── register.html   # Registration page template
│   │       └── risk.html       # Risk result template
│   │
│   ├── __pycache__/           # Python cache directory
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── init_db.py            # Database initialization script
│   ├── requirements.txt      # Python dependencies
│   ├── util.py              # Utility functions
│   └── vercel.json          # Vercel deployment configuration
```

## Key Components

### Backend (Flask)

- **app.py**: Main application file containing routes and core logic
- **config.py**: Configuration settings including MongoDB connection
- **util.py**: Utility functions for model prediction and error handling
- **init_db.py**: Database initialization and counter setup

### Frontend

- **templates/**: HTML templates using Jinja2

  - Modern, responsive design
  - Consistent styling across pages
  - Interactive form elements
  - User-friendly navigation

- **static/**: Frontend assets
  - **app.css**: Custom styling with modern design principles
  - **app.js**: Client-side interactivity and form handling

### Machine Learning

- **model/notebook.ipynb**: Complete model development process
- **model/log_model.pkl**: Serialized logistic regression model
- **model/columns.json**: Feature configuration for predictions

## Technical Details

### Dependencies

- Flask: Web framework
- MongoDB: Database backend
- scikit-learn: Machine learning functionality
- onnxruntime: Model optimization and inference
- Werkzeug: Security and utilities
- Bootstrap: Frontend styling
- jQuery: Frontend interactivity

### Security Features

- Password hashing using Werkzeug
- Session-based authentication
- CSRF protection
- Secure MongoDB connection
- Input validation and sanitization

### Database Schema

- **users**: User authentication data
- **risk_records**: Risk assessment history
- **counters**: Auto-incrementing record IDs

## Deployment

The application is configured for deployment on Vercel with Python runtime support. The `vercel.json` file contains the necessary build and route configurations.

## Development Setup

1. Create a .env file in server directory and add your MONGO_URI there: 

```bash
MONGO_URI="your_mongodb_uri_here"
```

2. Install Python dependencies:

```bash
cd server
pip install -r requirements.txt
```

3. Initialize the database: (in server directory)

```bash
python init_db.py
```

4. Start the development server: (in server directory)

```bash
flask run
```

5. Enjoy!

## Usage

1. Register a new account or login
2. Fill in the health assessment form
3. Submit to receive risk prediction
4. View history of predictions
5. Manage saved records

## Machine Learning Model

The cancer risk prediction model uses logistic regression trained on various health parameters:

- Age
- Sex
- BMI (calculated from height and weight)
- Alcohol consumption
- Smoking status
- Genetic risk
- Physical activity
- Diabetes status
- Hypertension status

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request
