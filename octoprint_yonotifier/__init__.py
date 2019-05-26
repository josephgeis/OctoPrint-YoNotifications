# coding=utf-8
from __future__ import absolute_import

# (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import requests


class YoNotifierPlugin(octoprint.plugin.SettingsPlugin,
                            octoprint.plugin.AssetPlugin,
                            octoprint.plugin.TemplatePlugin,
                            octoprint.plugin.EventHandlerPlugin):

    # ~~ SettingsPlugin mixin

    def get_settings_defaults(self):
        return dict(
            apiKey="",
            username="",
            events={}
        )
    
    def get_settings_version(self):
        return 1

    def on_settings_migrate(self, target, current):
        stock_settings = dict(
            apiKey="",
            username="",
            events={
                'Startup': {'enabled': False, 'message': 'OctoPrint is now live.'},
                'Shutdown': {'enabled': False, 'message': 'OctoPrint is going down.'},
                'ClientOpened': {'enabled': False, 'message': 'Someone connected from {remoteAddress}.'},
                'ClientClosed': {'enabled': False, 'message': 'Someone disconnected from {remoteAddress}.'},
                'Connecting': {'enabled': False, 'message': 'Attempting to connect to your printer.'},
                'Connected': {'enabled': False, 'message': 'Successfully connected printer on {port}.'},
                'Disconnected': {'enabled': False, 'message': 'Printer disconnected.'},
                'Error': {'enabled': False, 'message': 'Error: {error}'},
                'PrintStarted': {'enabled': False, 'message': 'Started printing {name}.'},
                'PrintFailed': {'enabled': False, 'message': 'Print {name} not finished because of {reason}.'},
                'PrintDone': {'enabled': False, 'message': 'Finished printing {name}.'},
                'PrintCancelling': {'enabled': False, 'message': 'Stopping print {name}.'},
                'PrintCancelled': {'enabled': False, 'message': 'Stopped print {name}.'},
                'PrintPaused': {'enabled': False, 'message': 'Paused print {name}.'},
                'PrintResumed': {'enabled': False, 'message': 'Resumed print {name}.'},
                'CaptureFailed': {'enabled': False, 'message': 'A frame was skipped because {error}.'},
                'MovieRendering': {'enabled': False, 'message': 'Rendering timelapse for {gcode}.'},
                'MovieDone': {'enabled': False, 'message': 'Finished rendering {movie_basename}.'},
                'MovieFailed': {'enabled': False, 'message': "Couldn't render {movie_basename} because ffmpeg exited on {returncode}."},
                'SlicingStarted': {'enabled': False, 'message': 'Slicing {stl}.'},
                'SlicingDone': {'enabled': False, 'message': 'Finished slicing {stl}.'},
                'SlicingCancelled': {'enabled': False, 'message': 'Stopped slicing {stl}.'},
                'SlicingFailed': {'enabled': False, 'message': "Couldn't slice {stl} because {reason}."}
            }
        )

        if current == None:
            self._settings.set([], None, force=True)
            self._settings.set([], stock_settings, force=True)
            self._settings.save(force=True)

    # ~~ AssetPlugin mixin

    def get_assets(self):
        # Define your plugin's asset files to automatically include in the
        # core UI here.
        return dict(
            js=["js/yonotifier.js"]
        )

    # ~ TemplatePlugin mizin

    def get_template_configs(self):
        return [
            dict(type="settings", custom_bindings=False)
        ]
    
    def get_template_vars(self):
        events = self._settings.get(["events"])
        return { "events": events }

    # ~~ Softwareupdate hook

    def get_update_information(self):
        # Define the configuration for your plugin to use with the Software Update
        # Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
        # for details.
        return dict(
            yonotifier=dict(
                displayName="Yo Notifications",
                displayVersion=self._plugin_version,

                # version check: github repository
                type="github_release",
                user="juniorrubyist",
                repo="OctoPrint-YoNotifications",
                current=self._plugin_version,

                # update method: pip
                pip="https://github.com/juniorrubyist/OctoPrint-YoNotifications/archive/{target_version}.zip"
            )
        )

    # ~ EventHandler Plugin
    def on_event(self, event, payload):
        self._logger.info("Event")
        events = self._settings.get(["events"])
        messages = self._settings.get(["messages"])
        if events.get(event):
            self._logger.info("event in keys")
            if events[event].get("enabled"):
                self._logger.info("event enabled")
                self.send_yo(events[event]["message"].format(**payload))
    
    # ~ Send Yo Message
    def send_yo(self, text):
        self._logger.info("Sending Yo: {text}".format(text=text))
        api_token = self._settings.get(["apiKey"])
        username = self._settings.get(["username"])
        self._logger.info({'api_token': api_token, 'username': username, 'text': text})
        r = requests.post("https://api.justyo.co/yo/",
                        data={'api_token': api_token, 'username': username, 'text': text})
        self._logger.info(r.content)

    # ~ Event Handlers
    def print_done(self, event, data):
        please = self._settings.get(["sendPrintDone"])
        if not please:
            return
        name = data['name']
        self.send_yo("Finished printing { name }".format(name=name))


# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
def __plugin_load__():
    global __plugin_implementation__
    __plugin_implementation__ = YoNotifierPlugin()

    global __plugin_hooks__
    __plugin_hooks__ = {
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }
