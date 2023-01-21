from flask import Flask, render_template,url_for,request
import pandas as pd
import json
import plotly
import plotly.express as px
from utils import plot_avg,plot_counts,plot_scatter

app = Flask(__name__)

@app.route('/')
def index():
    booking_titles = ['Average price per type of stay','Number of property types','Notes en fonction du prix et du type de sejour',
    'Average number of reviews per type','Notes en fonction du nombre de commentaires par type']

    flights_titles = ['Temps moyen d\'un vol aller par companie aerienne (en h)','Temps moyen d\'un vol retour par companie aerienne (en h)',
    'Nombre d\'escales par companies aeriennes','Prix moyen par voyage','Temps de vol par compagnie et par prix']

    return render_template('index.html',booking_titles = booking_titles,flights_titles = flights_titles)

@app.route('/products',methods=['GET', 'POST'])
def show_products():
    sort = request.form.get("sort")
    print(str(sort))
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')
    cross_housing_flights = pd.merge(booking_clean,flights,how = 'cross')[0:20]
    cross_housing_flights['total_price'] = cross_housing_flights['price_int'] + cross_housing_flights['price_float']
    if sort == 'no filter':
        pass
    elif sort == 'price':
        cross_housing_flights = cross_housing_flights.sort_values(by='total_price')
    
    
    columns = ['total_price','voyage_companies','voyage_in_h','allerdepart',
    'allerarrivee','retourdepart','retourarrivee','title','score']
    rename_attributes = ['Prix du voyage','Compagnies aeriennes','Durée du voyage','Aeroport de départ (aller)',
    'Aeroport d\'arrivee (aller)','Aeroport de départ (retour)','Aeroport d\'arrivee (retour)','Logement','Note du logement']
    attributes = [list(cross_housing_flights[col]) for col in columns]
    dict_attributes = dict(zip(rename_attributes,attributes))
    n_values = len(list(dict_attributes.values())[0])

    return render_template('products.html',dict_attributes = dict_attributes,n_values = n_values)



@app.route('/chart_booking/<int:chart_id>')
def chart_booking(chart_id):
    booking_clean = pd.read_csv('../csvs/booking_clean.csv')
    
    if chart_id == 1:
        fig = plot_avg(booking_clean,'property_type','price_int',width = 800,height=400,title='Average price per type of stay')
    elif chart_id == 2:
        fig = plot_counts(booking_clean,'property_type',title='Number of property types')
    elif chart_id == 3:
        fig = plot_scatter(booking_clean,'price_int','score_float','property_type',x_limit = 1000,names=['Guesthouse','Hotel','Apartment'],
    title = 'Notes en fonction du prix et du type de sejour',col1_name='prix',col2_name='note',col3_name='type')
    elif chart_id == 4:
        fig = plot_avg(booking_clean,'property_type','n_reviews_float',title = 'Average number of reviews per type')
    elif chart_id == 5:
        fig = plot_scatter(booking_clean,'n_reviews_float','score_float','property_type',x_limit = 5000,names=['Guesthouse','Hotel','Apartment'],
    title = 'Notes en fonction du nombre de commentaires par type',col1_name='number of reviews',col2_name='note',col3_name='type')

    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('chart.html', graphJSON=graphJSON)


@app.route('/chart_flights/<int:chart_id>')
def chart_flights(chart_id):
    flights = pd.read_csv('../csvs/flights_clean.csv',sep = ';')
    
    if chart_id == 1:
        fig = plot_avg(flights,'allercompanie','aller_time_in_h',title = 'Temps moyen d\'un vol aller par companie aerienne (en h)')
    elif chart_id == 2:
        fig = plot_avg(flights,'retourcompanie','retour_time_in_h',title = 'Temps moyen d\'un vol retour par companie aerienne (en h)')
    elif chart_id == 3:
        fig = plot_counts(flights,['allercompanie','allerescale'],barmode='relative',title='Nombre d\'escales par companies aeriennes')
    elif chart_id == 4:
        fig = plot_avg(flights,'voyage_companies','price_float',height=600,title='Prix moyen par voyage')
    elif chart_id == 5:
        fig = plot_scatter(flights,'price_float','voyage_in_h','voyage_companies',x_limit = 1000,names=['Iberia','Air France','Ryanair'],
    title = 'Temps de vol par compagnie et par prix',col1_name='prix',col2_name='temps (h)',col3_name='companie')


    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('chart.html', graphJSON=graphJSON)



app.run(debug=True)