# PostgreSQL Database Dumper

A Flask-based web application for exploring, managing, and exporting PostgreSQL database contents with a user-friendly interface.

## Features

- **Database Connection Switching**: Switch between multiple PostgreSQL databases
- **Table Explorer**: Browse all tables with comprehensive metadata
- **Data Viewer**: View table data with pagination, sorting, and search
- **Custom SQL Queries**: Execute custom SQL with syntax highlighting
- **Data Export**: Export data in CSV, JSON, and SQL formats
- **Responsive Design**: Dark-themed Bootstrap UI that works on all devices

## Deployment

### Vercel Deployment

This application is configured for easy deployment on Vercel:

1. **Fork or clone this repository**

2. **Set up environment variables** in your Vercel dashboard:
   ```
   EXTERNAL_DATABASE_URL=your_postgresql_connection_string
   ```

3. **Deploy to Vercel**:
   - Connect your GitHub repository to Vercel
   - The app will automatically deploy using the `vercel.json` configuration

4. **Database Connection**:
   - The app will automatically use your external database when deployed on Vercel
   - You can switch between databases using the interface (if multiple are configured)

### Local Development

1. **Install dependencies**:
   ```bash
   pip install flask flask-cors psycopg2-binary pandas werkzeug
   ```

2. **Set environment variables**:
   ```bash
   export DATABASE_URL="your_postgresql_connection_string"
   export EXTERNAL_DATABASE_URL="your_external_postgresql_connection_string"
   ```

3. **Run the application**:
   ```bash
   python main.py
   ```

4. **Access the application**:
   Open http://localhost:5000 in your browser

## Architecture

- **Backend**: Flask web framework with modular architecture
- **Database**: PostgreSQL with psycopg2 adapter
- **Frontend**: Bootstrap 5 with dark theme, Font Awesome icons
- **Deployment**: Serverless functions compatible (Vercel)

## File Structure

```
├── api/                    # Vercel serverless functions
│   ├── __init__.py
│   └── index.py           # Main entry point for Vercel
├── static/                # Static assets
│   ├── css/
│   │   └── custom.css    # Custom styles
│   └── js/
│       └── app.js        # Client-side JavaScript
├── templates/             # Jinja2 templates
│   ├── index.html        # Main dashboard
│   ├── table_view.html   # Table data viewer
│   └── query.html        # SQL query interface
├── app.py                # Flask application setup
├── database.py           # Database management layer
├── routes.py             # Application routes
├── main.py               # Application entry point
├── vercel.json           # Vercel deployment configuration
└── README.md             # This file
```

## Security

- Parameterized queries prevent SQL injection
- Read-only operations by default
- Connection timeout limits
- Environment-based configuration

## Browser Support

- Chrome/Chromium 90+
- Firefox 88+
- Safari 14+
- Edge 90+

## License

This project is open source and available under the MIT License.