import pandas as pd
import os
from flask import Flask, request, render_template
import webbrowser
from flask_ngrok import run_with_ngrok
#everything in this code is controlled by mr.dhanesh

#here are the things to be happening
app = Flask(__name__)
run_with_ngrok(app)

def save_to_excel(name1, name2, result):
    file_path = r'C:\Users\HP\Documents\Sampflask\dasa.xlsx'
    
    if os.path.exists(file_path):
        try:
            df = pd.read_excel(file_path, engine='openpyxl')
        except Exception as e:
            print(f"Error reading the file: {e}")
            df = pd.DataFrame(columns=['name1', 'name2', 'Result'])
    else:
        df = pd.DataFrame(columns=['name1', 'name2', 'Result'])
    
    new_row = pd.DataFrame([{'name1': name1, 'name2': name2, 'Result': result}])
    df = pd.concat([df, new_row], ignore_index=True)
    
    try:
        df.to_excel(file_path, index=False, engine='openpyxl')
    except Exception as e:
        print(f"Error saving the file: {e}")
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    name1 = request.form['name1']
    name2 = request.form['name2']
    result = process_names(name1.lower(), name2.lower())
    save_to_excel(name1, name2, result)  # Save to Excel
    return render_template('index.html', result=result)

def process_names(s1, s2):
    l1 = list(s1)
    l2 = list(s2)
    for i in s1:
        if i in l2:
            l1.remove(i)
            l2.remove(i)
    
    n = len(l1) + len(l2)
    l = ['Friends', 'Lovers', 'Animals', 'Marriage', 'Enemies', 'Sisters']
    while len(l) != 1:
        g = (n % len(l)) - 1
        k = l[g]
        l = l[g:] + l[:g]
        l.remove(k)
    return l[0]

if __name__ == '__main__':
    webbrowser.open_new('http://127.0.0.1:5000/')
    app.run()
