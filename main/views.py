from django.shortcuts import render
# Create your views here.

# generic base view
from django.views.generic import TemplateView 


#folium
import folium
from folium import plugins


#gee
import ee

ee.Initialize()


#home
class home(TemplateView):
    template_name = 'index.html'

    # Define a method for displaying Earth Engine image tiles on a folium map.
    def get_context_data(self, **kwargs):

        figure = folium.Figure()
        
        #create Folium Object
        m = folium.Map(
            location=[34.2950933, 48.82412],
            zoom_start=15.25
        )

        #add map to figure
        m.add_to(figure)

        
        #select the Dataset Here's used the MODIS data
        dataset = (ee.ImageCollection('MODIS/006/MOD13Q1')
                  .filter(ee.Filter.date('2019-07-01', '2019-11-30'))
                  .first())
        modisndvi = dataset.select('NDVI')

        #Styling 
        vis_paramsNDVI = {
            'min': 0,
            'max': 9000,
            'palette': [ 'FE8374', 'C0E5DE', '3A837C','034B48',]}

        
        #add the map to the the folium map
        map_id_dict = ee.Image(modisndvi).getMapId(vis_paramsNDVI)
       
        #GEE raster data to TileLayer
        folium.raster_layers.TileLayer(
                    tiles = map_id_dict['tile_fetcher'].url_format,
                    attr = 'Google Earth Engine',
                    name = 'NDVI',
                    overlay = False,
                    control = True
                    ).add_to(m)

        folium.CircleMarker(
		location=[34.284985,48.8170867],
		radius=150,
		popup="Laurelhurst Park",
		color="#1fc219",
		fill=True,
		fill_color="#1fc219",
		).add_to(m)

        #add Layer control
        m.add_child(folium.LayerControl())
       
        #figure 
        figure.render()
         
        #return map
        return {"map": figure}