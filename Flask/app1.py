from lib2to3.pgen2.pgen import DFAState
import numpy as np
import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt
import plotly.offline as py
import plotly.graph_objs as go
import seaborn as sns
import warnings
warnings.filterwarnings('always')
warnings.filterwarnings('ignore')
import nltk
nltk.download('punkt')
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.metrics.pairwise import linear_kernel
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import flask
from flask import Flask, redirect, render_template, request, url_for
import pickle

app = Flask(__name__)

# Define tfidf_matrix globally
tfidf_matrix = None

# Load the updated dataset
zomato_df = pd.read_csv(r'C:\Users\sunik\OneDrive\Desktop\Resturant_Recommendation_System\Flask\restaurant1.csv')

def get_recommendations(restaurant_name):
    # Find the details of the input restaurant
    input_restaurant = zomato_df[zomato_df['name'] == restaurant_name].iloc[0]

    # Get the first keyword of the cuisine of the input restaurant
    first_cuisine_keyword = input_restaurant['cuisines'].split()[0]

    # Filter restaurants with cuisines that start with the first keyword
    similar_restaurants = zomato_df[zomato_df['cuisines'].apply(lambda x: x.split()[0] == first_cuisine_keyword)]

    # Sort by Mean Rating (in descending order)
    top_restaurants = similar_restaurants.sort_values(by='Mean Rating', ascending=False)

    # Remove duplicates while preserving order
    top_restaurants = top_restaurants[~top_restaurants.duplicated(subset=['name', 'cuisines', 'cost'], keep='first')]

    # Convert cost to thousands
    top_restaurants['cost'] = top_restaurants['cost']
    
    return top_restaurants.head(10)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/recommend', methods=['GET'])
def recommend():
    return render_template('recommend.html')

@app.route('/result', methods=['GET', 'POST'])
def result():
    if request.method == 'POST':
        restaurant_name = request.form.get('restaurant_name')
        if not restaurant_name:
            return "Error: No restaurant name provided. Please go back and enter a restaurant name."
        top_restaurants = get_recommendations(restaurant_name)
        if isinstance(top_restaurants, str):
            # If top_restaurants is a string, it's an error message
            return top_restaurants
        top_restaurants_list = top_restaurants.to_dict('records')
        return render_template('result.html', recommended_restaurants=top_restaurants_list)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)




