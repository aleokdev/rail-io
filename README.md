# Mechelen Train Station Kiosk

A minimal, dark-themed web application that displays real-time train departure information for Mechelen station in Belgium. Designed for kiosk displays with no interactive elements.

## Features

- 🚂 Real-time train departure information from iRail API
- 🕐 Shows departure times, train numbers, destinations, and platforms
- ⏱️ Displays delays and cancellations
- 🌙 Dark theme optimized for kiosk displays
- 📱 Responsive design that works on various screen sizes
- 🔄 Auto-refresh every 60 seconds
- 🚫 No interactive elements (perfect for kiosks)

## Setup

### Prerequisites

- Python 3.7 or higher
- Internet connection for API access

### Installation

1. Clone or download this repository
2. Navigate to the project directory
3. Create a virtual environment (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### Option 1: Using the startup script (Recommended)
```bash
./start.sh
```

#### Option 2: Manual setup
1. Start the Flask development server:
   ```bash
   python app.py
   ```
2. Open your web browser and go to `http://localhost:5000`
3. For kiosk mode, use full-screen mode (F11 in most browsers)

#### Option 3: Using Docker
1. Build the Docker image:
   ```bash
   docker build -t mechelen-train-kiosk .
   ```
2. Run the container:
   ```bash
   docker run -p 5000:5000 mechelen-train-kiosk
   ```
3. Open your web browser and go to `http://localhost:5000`

### For Production Deployment

For production use, consider using a proper WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## API Usage

The application uses the iRail API (https://api.irail.be/) to fetch real-time train data for Mechelen station. The API is free and doesn't require authentication, but please respect their rate limits (3 requests per second).

## Configuration

You can modify the following variables in `app.py`:

- `MECHELEN_STATION`: Change to a different station name
- `USER_AGENT`: Update with your application information
- Auto-refresh interval: Modify the JavaScript timeout in the template (currently 60 seconds)

## API Endpoints

- `/` - Main kiosk display page
- `/api/departures` - JSON API endpoint for departure data

## Screen Optimization

The interface is optimized for:
- Large displays (1920x1080 and above)
- Landscape orientation
- 24/7 operation
- No user interaction required

## License

This project is open source. Please respect the iRail API terms of service when using this application.

## Support

For issues related to train data, please check the iRail API status at https://status.irail.be/

For application issues, please check the console output for error messages.
