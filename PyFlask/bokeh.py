import pandas as pd
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource, CategoricalColorMapper
from bokeh.palettes import Spectral6
from bokeh.io import curdoc
from bokeh.layouts import row, widgetbox
from bokeh.models import Slider, Select

df=pd.read_csv("https://assets.datacamp.com/production/repositories/401/datasets/09378cc53faec573bcb802dce03b01318108a880/gapminder_tidy.csv")

source = ColumnDataSource(data={'x': df.loc[df['Year']==1970].fertility,
                                'y': df.loc[df['Year']==1970].life,
                                'country': df.loc[df['Year']==1970].Country,
                                'pop': (df.loc[df['Year']==1970].population / 20000000) + 2,
                                'region': df.loc[df['Year']==1970].region,
                               })

regions_list = df.region.unique().tolist() 
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

xmin, xmax = min(df.fertility), max(df.fertility)
ymin, ymax = min(df.life), max(df.life)

hover = HoverTool(tooltips=[('Country', '@country')])

TOOLS = "pan, wheel_zoom, box_zoom, box_select, reset"

p = figure(title='Data', x_axis_label='Fertility (children per woman)', y_axis_label='Life Expectancy (years)',
           plot_width=800, plot_height=500, x_range=(xmin, xmax), y_range=(ymin, ymax),
           tools=TOOLS, toolbar_location = 'right')

p.add_tools(hover)

p.circle(x='x', y='y', source=source, size=10, alpha=1,
         nonselection_fill_alpha=0.2, nonselection_fill_color='grey',
         color=dict(field='region', transform=color_mapper), legend='region')

p.legend.location = 'top_right'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # Set the yr name to slider.value and new_data to source.data
    yr = slider.value
    
    x = x_select.value
    y = y_select.value

    p.xaxis.axis_label = x
    p.yaxis.axis_label = y
    
    new_data = {
        'x'       : df.loc[df['Year']==yr][x],
        'y'       : df.loc[df['Year']==yr][y],
        'country' : df.loc[df['Year']==yr].Country,
        'pop'     : (df.loc[df['Year']==yr].population / 20000000) + 2,
        'region'  : df.loc[df['Year']==yr].region,
    }
    source.data = new_data

    p.x_range.start = min(df[x])
    p.x_range.end = max(df[x])
    p.y_range.start = min(df[y])
    p.y_range.end = max(df[y])
    
    plot.title.text = 'Gapminder data for %d' % yr

slider = Slider(start=1970, end=2010, step=1, value=1970, title='Year')
slider.on_change('value', update_plot)

x_select = Select(options=['fertility', 'life', 'child_mortality', 'gdp'], value='fertility', title='x-axis data')
x_select.on_change('value', update_plot)

y_select = Select(options=['fertility', 'life', 'child_mortality', 'gdp'], value='life', title='y-axis data')
y_select.on_change('value', update_plot)

layout = row(widgetbox(slider, x_select, y_select), p)

curdoc().add_root(layout)
