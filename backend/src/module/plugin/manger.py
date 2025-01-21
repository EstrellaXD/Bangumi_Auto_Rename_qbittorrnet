class PluginManger:
    def __init__(self):
        self.plugins = []

    def load(self, plugin):
        self.plugins.append(plugin)

    def run(self):
        for plugin in self.plugins:
            plugin.run()
