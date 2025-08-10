# PostgreSQL Database Dumper

## Overview

This is a Flask-based web application that provides a user-friendly interface for viewing and managing PostgreSQL databases. The application serves as a database administration tool, allowing users to browse tables, view data with pagination and filtering, execute custom SQL queries, and export data in various formats. It features a dark-themed Bootstrap UI with responsive design and real-time data interaction capabilities.

**Recent Changes (August 10, 2025):**
- Configured for Vercel deployment with serverless functions
- Added database switching between Replit and external PostgreSQL databases
- Created proper WSGI entry points and environment configuration
- Added comprehensive error handling and connection timeouts
- Prepared deployment-ready structure with proper static file handling

## User Preferences

Preferred communication style: Simple, everyday language.

## Deployment Configuration

### Vercel Deployment
- **Entry Point**: `api/index.py` (serverless function)
- **Static Files**: Properly routed through `/static/` path
- **Environment Variables**: `EXTERNAL_DATABASE_URL` required
- **Database**: Uses external PostgreSQL database (ReviewPilot production)
- **Python Version**: 3.11 (specified in runtime.txt)
- **Dependencies**: Defined in Pipfile and requirements_vercel.txt

## System Architecture

### Backend Architecture
- **Framework**: Flask web framework with modular route organization
- **Database Layer**: Custom DatabaseManager class using psycopg2 for PostgreSQL connectivity
- **Configuration**: Environment-based configuration with fallback defaults for development
- **Middleware**: ProxyFix for deployment compatibility and CORS enabled for API access

### Frontend Architecture
- **UI Framework**: Bootstrap 5 with dark theme and Font Awesome icons
- **JavaScript**: Vanilla JavaScript with jQuery for DataTables integration
- **Template Engine**: Jinja2 templates with modular layout structure
- **Interactive Features**: CodeMirror for SQL query editing and DataTables for enhanced table viewing

### Data Management
- **Database Connection**: Connection pooling with automatic reconnection handling
- **Query Processing**: Parameterized queries with pagination, sorting, and search capabilities
- **Data Export**: Multiple export formats (CSV, JSON) with streaming for large datasets
- **Error Handling**: Comprehensive logging and user-friendly error messages

### Security & Performance
- **Session Management**: Flask sessions with configurable secret keys
- **Input Validation**: SQL injection protection through parameterized queries
- **Performance**: Pagination and lazy loading for large datasets
- **Responsive Design**: Mobile-friendly interface with adaptive layouts

### Application Structure
- **Separation of Concerns**: Clear separation between routes, database logic, and presentation
- **Modular Design**: Reusable components for table viewing, query execution, and data export
- **Template Inheritance**: Base template structure for consistent UI across pages
- **Static Assets**: Organized CSS and JavaScript with custom styling overrides

## External Dependencies

### Database
- **PostgreSQL**: Primary database with configurable connection string
- **psycopg2**: Python PostgreSQL adapter with real dictionary cursor support

### Frontend Libraries
- **Bootstrap 5**: UI framework with dark theme variant
- **Font Awesome 6**: Icon library for enhanced visual elements
- **DataTables**: Advanced table functionality with sorting and filtering
- **CodeMirror**: Code editor for SQL query interface with syntax highlighting

### Python Packages
- **Flask**: Core web framework
- **Flask-CORS**: Cross-origin resource sharing support
- **pandas**: Data manipulation for export functionality
- **Werkzeug**: WSGI utilities and proxy handling

### Development Tools
- **Logging**: Built-in Python logging for debugging and monitoring
- **Environment Variables**: Configuration management for deployment flexibility