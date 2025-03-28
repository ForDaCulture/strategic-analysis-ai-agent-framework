import os
import json
import re
import pandas as pd
import tempfile
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from werkzeug.utils import secure_filename

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'json', 'csv', 'xlsx', 'xls'}
DEFAULT_BPM_FILE = 'bpm_principles.json'

# Initialize Flask app
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size
app.secret_key = 'bpm_principles_explorer_secret_key'  # For session and flash messages

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Helper function to check if file extension is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Helper function to validate JSON file
def is_valid_json(file_path):
    try:
        with open(file_path, 'r') as f:
            json.load(f)
        return True
    except json.JSONDecodeError:
        return False
    except Exception:
        return False

# Helper function to convert CSV to JSON
def convert_csv_to_json(file_path):
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Check if the CSV has the expected structure
        # This is a simplified check - you might need more sophisticated validation
        if df.empty:
            return None
        
        # Convert to JSON structure
        # This is a simplified conversion - adjust based on your expected structure
        result = {}
        
        # Try to detect if the CSV has a specific structure
        if 'name' in df.columns and 'description' in df.columns:
            # Looks like a list of items with name and description
            category_name = os.path.splitext(os.path.basename(file_path))[0]
            result[category_name] = df.to_dict(orient='records')
        else:
            # Generic approach: group by first column
            if len(df.columns) >= 2:
                group_col = df.columns[0]
                for group, group_df in df.groupby(group_col):
                    result[group] = group_df.drop(columns=[group_col]).to_dict(orient='records')
            else:
                # Fallback for simple lists
                result['items'] = df.to_dict(orient='records')
        
        return result
    except Exception as e:
        print(f"Error converting CSV to JSON: {str(e)}")
        return None

# Helper function to convert Excel to JSON
def convert_excel_to_json(file_path):
    try:
        # Read all sheets from Excel file
        excel_data = pd.read_excel(file_path, sheet_name=None)
        
        # Convert each sheet to a section in the JSON
        result = {}
        for sheet_name, df in excel_data.items():
            if df.empty:
                continue
                
            # Convert sheet to list of records
            result[sheet_name] = df.to_dict(orient='records')
        
        return result
    except Exception as e:
        print(f"Error converting Excel to JSON: {str(e)}")
        return None

