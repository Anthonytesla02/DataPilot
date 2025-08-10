# Deploy PostgreSQL Database Dumper to Render

## Quick Deployment Steps

### Option 1: Using render.yaml (Recommended)
1. **Fork or clone this repository** to your GitHub account
2. **Connect to Render**:
   - Go to [Render Dashboard](https://dashboard.render.com/)
   - Click "New" → "Blueprint"
   - Connect your GitHub repository
   - Select this repository
3. **Deploy**: Render will automatically read the `render.yaml` file and deploy your app

### Option 2: Manual Setup
1. **Create a new Web Service** on Render
2. **Connect your repository** 
3. **Configure the service**:
   - **Name**: `postgresql-database-dumper`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements_render.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT main:app`
   - **Plan**: Free (or upgrade as needed)

### Environment Variables
The app will automatically use the database connection defined in the `render.yaml` file. If you want to use a different database:

1. **Go to your service settings** in Render
2. **Add environment variable**:
   ```
   EXTERNAL_DATABASE_URL = your_postgresql_connection_string
   ```

## What Gets Deployed

- **Full Flask application** with PostgreSQL connectivity
- **Web interface** for database management
- **Table browser** with pagination and search
- **SQL query interface** with syntax highlighting  
- **Data export** in CSV, JSON, and SQL formats
- **Responsive design** that works on all devices

## Database Connection

The app connects to your PostgreSQL database using the connection string:
```
postgresql://reviewpilot_user:kLQiZvLx6Hk5sOw92HO5tt7Xa9oeUEL6@dpg-d27nseogjchc738fvaf0-a.oregon-postgres.render.com/reviewpilot
```

## After Deployment

1. **Access your app** at `https://your-app-name.onrender.com`
2. **Browse database tables** using the interface
3. **Run custom SQL queries** with the built-in editor
4. **Export data** in multiple formats

## Troubleshooting

- **If database connection fails**: Check that your PostgreSQL database allows external connections
- **If app doesn't start**: Check the build logs in Render dashboard
- **For slow cold starts**: Consider upgrading from the free plan

Your app will be production-ready and accessible worldwide once deployed!