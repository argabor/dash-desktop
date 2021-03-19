from threading import Thread

import PyQt5.QtCore as core
import PyQt5.QtWidgets as core_widgets
import PyQt5.QtWebEngine as web_engine
import PyQt5.QtWebEngineWidgets as web_widgets
import PyQt5.QtGui as gui

import logging
import sys

default_url = "127.0.0.1"
default_port = 8050


class DashUI(object):
    def __init__(self, app, url=default_url, port=default_port, proxy=None,
                 debug=False, icon_path=None, app_name=None, 
                 contextMenuPolicy=core.Qt.NoContextMenu,
                 showMaximized=True, zoomFactor=1.0, resize=(900, 800),
                 disable_url_logging=True, disable_server_banner=True, disable_url_printing=False,
                 **extra_options):
        self.dash_app = app
        
        if disable_url_logging:
            self.dash_app.logger.disabled = True
            log = logging.getLogger('werkzeug')
            log.disabled = True
        if disable_server_banner:
            cli = sys.modules['flask.cli']
            cli.show_server_banner = lambda *x: None
        self.disable_url_printing = disable_url_printing
        
        self.dash_thread = Thread(target=self._run_dash,
                                    args=( url, port, proxy, debug ),
                                    kwargs=extra_options )
        self.dash_thread.daemon = True
        self.debug = debug

        self.url = "http://{}:{}".format(url, port)
        self.app = core_widgets.QApplication([])
        self.app.setWindowIcon(gui.QIcon(icon_path))
        self.app.setApplicationName(app_name)
        self.view = web_widgets.QWebEngineView(self.app.activeModalWidget())
        self.view.setContextMenuPolicy(contextMenuPolicy)
        self.page = CustomWebEnginePage(self.view)
        self.view.setPage(self.page)
        self.view.setZoomFactor(zoomFactor)
        self.view.resize(*resize)
        self.showMaximized = showMaximized

    def run(self):
        self.run_dash()
        self.run_gui()

    def run_dash(self):
        self.dash_thread.start()

    def run_gui(self):
        self.view.load(core.QUrl(self.url))

        change_setting = self.view.page().settings().setAttribute
        settings = web_widgets.QWebEngineSettings
        change_setting(settings.LocalStorageEnabled, True)
        change_setting(settings.PluginsEnabled, True)

        # TODO: These settings aren't implemented in QWebEngineSettings (yet)
        #change_setting(settings.DeveloperExtrasEnabled, True)
        #change_setting(settings.OfflineStorageDatabaseEnabled, True)
        #change_setting(settings.OfflineWebApplicationCacheEnabled, True)

        if self.showMaximized:
            self.view.showMaximized()
        else:
            self.view.show()

        self.app.exec_()

    def _run_dash(self, host, port, proxy=None, debug=False, **extra_options):
        if not self.disable_url_printing:
            print(f'Serving app from {self.url}')
        self.dash_app.run_server(debug=debug, host=host, port=port, use_reloader=False, **extra_options)


class CustomWebEnginePage(web_widgets.QWebEnginePage):
    def createWindow(self, _type):
        page = CustomWebEnginePage(self)
        page.urlChanged.connect(self.open_browser)
        return page

    def open_browser(self, url):
        page = self.sender()
        gui.QDesktopServices.openUrl(url)
        page.deleteLater()