# Helper function to process uploaded file and convert to JSON if needed
def process_uploaded_file(file_path):
    file_ext = os.path.splitext(file_path)[1].lower()
    
    if file_ext == '.json':
        # Validate JSON
        if is_valid_json(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return None
    elif file_ext == '.csv':
        # Convert CSV to JSON
        return convert_csv_to_json(file_path)
    elif file_ext in ['.xlsx', '.xls']:
        # Convert Excel to JSON
        return convert_excel_to_json(file_path)
    else:
        return None

# Helper function to save processed data as JSON
def save_as_json(data, original_filename):
    try:
        # Create a JSON filename based on the original filename
        base_name = os.path.splitext(original_filename)[0]
        json_filename = f"{base_name}.json"
        json_path = os.path.join(app.config['UPLOAD_FOLDER'], json_filename)
        
        # Save the data as JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        
        return json_filename
    except Exception as e:
        print(f"Error saving JSON: {str(e)}")
        return None

# Helper function to load JSON data
def load_json_data(filename):
    if filename == DEFAULT_BPM_FILE:
        file_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', filename)
    else:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        flash(f"Error loading file: {str(e)}", "error")
        return None

# Helper function to get list of uploaded files
def get_uploaded_files():
    files = []
    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if allowed_file(filename):
            files.append(filename)
    return sorted(files)

# Helper function to search in JSON data
def search_in_json(data, search_term, query_type='all'):
    results = {}
    search_term = search_term.lower()
    
    # Define sections to search based on query_type
    if query_type == 'all':
        sections = [
            'core_principles', 'methodologies', 'frameworks', 'maturity_models',
            'performance_metrics', 'implementation_best_practices', 
            'common_challenges', 'technology_enablers'
        ]
    else:
        sections = [query_type]
    
    # Search in each section
    for section in sections:
        if section in data:
            section_results = []
            
            # Handle different data structures
            if section == 'performance_metrics':
                # Performance metrics have categories
                for category in data[section]:
                    for metric in category['metrics']:
                        if search_in_item(metric, search_term):
                            # Include category information
                            metric_copy = metric.copy()
                            metric_copy['category'] = category['category']
                            section_results.append(metric_copy)
            else:
                # Other sections have direct lists
                for item in data[section]:
                    if search_in_item(item, search_term):
                        section_results.append(item)
            
            # Add results to the output if any found
            if section_results:
                results[section] = section_results
    
    return results

# Helper function to search within an item
def search_in_item(item, search_term):
    # Convert item to string for simple search
    item_str = json.dumps(item).lower()
    return search_term in item_str

# Routes
@app.route('/')
def index():
    # Get active file from session or use default
    active_file = session.get('active_file', DEFAULT_BPM_FILE)
    
    # Load data from active file
    data = load_json_data(active_file)
    
    # If data loading failed, use default file
    if data is None:
        active_file = DEFAULT_BPM_FILE
        data = load_json_data(active_file)
        session['active_file'] = active_file
    
    # Get list of uploaded files
    uploaded_files = get_uploaded_files()
    
    return render_template('index.html', 
                          data=data, 
                          active_file=active_file, 
                          uploaded_files=uploaded_files)

@app.route('/view/<filename>')
def view_file(filename):
    # Validate filename
    if filename != DEFAULT_BPM_FILE and filename not in get_uploaded_files():
        flash(f"File {filename} not found.", "error")
        return redirect(url_for('index'))
    
    # Set active file in session
    session['active_file'] = filename
    
    return redirect(url_for('index'))

@app.route('/upload', methods=['POST'])
def upload_file():
    # Check if file part exists in request
    if 'file' not in request.files:
        flash('No file part', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    
    # Check if file is selected
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if file has allowed extension
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        # Save file
        file.save(file_path)
        
        # Process file based on its type
        file_ext = os.path.splitext(filename)[1].lower()
        
        if file_ext == '.json':
            # Validate JSON
            if not is_valid_json(file_path):
                os.remove(file_path)
                flash('Invalid JSON file', 'error')
                return redirect(url_for('index'))
            
            # Set as active file
            session['active_file'] = filename
            flash(f'JSON file {filename} uploaded successfully', 'success')
        
        elif file_ext in ['.csv', '.xlsx', '.xls']:
            # Process CSV or Excel file
            processed_data = process_uploaded_file(file_path)
            
            if processed_data is None:
                os.remove(file_path)
                flash(f'Invalid {file_ext[1:].upper()} file or conversion failed', 'error')
                return redirect(url_for('index'))
            
            # Save processed data as JSON
            json_filename = save_as_json(processed_data, filename)
            
            if json_filename is None:
                os.remove(file_path)
                flash('Failed to save processed data', 'error')
                return redirect(url_for('index'))
            
            # Set the JSON file as active
            session['active_file'] = json_filename
            flash(f'{file_ext[1:].upper()} file {filename} converted and uploaded successfully as {json_filename}', 'success')
    else:
        allowed_ext_str = ', '.join(ALLOWED_EXTENSIONS)
        flash(f'Only {allowed_ext_str.upper()} files are allowed', 'error')
    
    return redirect(url_for('index'))

@app.route('/upload-batch', methods=['POST'])
def upload_batch():
    # Check if files part exists in request
    if 'files' not in request.files:
        flash('No files part', 'error')
        return redirect(url_for('index'))
    
    files = request.files.getlist('files')
    
    # Check if files are selected
    if len(files) == 0 or all(file.filename == '' for file in files):
        flash('No files selected', 'error')
        return redirect(url_for('index'))
    
    # Process each file
    success_count = 0
    last_valid_file = None
    
    for file in files:
        if file.filename == '':
            continue
        
        if allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            
            # Save file
            file.save(file_path)
            
            # Process file based on its type
            file_ext = os.path.splitext(filename)[1].lower()
            
            if file_ext == '.json':
                # Validate JSON
                if is_valid_json(file_path):
                    success_count += 1
                    last_valid_file = filename
                else:
                    os.remove(file_path)
                    flash(f'File {filename} is not a valid JSON file', 'warning')
            
            elif file_ext in ['.csv', '.xlsx', '.xls']:
                # Process CSV or Excel file
                processed_data = process_uploaded_file(file_path)
                
                if processed_data is not None:
                    # Save processed data as JSON
                    json_filename = save_as_json(processed_data, filename)
                    
                    if json_filename is not None:
                        success_count += 1
                        last_valid_file = json_filename
                        flash(f'{file_ext[1:].upper()} file {filename} converted to {json_filename}', 'info')
                    else:
                        os.remove(file_path)
                        flash(f'Failed to save processed data from {filename}', 'warning')
                else:
                    os.remove(file_path)
                    flash(f'Failed to process {filename}', 'warning')
        else:
            allowed_ext_str = ', '.join(ALLOWED_EXTENSIONS)
            flash(f'File {file.filename} is not allowed (only {allowed_ext_str.upper()} files are accepted)', 'warning')
    
    # Set last valid file as active if any
    if last_valid_file:
        session['active_file'] = last_valid_file
    
    # Show summary message
    if success_count > 0:
        flash(f'Successfully processed {success_count} file(s)', 'success')
    else:
        flash('No valid files were processed', 'error')
    
    return redirect(url_for('index'))

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    # Prevent deletion of default file
    if filename == DEFAULT_BPM_FILE:
        flash('Cannot delete the default file', 'error')
        return redirect(url_for('index'))
    
    # Check if file exists
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(file_path):
        flash(f'File {filename} not found', 'error')
        return redirect(url_for('index'))
    
    # Delete file
    try:
        os.remove(file_path)
        flash(f'File {filename} deleted successfully', 'success')
        
        # If active file was deleted, switch to default
        if session.get('active_file') == filename:
            session['active_file'] = DEFAULT_BPM_FILE
    except Exception as e:
        flash(f'Error deleting file: {str(e)}', 'error')
    
    return redirect(url_for('index'))

@app.route('/query', methods=['POST'])
def query():
    # Get query parameters
    search_term = request.form.get('search_term', '').strip()
    query_type = request.form.get('query_type', 'all')
    
    # Validate search term
    if not search_term:
        return jsonify({})
    
    # Get active file
    active_file = session.get('active_file', DEFAULT_BPM_FILE)
    
    # Load data
    data = load_json_data(active_file)
    if data is None:
        return jsonify({})
    
    # Perform search
    results = search_in_json(data, search_term, query_type)
    
    return jsonify(results)

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html', error='Page not found'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('error.html', error='Server error'), 500

# Run the app
if __name__ == '__main__':
    app.run(debug=True)