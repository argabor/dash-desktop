# package imports
import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from dash import no_update
from flask import session

# local imports
from auth import authenticate_user, validate_login_session
from server import app, server, ui

# login layout content
def login_layout():
    return html.Div(
        [
            dcc.Location(id='login-url', pathname='/login', refresh=False),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            dbc.Card(
                                [
                                    html.H4('Login', className='card-title'),
                                    dbc.Input(id='login-email', placeholder='User', autoFocus=True),
                                    dbc.Input(id='login-password', placeholder='Password', type='password'),
                                    dbc.Button('Submit', id='login-button', color='success', block=True),
                                    html.Br(),
                                    html.Div(id='login-alert')
                                ],
                                body=True
                            ),
                            width=6
                        ),
                        justify='center'
                    )
                ]
            )
        ]
    )


# home layout content
are_sure = dbc.Modal(
    [
        dbc.ModalHeader("Logout"),
        dbc.ModalBody("Are you sure?"),
        dbc.ModalFooter(
            dbc.Row(
                [
                    dbc.Col(dbc.Button("Yes", id="yes-are_sure")),
                    dbc.Col(dbc.Button("Close", id="close-are_sure")),
                ],
                justify="center",
            )
        ),
    ],
    id="modal-are_sure",
    centered=True,
)

test_page = html.Div([
    html.H1("DashUI test!"),
    html.Br(),
    html.H6("Change the value in the text box to see callbacks in action!"),
    dbc.Input(id='my-input', value='initial value', type='text', autoFocus=True),
    html.Br(),
    html.Div(id='my-output'),
    are_sure,
])

@validate_login_session
def app_layout():
    return \
        html.Div([
            dcc.Location(id='home-url',pathname='/home'),
            dbc.Container(
                [
                    dbc.Row(
                        dbc.Col(
                            test_page,
                        ),
                        justify='center'
                    ),

                    html.Br(),

                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Logout', id='logout-button', color='danger', block=True, size='sm'),
                            width=4
                        ),
                        justify='center'
                    ),

                    
                    html.Br()
                ],
            )
        ]
    )

# main app layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),
        html.Div(
            login_layout(),
            id='page-content'
        ),
    ]
)


###############################################################################
# utilities
###############################################################################

# router
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def router(url):
    if url=='/home':
        return app_layout()
    elif url=='/login':
        return login_layout()
    else:
        return login_layout()

# authenticate 
@app.callback(
    [Output('url', 'pathname'),
     Output('login-alert', 'children')],
    [Input('login-button', 'n_clicks'),
     Input('login-email',' n_submit'),
     Input('login-password', 'n_submit'),
    ],
    [State('login-email', 'value'),
     State('login-password', 'value')])
def login_auth(n_clicks, n_submit_email, n_submit_password, email ,pw):
    '''
    check credentials
    if correct, authenticate the session
    otherwise, authenticate the session and send user to login
    '''
    if n_clicks is None \
        and n_submit_email is None \
        and n_submit_password is None:
        return no_update, no_update
    credentials = {'user':email, "password":pw}
    if authenticate_user(credentials):
        session['authed'] = True
        return '/home', ''
    session['authed'] = False
    return no_update, dbc.Alert('Incorrect credentials.', color='danger', dismissable=True)

@app.callback(
    Output('home-url', 'pathname'),
    [Input('yes-are_sure', 'n_clicks')]
)
def logout_(n_clicks):
    '''clear the session and send user to login'''
    if n_clicks is None:
        return no_update
    session['authed'] = False
    return '/login'

@app.callback(
    [Output('modal-are_sure', 'is_open'),
     Output('close-are_sure', 'n_clicks')],
    [Input('logout-button', 'n_clicks'),
     Input('close-are_sure', 'n_clicks')],
    [State('modal-are_sure', 'is_open')],
)
def logout_modal(logout_click, close_click, is_open):
    if close_click is not None:
        return False, None
    elif logout_click is not None:
        return True, None
    else:
        return is_open, close_click

###############################################################################
# callbacks
###############################################################################

# @app.callback(
#     Output('...'),
#     [Input('...')]
# )
# def func(...):
#     ...

@app.callback(
    Output(component_id='my-output', component_property='children'),
    [Input(component_id='my-input', component_property='value')]
)
def update_output_div(input_value):
    return f'Output: {input_value}'

###############################################################################
# run app
###############################################################################

if __name__ == "__main__":
    ui.run()
