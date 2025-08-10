import psycopg2
import psycopg2.extras
import pandas as pd
import json
import csv
import io
from urllib.parse import urlparse
from app import app
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.connection = None
        self.database_url = app.config["DATABASE_URL"]
        
    def connect(self):
        """Establish database connection"""
        try:
            if self.connection is None or self.connection.closed:
                self.connection = psycopg2.connect(
                    self.database_url,
                    cursor_factory=psycopg2.extras.RealDictCursor
                )
            return True
        except Exception as e:
            logger.error(f"Database connection failed: {str(e)}")
            return False
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and not self.connection.closed:
            self.connection.close()
    
    def get_tables(self):
        """Get list of all tables in the database"""
        try:
            if not self.connect():
                return None
                
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT table_name, table_schema
                FROM information_schema.tables 
                WHERE table_schema NOT IN ('information_schema', 'pg_catalog')
                ORDER BY table_schema, table_name
            """)
            tables = cursor.fetchall()
            cursor.close()
            return tables
        except Exception as e:
            logger.error(f"Error fetching tables: {str(e)}")
            return None
    
    def get_table_structure(self, table_name, schema='public'):
        """Get structure information for a specific table"""
        try:
            if not self.connect():
                return None
                
            cursor = self.connection.cursor()
            cursor.execute("""
                SELECT 
                    column_name,
                    data_type,
                    is_nullable,
                    column_default,
                    character_maximum_length
                FROM information_schema.columns 
                WHERE table_name = %s AND table_schema = %s
                ORDER BY ordinal_position
            """, (table_name, schema))
            columns = cursor.fetchall()
            cursor.close()
            return columns
        except Exception as e:
            logger.error(f"Error fetching table structure: {str(e)}")
            return None
    
    def get_table_data(self, table_name, schema='public', limit=100, offset=0, order_by=None, order_dir='ASC', search=None):
        """Get data from a specific table with pagination and filtering"""
        try:
            if not self.connect():
                return None, 0
                
            cursor = self.connection.cursor()
            
            # Build base query
            base_query = f'FROM "{schema}"."{table_name}"'
            where_clause = ""
            params = []
            
            # Add search functionality
            if search:
                # Get column names for search
                columns = self.get_table_structure(table_name, schema)
                if columns:
                    search_conditions = []
                    for col in columns:
                        search_conditions.append(f'"{col["column_name"]}"::text ILIKE %s')
                        params.append(f'%{search}%')
                    where_clause = f" WHERE ({' OR '.join(search_conditions)})"
            
            # Count total records
            count_query = f"SELECT COUNT(*) {base_query}{where_clause}"
            cursor.execute(count_query, params)
            total_count = cursor.fetchone()[0]
            
            # Build main query with ordering and pagination
            order_clause = ""
            if order_by:
                order_clause = f' ORDER BY "{order_by}" {order_dir}'
            
            query = f'SELECT * {base_query}{where_clause}{order_clause} LIMIT %s OFFSET %s'
            params.extend([limit, offset])
            
            cursor.execute(query, params)
            data = cursor.fetchall()
            cursor.close()
            
            return data, total_count
        except Exception as e:
            logger.error(f"Error fetching table data: {str(e)}")
            return None, 0
    
    def execute_custom_query(self, query, limit=1000):
        """Execute a custom SQL query"""
        try:
            if not self.connect():
                return None, "Database connection failed"
                
            cursor = self.connection.cursor()
            
            # Add limit to SELECT queries if not already present
            query_stripped = query.strip().upper()
            if query_stripped.startswith('SELECT') and 'LIMIT' not in query_stripped:
                query += f' LIMIT {limit}'
            
            cursor.execute(query)
            
            if cursor.description:  # Query returns results
                data = cursor.fetchall()
                cursor.close()
                return data, None
            else:  # Query doesn't return results (INSERT, UPDATE, DELETE, etc.)
                self.connection.commit()
                cursor.close()
                return [], None
                
        except Exception as e:
            logger.error(f"Error executing custom query: {str(e)}")
            return None, str(e)
    
    def export_table_csv(self, table_name, schema='public'):
        """Export table data as CSV"""
        try:
            data, _ = self.get_table_data(table_name, schema, limit=10000)
            if data is None:
                return None
                
            # Convert to pandas DataFrame
            df = pd.DataFrame(data)
            
            # Create CSV string
            output = io.StringIO()
            df.to_csv(output, index=False)
            return output.getvalue()
            
        except Exception as e:
            logger.error(f"Error exporting CSV: {str(e)}")
            return None
    
    def export_table_json(self, table_name, schema='public'):
        """Export table data as JSON"""
        try:
            data, _ = self.get_table_data(table_name, schema, limit=10000)
            if data is None:
                return None
                
            # Convert RealDictRow to regular dict for JSON serialization
            json_data = [dict(row) for row in data]
            return json.dumps(json_data, indent=2, default=str)
            
        except Exception as e:
            logger.error(f"Error exporting JSON: {str(e)}")
            return None
    
    def export_table_sql(self, table_name, schema='public'):
        """Export table data as SQL INSERT statements"""
        try:
            data, _ = self.get_table_data(table_name, schema, limit=10000)
            if data is None:
                return None
                
            if not data:
                return f"-- No data found in table {schema}.{table_name}\n"
                
            # Get column names
            columns = list(data[0].keys())
            column_list = ', '.join([f'"{col}"' for col in columns])
            
            sql_statements = []
            sql_statements.append(f"-- Data export for table {schema}.{table_name}")
            sql_statements.append(f"-- Generated on {pd.Timestamp.now()}")
            sql_statements.append("")
            
            for row in data:
                values = []
                for col in columns:
                    value = row[col]
                    if value is None:
                        values.append('NULL')
                    elif isinstance(value, str):
                        values.append(f"'{value.replace(chr(39), chr(39)+chr(39))}'")  # Escape single quotes
                    else:
                        values.append(str(value))
                
                values_list = ', '.join(values)
                sql_statements.append(f'INSERT INTO "{schema}"."{table_name}" ({column_list}) VALUES ({values_list});')
            
            return '\n'.join(sql_statements)
            
        except Exception as e:
            logger.error(f"Error exporting SQL: {str(e)}")
            return None

# Global database manager instance
db_manager = DatabaseManager()
