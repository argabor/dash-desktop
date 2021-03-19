# dash-desktop

dash-desktop is a Python module that allows you to convert Dash apps into cross platform desktop apps.

The project was forked from the [flask-desktop](https://github.com/Widdershin/flask-desktop) project. Thanks to Widdershin.

## Installation:

::

    pip install git+git://github.com/argabor/dash-desktop.git

I'd like to have dash-desktop available on pip, but currently don't have the time and headspace to make that happen. If you want this to happen, please do it and I'll add you as a collaborator to this repo.

## Usage:

::

    from dashui import DashUI # Add DashUI to your imports
    import dash

    app = dash.Dash(__name__)
    ui = DashUI(app, debug=True) # Create a DashUI instance

    # all of your standard dash logic

    if __name__ == '__main__':
      ui.run() #replace app.run_server() with ui.run(), and that's it

dash-desktop is powered by PyQt5, and should run on Windows, Mac and Linux. You can even create standalone executables using PyInstaller!

## License

dash-desktop is licensed under the MIT License. See the LICENSE file for more details.
