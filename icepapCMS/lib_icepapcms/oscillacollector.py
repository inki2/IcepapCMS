from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QString
from collections import OrderedDict
from pyIcePAP import EthIcePAPController
import time


class Channel:

    def __init__(self, system, address, signal_name):
        self.signals = OrderedDict([('PosAxis', self._getter_pos_axis),
                                    ('PosTgtenc', self._getter_pos_tgtenc),
                                    ('PosShftenc', self._getter_pos_shftenc),
                                    ('PosEncin', self._getter_pos_encin),
                                    ('PosAbsenc', self._getter_pos_absenc),
                                    ('PosInpos', self._getter_pos_inpos),
                                    ('PosMotor', self._getter_pos_motor),
                                    ('PosCtrlenc', self._getter_pos_ctrlenc),
                                    ('PosMeasure', self._getter_pos_measure),
                                    ('DifAxMeasure', self._getter_dif_ax_measure),
                                    ('DifAxMotor', self._getter_dif_ax_motor),
                                    ('DifAxTgtenc', self._getter_dif_ax_tgtenc),
                                    ('DifAxShftenc', self._getter_dif_ax_shftenc),
                                    ('DifAxCtrlenc', self._getter_dif_ax_ctrlenc),
                                    ('EncEncin', self._getter_enc_encin),
                                    ('EncAbsenc', self._getter_enc_absenc),
                                    ('EncTgtenc', self._getter_enc_tgtenc),
                                    ('EncInpos', self._getter_enc_inpos),
                                    ('StatReady', self._getter_stat_ready),
                                    ('StatMoving', self._getter_stat_moving),
                                    ('StatSettling', self._getter_stat_settling),
                                    ('StatOutofwin', self._getter_stat_outofwin),
                                    ('StatStopcode', self._getter_stat_stopcode),
                                    ('StatWarning', self._getter_stat_warning),
                                    ('StatLim+', self._getter_stat_limit_positive),
                                    ('StatLim-', self._getter_stat_limit_negative),
                                    ('StatHome', self._getter_stat_home),
                                    ('MeasI', self._getter_meas_i),
                                    ('MeasIa', self._getter_meas_ia),
                                    ('MeasIb', self._getter_meas_ib),
                                    ('MeasVm', self._getter_meas_vm)])
        self.system = system
        self.axis = system[address]
        self.sig_name = signal_name
        self.measure_resolution = 1.
        self.signal_val_getter = self.signals[signal_name]
        self.collected_samples = []

    def init(self):
        """Performs some signal dependant checks based on configuration."""
        sn = QString(self.sig_name)
        cond_1 = sn.endsWith('Tgtenc')
        cond_2 = sn.endsWith('Shftenc')
        cond_3 = sn == 'DifAxMeasure'
        if not (cond_1 or cond_2 or cond_3):
            return
        try:
            cfg = self.axis.get_cfg()
        except RuntimeError as e:
            msg = 'Failed to retrieve configuration parameters for driver {}\n{}.'.format(self.axis.addr, e)
            raise Exception(msg)
        if (cond_1 and cfg['TGTENC'].upper() == 'NONE') or (cond_2 and cfg['SHFTENC'].upper() == 'NONE'):
            msg = 'Signal {} is not mapped/valid.'.format(sn)
            raise Exception(msg)
        if cond_3:
            self.measure_resolution = self._calc_measure_resolution(cfg)

    def get_signals(self):
        """
        Retrieves the available signals.

        Return: List of available signals.
        """
        return self.signals.keys()

    def equals(self, icepap_addr, signal_name):
        """
        Checks for equality.

        icepap_addr - IcePAP address.
        signal_name - Signal name.
        Return: True if equal. False otherwise.
        """
        if icepap_addr != self.axis.addr:
            return False
        if signal_name != self.sig_name:
            return False
        return True

    @staticmethod
    def _calc_measure_resolution(cfg):
        tgtenc = cfg['TGTENC'].upper()
        shftenc = cfg['SHFTENC'].upper()
        axisnstep = cfg['ANSTEP']
        axisnturn = cfg['ANTURN']
        nstep = axisnstep
        nturn = axisnturn
        if tgtenc == 'ABSENC' or (tgtenc == 'NONE' and shftenc == 'ABSENC'):
            nstep = cfg['ABSNSTEP']
            nturn = cfg['ABSNTURN']
        elif tgtenc == 'ENCIN' or (tgtenc == 'NONE' and shftenc == 'ENCIN'):
            nstep = cfg['EINNSTEP']
            nturn = cfg['EINNTURN']
        elif tgtenc == 'INPOS' or (tgtenc == 'NONE' and shftenc == 'INPOS'):
            nstep = cfg['INPNSTEP']
            nturn = cfg['INPNTURN']
        return (float(nstep) / float(nturn)) / (float(axisnstep) / float(axisnturn))

    def _getter_pos_axis(self):
        return self.axis.pos

    def _getter_pos_tgtenc(self):
        return self.axis.pos_tgtenc

    def _getter_pos_shftenc(self):
        return self.axis.pos_shftenc

    def _getter_pos_encin(self):
        return self.axis.pos_encin

    def _getter_pos_absenc(self):
        return self.axis.pos_absenc

    def _getter_pos_inpos(self):
        return self.axis.pos_inpos

    def _getter_pos_motor(self):
        return self.axis.pos_motor

    def _getter_pos_ctrlenc(self):
        return self.axis.pos_ctrlenc

    def _getter_pos_measure(self):
        return self.system.get_fpos(self.axis.addr, 'MEASURE')[0]

    def _getter_dif_ax_measure(self):
        return self._getter_pos_axis() - self._getter_pos_measure() / self.measure_resolution

    def _getter_dif_ax_motor(self):
        return self._getter_pos_axis() - self._getter_pos_motor()

    def _getter_dif_ax_tgtenc(self):
        return self._getter_pos_axis() - self._getter_pos_tgtenc()

    def _getter_dif_ax_shftenc(self):
        return self._getter_pos_axis() - self._getter_pos_shftenc()

    def _getter_dif_ax_ctrlenc(self):
        return self._getter_pos_axis() - self._getter_pos_ctrlenc()

    def _getter_enc_encin(self):
        return self.axis.enc_encin

    def _getter_enc_absenc(self):
        return self.axis.enc_absenc

    def _getter_enc_tgtenc(self):
        return self.axis.enc_tgtenc

    def _getter_enc_inpos(self):
        return self.axis.enc_inpos

    def _getter_stat_ready(self):
        return 1 if self.axis.state_ready else 0

    def _getter_stat_moving(self):
        return 1 if self.axis.state_moving else 0

    def _getter_stat_settling(self):
        return 1 if self.axis.state_settling else 0

    def _getter_stat_outofwin(self):
        return 1 if self.axis.state_outofwin else 0

    def _getter_stat_stopcode(self):
        return self.axis.state_stop_code

    def _getter_stat_warning(self):
        return 1 if self.axis.state_warning else 0

    def _getter_stat_limit_positive(self):
        return 1 if self.axis.state_limit_positive else 0

    def _getter_stat_limit_negative(self):
        return 1 if self.axis.state_limit_negative else 0

    def _getter_stat_home(self):
        return 1 if self.axis.state_inhome else 0

    def _getter_meas_i(self):
        return self.axis.meas_i

    def _getter_meas_ia(self):
        return self.axis.meas_ia

    def _getter_meas_ib(self):
        return self.axis.meas_ib

    def _getter_meas_vm(self):
        return self.axis.meas_vm


