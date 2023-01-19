from flask import Flask, render_template
import pandas as pd
import json
import plotly
import plotly.express as px
from utils import plot_avg,plot_counts,plot_scatter

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chart1')
def chart1():
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')

    fig = plot_avg(booking_clean,'property_type','price_int',width = 800,height=400,title='Average price per type of stay')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart2')
def chart2():
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')

    fig = plot_counts(booking_clean,'property_type',title='Number of property types')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart3')
def chart3():
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')

    fig = plot_scatter(booking_clean,'price_int','score_float','property_type',x_limit = 1000,names=['Guesthouse','Hotel','Apartment'],
    title = 'Notes en fonction du prix et du type de sejour',col1_name='prix',col2_name='note',col3_name='type')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart4')
def chart4():
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')

    fig = plot_avg(booking_clean,'property_type','n_reviews_float',title = 'Average number of reviews per type')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart5')
def chart5():
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')

    fig = plot_scatter(booking_clean,'n_reviews_float','score_float','property_type',x_limit = 5000,names=['Guesthouse','Hotel','Apartment'],
    title = 'Notes en fonction du prix et du type de sejour',col1_name='number of reviews',col2_name='note',col3_name='type')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart6')
def chart6():
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')
    

    fig = plot_avg(flights,'allercompanie','aller_time_in_h',title = 'Temps moyen d\'un vol aller par companie aerienne (en h)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart7')
def chart7():
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')

    fig = plot_avg(flights,'retourcompanie','retour_time_in_h',title = 'Temps moyen d\'un vol retour par companie aerienne (en h)')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart8')
def chart8():
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')

    fig = plot_counts(flights,['allercompanie','allerescale'],barmode='relative',title='Nombre d\'escales par companies aeriennes')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart9')
def chart9():
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')

    fig = plot_avg(flights,'voyage_companies','price_float',height=600,title='Prix moyen par voyage')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)

@app.route('/chart10')
def chart10():
    flights = pd.read_csv('../csvs/flights_clean.csv',sep=';')

    fig = plot_scatter(flights,'price_float','voyage_in_h','voyage_companies',x_limit = 1000,names=['Iberia','Air France','Ryanair'],
    title = 'Temps de vol par compagnie et par prix',col1_name='prix',col2_name='temps (h)',col3_name='companie')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('notdash2.html', graphJSON=graphJSON)