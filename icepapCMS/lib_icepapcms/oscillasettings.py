from singleton import Singleton


class OscillaSettings(Singleton):
    """Settings for the oscilla application."""

    def __init__(self, gui, collector):
        """Initializes an instance of class OscillaSettings."""
        # Settings in the collector (held by the collector).
        self.gui = gui
        self.collector = collector
        self.sample_rate_min = collector.tick_interval_min
        self.sample_rate_max = collector.tick_interval_max
        self.sample_rate = collector.tick_interval
        self.dump_rate_min = collector.sample_buf_len_min
        self.dump_rate_max = collector.sample_buf_len_max
        self.dump_rate = collector.sample_buf_len

        # Settings in the GUI (held here).
        self.default_x_axis_length_min = 5  # [Seconds]
        self.default_x_axis_length_max = 3600  # [Seconds]
        self.default_x_axis_length = 30  # [Seconds]

    def announce_update(self):
        self.collector.tick_interval = self.sample_rate
        self.collector.sample_buf_len = self.dump_rate
        self.gui.settings_updated()
