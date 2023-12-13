from flask import Flask, render_template, request
import pandas as pd
from instagram_scraper import get_insta_reels_stat
from youtube_scraper import get_shorts_statistics


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        return 'No file part'
    
    file = request.files['file']

    if file.filename == '':
        return 'No selected file'
    youtube_data_list = []
    insta_data_list = [] 
    if file:
        # Read the Excel file
        df = pd.read_excel(file)

        # Print rows in the terminal
        print("Rows in Excel file:")
        for index, row in df.iterrows():
            #print(row)
            if 'Instagram'  in row.to_dict():
                print(f"Instagram: {row.to_dict()['Instagram']}")
                insta_data_list.append(get_insta_reels_stat(row.to_dict()['Instagram']))
            if 'Youtube'  in row.to_dict():
                print(f"Youtube: {row.to_dict()['Youtube']}")
                youtube_data_list.append(get_shorts_statistics(row.to_dict()['Youtube']))
        print(insta_data_list)
        print(youtube_data_list)
        
        # Convert the list of dictionaries to a DataFrame
        df_insta = pd.DataFrame(insta_data_list)
        df_youtube = pd.DataFrame(youtube_data_list)

        # Save the DataFrame to a xlsx file
        df_insta.to_excel('insta_data_list.xlsx', index=False)
        df_youtube.to_excel('youtube_data_list.xlsx', index=False)

        return 'Statistics completed xlsx file saved with insta_data_list , youtube_data_list.'

if __name__ == '__main__':
    app.run(debug=True)
