from flask import render_template, request, jsonify, Response, flash, redirect, url_for, session
from app import app
from database import db_manager, DatabaseManager
import logging

logger = logging.getLogger(__name__)

def get_current_db_manager():
    """Get the database manager for the current database selection"""
    db_choice = session.get('database_choice', 'external')  # Default to external for Vercel
    if db_choice == 'external':
        return DatabaseManager(app.config["EXTERNAL_DATABASE_URL"])
    else:
        # For Vercel deployment, use external DB if no Replit DB is available
        replit_url = app.config.get("REPLIT_DATABASE_URL")
        if replit_url:
            return DatabaseManager(replit_url)
        else:
            return DatabaseManager(app.config["EXTERNAL_DATABASE_URL"])

@app.route('/')
def index():
    """Main dashboard showing all tables"""
    current_db = get_current_db_manager()
    tables = current_db.get_tables()
    db_choice = session.get('database_choice', 'replit')
    
    if tables is None:
        flash('Failed to connect to database. Please check your connection.', 'error')
        tables = []
    
    return render_template('index.html', tables=tables, db_choice=db_choice)

@app.route('/switch_database', methods=['POST'])
def switch_database():
    """Switch between databases"""
    db_choice = request.form.get('database_choice', 'replit')
    session['database_choice'] = db_choice
    flash(f'Switched to {"External" if db_choice == "external" else "Replit"} database', 'info')
    return redirect(url_for('index'))

@app.route('/table/<table_name>')
def table_view(table_name):
    """View table data with pagination and filtering"""
    schema = request.args.get('schema', 'public')
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 50))
    order_by = request.args.get('order_by')
    order_dir = request.args.get('order_dir', 'ASC')
    search = request.args.get('search', '').strip()
    
    offset = (page - 1) * per_page
    current_db = get_current_db_manager()
    
    # Get table structure
    structure = current_db.get_table_structure(table_name, schema)
    if structure is None:
        flash(f'Failed to fetch table structure for {table_name}', 'error')
        return redirect(url_for('index'))
    
    # Get table data
    data, total_count = current_db.get_table_data(
        table_name, schema, per_page, offset, order_by, order_dir, search
    )
    
    if data is None:
        flash(f'Failed to fetch data from table {table_name}', 'error')
        data = []
        total_count = 0
    
    # Calculate pagination info
    total_pages = (total_count + per_page - 1) // per_page
    has_prev = page > 1
    has_next = page < total_pages
    
    return render_template('table_view.html',
                         table_name=table_name,
                         schema=schema,
                         structure=structure,
                         data=data,
                         page=page,
                         per_page=per_page,
                         total_count=total_count,
                         total_pages=total_pages,
                         has_prev=has_prev,
                         has_next=has_next,
                         order_by=order_by,
                         order_dir=order_dir,
                         search=search)

@app.route('/query')
def query_interface():
    """Custom SQL query interface"""
    return render_template('query.html')

@app.route('/execute_query', methods=['POST'])
def execute_query():
    """Execute custom SQL query"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({'success': False, 'error': 'Query cannot be empty'})
        
        current_db = get_current_db_manager()
        # Execute query
        result, error = current_db.execute_custom_query(query)
        
        if error:
            return jsonify({'success': False, 'error': error})
        
        # Convert result to serializable format
        if result:
            serialized_result = [dict(row) for row in result]
            if hasattr(result[0], 'keys'):
                columns = list(result[0].keys())
            else:
                columns = []
        else:
            serialized_result = []
            columns = []
        
        return jsonify({
            'success': True,
            'data': serialized_result,
            'columns': columns,
            'row_count': len(serialized_result)
        })
        
    except Exception as e:
        logger.error(f"Error executing query: {str(e)}")
        return jsonify({'success': False, 'error': str(e)})

@app.route('/export/<table_name>')
def export_table(table_name):
    """Export table data in various formats"""
    schema = request.args.get('schema', 'public')
    format_type = request.args.get('format', 'csv').lower()
    current_db = get_current_db_manager()
    
    try:
        if format_type == 'csv':
            data = current_db.export_table_csv(table_name, schema)
            if data is None:
                flash('Failed to export table data', 'error')
                return redirect(url_for('table_view', table_name=table_name, schema=schema))
            
            return Response(
                data,
                mimetype='text/csv',
                headers={'Content-Disposition': f'attachment; filename={table_name}.csv'}
            )
        
        elif format_type == 'json':
            data = current_db.export_table_json(table_name, schema)
            if data is None:
                flash('Failed to export table data', 'error')
                return redirect(url_for('table_view', table_name=table_name, schema=schema))
            
            return Response(
                data,
                mimetype='application/json',
                headers={'Content-Disposition': f'attachment; filename={table_name}.json'}
            )
        
        elif format_type == 'sql':
            data = current_db.export_table_sql(table_name, schema)
            if data is None:
                flash('Failed to export table data', 'error')
                return redirect(url_for('table_view', table_name=table_name, schema=schema))
            
            return Response(
                data,
                mimetype='text/sql',
                headers={'Content-Disposition': f'attachment; filename={table_name}.sql'}
            )
        
        else:
            flash('Invalid export format', 'error')
            return redirect(url_for('table_view', table_name=table_name, schema=schema))
            
    except Exception as e:
        logger.error(f"Error exporting table: {str(e)}")
        flash('Failed to export table data', 'error')
        return redirect(url_for('table_view', table_name=table_name, schema=schema))

@app.route('/api/tables')
def api_tables():
    """API endpoint to get list of tables"""
    current_db = get_current_db_manager()
    tables = current_db.get_tables()
    if tables is None:
        return jsonify({'success': False, 'error': 'Failed to fetch tables'})
    
    return jsonify({
        'success': True,
        'tables': [dict(table) for table in tables]
    })

@app.route('/api/table/<table_name>/structure')
def api_table_structure(table_name):
    """API endpoint to get table structure"""
    schema = request.args.get('schema', 'public')
    current_db = get_current_db_manager()
    structure = current_db.get_table_structure(table_name, schema)
    
    if structure is None:
        return jsonify({'success': False, 'error': 'Failed to fetch table structure'})
    
    return jsonify({
        'success': True,
        'structure': [dict(col) for col in structure]
    })

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('index.html', error='Page not found'), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('index.html', error='Internal server error'), 500
