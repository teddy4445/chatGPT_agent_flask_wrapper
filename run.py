import os
import re
from io import StringIO
from flask import Flask, request, render_template, session, jsonify
import csv
import pandas as pd
import tempfile
from llm_api import LLMAPI  # Make sure to import LLMAPI class
import json

# Initialize your OpenAI API key here
OPENAI_API_KEY = ''

app = Flask(__name__)
app.secret_key = ''  # Needed for session management

# Directory to store uploaded files
UPLOAD_FOLDER = tempfile.mkdtemp()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Initialize LLMAPI instance
llm_api = LLMAPI(key=OPENAI_API_KEY)

try:
    os.mkdir(os.path.join(os.path.dirname(__file__), "/tmp"))
except:
    pass


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle file upload
        if 'csv_file' not in request.files:
            return 'No file part', 400

        file = request.files['csv_file']

        if file.filename == '':
            return 'No selected file', 400

        if file and file.filename.endswith('.csv'):
            # Save the file to the upload folder

            try:
                csv_data = pd.read_csv(StringIO(file.stream.read().decode('utf-8')), low_memory=False)
            except Exception as error:
                return jsonify({"status": "file wrong", "error_message": error})
            csv_data.dropna(how='all', axis=0, inplace=True)
            csv_data.dropna(how='all', axis=1, inplace=True)

            if len(csv_data) == 0:
                return '<b>System:</b>: The CSV file is empty. Please upload a valid CSV file.', 400

            if all(isinstance(val, str) and val.strip() != '' for val in csv_data.iloc[0]):
                return '<b>System:</b>: The CSV file is empty. Please upload a valid CSV file.', 400

            # make sure the col names are safe to use in SQL
            make_sql_safe_column_names(csv_data)
            # make it a string for the LLM
            csv_text = csv_data.describe().to_string()

            if len(csv_text.replace("_", " ").split()) > 7000:
                return '<b>System:</b>: To many columns in this CSV for the demo. Please upload a valid CSV file.', 400

            file_path = os.path.join("/tmp", file.filename)
            csv_data.to_csv(file_path, index=False)
            session['csv_file_path'] = file_path
            return '<b>System:</b>:CSV file uploaded successfully. You can now query the file.'
        else:
            return '<b>System:</b>: Invalid file type. Please upload a CSV file.', 400

    return render_template('index.html')


@app.route('/query', methods=['POST'])
def query():
    if 'csv_file_path' not in session:
        return 'No CSV file uploaded yet.', 400

    csv_file_path = session['csv_file_path']
    search_text = request.json.get('search_text')

    # Read CSV content
    csv_content = pd.read_csv(csv_file_path)

    # Define the context for the LLM
    context_message = f"Here is the CSV data:\n{csv_content}\nPlease answer the following question based on the data above:"

    # Query LLM
    response = llm_api.data_related_chat(
        csv_text=csv_content,
        chat_so_far=[],
        last_text=search_text,
        temperature=0.2,
        context_message=context_message
    )

    return response


def make_sql_safe_column_names(df):
    # Remove special characters and spaces, replace with underscores
    def clean_column_name(col):
        col = re.sub(r'[^a-zA-Z0-9_\n\t]', '_', col)
        return col.replace(' ', '_')

    # Make all column names lowercase
    df.columns = map(str.lower, df.columns)

    # Clean and make unique column names
    new_columns = []
    seen = set()
    for col in df.columns:
        new_col = clean_column_name(col)
        while new_col in seen:
            new_col += '_'
        seen.add(new_col)
        new_columns.append(new_col)
    df.columns = new_columns


if __name__ == '__main__':
    app.run(debug=True)
