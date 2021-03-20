from dashui import DashUI

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

port = DashUI.get_open_port()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
ui = DashUI(app, port=port, app_name='DashUI test', showMaximized=False, resize=(600, 250)) # Create a DashUI instance

app.layout = html.Div([
    html.H1("DashUI test!"),
    html.H6("Change the value in the text box to see callbacks in action!"),
    html.Div(["Input: ",
              dcc.Input(id='my-input', value='initial value', type='text')]),
    html.Br(),
    html.Div(id='my-output'),
])

@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return 'Output: {}'.format(input_value)

if __name__ == '__main__':
    ui.run()
