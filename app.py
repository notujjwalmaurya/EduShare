from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Mock data for resources (initialize empty to allow for uploads)
resources = []

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/resources')
def view_resources():
    # Get search and category filters
    search = request.args.get('search', '').lower()
    category = request.args.get('category', 'all')
    
    # Filter resources based on search query and category
    filtered_resources = resources
    if search:
        filtered_resources = [r for r in filtered_resources 
                              if search in r['title'].lower() 
                              or search in r['description'].lower()]
    if category != 'all':
        filtered_resources = [r for r in filtered_resources 
                              if r['category'] == category]
    
    return render_template('resources.html', resources=filtered_resources)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Collect form data
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        file = request.files['file']

        # Check if file and fields are filled
        if file and title and description:
            # Save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Add uploaded resource to the resources list
            new_resource = {
                "id": len(resources) + 1,
                "title": title,
                "description": description,
                "category": category,
                "rating": 0,  # Default rating
                "filename": filename  # Save filename for download link
            }
            resources.append(new_resource)

            # Flash success message and redirect to resources page
            flash('File uploaded successfully!')
            return redirect(url_for('view_resources'))
        else:
            flash('Please complete all fields and select a file.')
            return redirect(request.url)
    
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
