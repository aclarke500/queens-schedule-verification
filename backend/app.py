from flask import Flask, request, jsonify
from flask_cors import CORS
from ocr import extract_text_from_image
from agent import get_courses_from_ocr
from analyze_courses import check_cs_courses
import os

app = Flask(__name__)
# Configure CORS with more explicit settings
CORS(app, resources={r"/*": {
    "origins": ["http://localhost:5173", "http://127.0.0.1:5173", "https://queens-schedule-analyzer.netlify.app"],
    "methods": ["GET", "POST", "OPTIONS"],
    "allow_headers": ["Content-Type", "Authorization"]
}})

@app.route('/api/upload', methods=['POST'])
def upload_file():
    """
    Endpoint for uploading files, processing them with OCR, and extracting course information.
    
    Expects:
        - A file uploaded with key 'file1' (required)
        - An optional file uploaded with key 'file2'
    
    Returns:
        - JSON object with extracted course information from both files combined
    """
    # Check if at least one file was uploaded
    if 'file1' not in request.files:
        return jsonify({'error': 'First file (file1) is required'}), 400
    
    file1 = request.files['file1']
    
    # Check if first file is empty
    if file1.filename == '':
        return jsonify({'error': 'No file selected for first upload'}), 400
    
    try:
        # Process the first file with OCR
        text1 = extract_text_from_image(file1)
        
        # Extract course information from first file
        courses1 = get_courses_from_ocr(text1)
        
        # Initialize combined courses list with the first file's results
        all_courses = courses1
        
        # Check if a second file was uploaded
        if 'file2' in request.files:
            file2 = request.files['file2']
            
            # Only process second file if it's not empty
            if file2.filename != '':
                text2 = extract_text_from_image(file2)
                courses2 = get_courses_from_ocr(text2)
                
                # Combine courses from both files
                all_courses = courses1 + courses2
        
        # Analyze the combined course list
        cs_requirements = check_cs_courses(all_courses)
        
        # Return the extracted information
        response = jsonify({
            'courses': all_courses,
            'cs_requirements': cs_requirements,
            'success': True
        })
        
        return response
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/api/upload-multiple', methods=['POST'])
def upload_multiple_files():
    """
    Endpoint for uploading multiple files, processing with OCR, and extracting course information.
    
    Expects:
        - An array of files with key 'files[]'
    
    Returns:
        - JSON object with extracted course information from all files combined
    """
    # Check if files were uploaded
    if 'files[]' not in request.files:
        return jsonify({'error': 'No files uploaded'}), 400
    
    files = request.files.getlist('files[]')
    
    # Check if any files were selected
    if len(files) == 0 or all(f.filename == '' for f in files):
        return jsonify({'error': 'No files selected for uploading'}), 400
    
    try:
        all_courses = []
        
        # Process each file
        for file in files:
            if file.filename != '':
                text = extract_text_from_image(file)
                courses = get_courses_from_ocr(text)
                all_courses.extend(courses)
        
        # Analyze the combined course list
        cs_requirements = check_cs_courses(all_courses)
        
        # Return the extracted information
        return jsonify({
            'courses': all_courses,
            'cs_requirements': cs_requirements,
            'success': True
        })
    
    except Exception as e:
        return jsonify({'error': str(e), 'success': False}), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Simple health check endpoint"""
    return jsonify({'status': 'healthy'})

# For local testing only
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)