class Collector:

    def __init__(self, host, port, callback):
        self.host = host
        self.port = port
        self.cb = callback
        self.icepap_system = None
        self.channels_subscribed = {}
        self.channels_started = {}
        self.channel_id = 0
        self.max_buf_len = 10

        try:
            self.icepap_system = EthIcePAPController(self.host, self.port)
        except Exception as e:
            msg = 'Failed to instantiate master controller.\nHost: {}\nPort: {}\n{}'.format(self.host, self.port, e)
            raise Exception(msg)
        if not self.icepap_system:
            msg = 'IcePAP system {} has no active drivers! Aborting.'.format(self.host)
            raise Exception(msg)

        dummy_channel = Channel(self.icepap_system, 1, 'PosAxis')  # Using dummy values.
        self.signals = dummy_channel.get_signals()

        self.tick_interval = 100  # [milliseconds]
        self.ticker = QTimer()
        self._connect_signals()
        self.ticker.start(self.tick_interval)

    def _connect_signals(self):
        self.ticker.timeout.connect(self._tick)  # Todo: Fix warning.

    def get_available_drivers(self):
        """
        Retrieves the available drivers.

        Return: List of available drivers.
        """
        return self.icepap_system.keys()

    def get_available_signals(self):
        """
        Retrieves the available signals.

        Return: List of available signals.
        """
        return self.signals

    def get_signal_index(self, signal_name):
        """
        Retrieves the fixed index of a signal from its name.

        Return: Signal index.
        """
        return self.signals.index(signal_name)

    @staticmethod
    def get_current_time():
        """
        Retrieves the current time.

        Return: Current time as seconds (with fractions) from 1970.
        """
        return time.time()

    def subscribe(self, icepap_addr, signal_name):
        """
        Creates a new subscription for signal values.

        icepap_addr - IcePAP driver number.
        signal_name - Signal name.
        Return - A positive integer id used when unsubscribing.
        """
        for ch in self.channels_subscribed.values():
            if ch.equals(icepap_addr, signal_name):
                msg = 'Channel already exists.\nAddr: {}\nSignal: {}'.format(icepap_addr, signal_name)
                raise Exception(msg)
        channel = Channel(self.icepap_system, icepap_addr, signal_name)
        try:
            channel.init()
        except Exception as e:
            msg = 'Failed to initialize new channel.\nAddr: {}\nSignal: {}\n{}'.format(icepap_addr, signal_name, e)
            raise Exception(msg)
        self.channel_id += 1
        self.channels_subscribed[self.channel_id] = channel
        return self.channel_id

    def start(self, subscription_id):
        """
        Starts collecting data for a subscription.

        subscription_id - The given subscription id.
        """
        if subscription_id in self.channels_subscribed.keys() and subscription_id not in self.channels_started.keys():
            self.channels_started[subscription_id] = self.channels_subscribed[subscription_id]

    def unsubscribe(self, subscription_id):
        """
        Cancels a subscription.

        subscription_id - The given subscription id.
        """
        """Cancels a subscription."""
        if subscription_id in self.channels_subscribed.keys():
            del self.channels_started[subscription_id]
            del self.channels_subscribed[subscription_id]

    def _tick(self):
        for subscription_id, channel in self.channels_started.iteritems():
            try:
                val = channel.signal_val_getter()
                tv = (time.time(), val)
                channel.collected_samples.append(tv)
                if len(channel.collected_samples) >= self.max_buf_len:
                    self.cb(subscription_id, channel.collected_samples)
                    channel.collected_samples = []
            except RuntimeError as e:
                msg = 'Failed to collect data for signal {}\n{}'.format(channel.sig_name, e)
                print(msg)  # Todo: Investigate oscilla shutdown when started from IcePAPcms.
        self.ticker.start(self.tick_interval)
