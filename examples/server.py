import dash
import dash_bootstrap_components as dbc
from dashui import DashUI
import os

port = DashUI.get_open_port()

external_stylesheets=[dbc.themes.BOOTSTRAP]

app = dash.Dash(
    __name__,
    external_stylesheets=external_stylesheets
)

app.config.suppress_callback_exceptions = True
app.title = 'DashUI test'

server = app.server

# Set the secret key to some random bytes.
server.config['SECRET_KEY'] = os.urandom(16)

ui = DashUI(app, port=port, app_name=app.title, showMaximized=False, resize=(800, 400)) # Create a DashUI instance
