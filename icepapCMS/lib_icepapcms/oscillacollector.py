from PyQt4.QtCore import QTimer
from PyQt4.QtCore import QString
import time
from pyIcePAP import EthIcePAPController


class Channel:

    def __init__(self, system, address, signal_name):
        self.system = system
        self.axis = system[address]
        self.sig_name = signal_name
        self.measure_resolution = 1.
        self.signal_val_getter = self._set_signal_val_getter(signal_name)
        self.collected_samples = []

        try:
            cfg = self.axis.get_cfg()
        except RuntimeError as e:
            msg = 'Failed to retrieve configuration parameters for driver {}\n{}.'.format(self.axis.addr, e)
            raise Exception(msg)
        sn = QString(self.sig_name)
        if (sn.endsWith('Tgtenc') and cfg['TGTENC'].upper() == 'NONE') or \
                (sn.endsWith('Shftenc') and cfg['SHFTENC'].upper() == 'NONE'):
            msg = 'Signal {} is not mapped/valid.'.format(sn)
            raise Exception(msg)
        if self.sig_name == 'DifAxMeasure':
            self.measure_resolution = self._calc_measure_resolution(cfg)

    def equals(self, icepap_addr, signal_name):
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

    def _getter_enc_encin(self):
        return self.axis.enc_encin

    def _getter_enc_absenc(self):
        return self.axis.enc_absenc

    def _getter_enc_tgtenc(self):
        return self.axis.enc_tgtenc

    def _getter_enc_inpos(self):
        return self.axis.enc_inpos

    def _getter_stat_moving(self):
        return 1 if self.axis.state_moving else 0

    def _getter_stat_settling(self):
        return 1 if self.axis.state_settling else 0

    def _getter_stat_outofwin(self):
        return 1 if self.axis.state_outofwin else 0

    def _getter_stat_ready(self):
        return 1 if self.axis.state_ready else 0

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

    def _set_signal_val_getter(self, sig):
        if sig == 'PosAxis':
            return self._getter_pos_axis
        elif sig == 'PosTgtenc':
            return self._getter_pos_tgtenc
        elif sig == 'PosShftenc':
            return self._getter_pos_shftenc
        elif sig == 'PosEncin':
            return self._getter_pos_encin
        elif sig == 'PosAbsenc':
            return self._getter_pos_absenc
        elif sig == 'PosInpos':
            return self._getter_pos_inpos
        elif sig == 'PosMotor':
            return self._getter_pos_motor
        elif sig == 'PosCtrlenc':
            return self._getter_pos_ctrlenc
        elif sig == 'PosMeasure':
            return self._getter_pos_measure
        elif sig == 'DifAxMeasure':
            return self._getter_dif_ax_measure
        elif sig == 'DifAxMotor':
            return self._getter_dif_ax_motor
        elif sig == 'DifAxTgtenc':
            return self._getter_dif_ax_tgtenc
        elif sig == 'DifAxShftenc':
            return self._getter_dif_ax_shftenc
        elif sig == 'DifAxCtrlenc':
            return self._getter_dif_ax_ctrlenc
        elif sig == 'EncEncin':
            return self._getter_enc_encin
        elif sig == 'EncAbsenc':
            return self._getter_enc_absenc
        elif sig == 'EncTgtenc':
            return self._getter_enc_tgtenc
        elif sig == 'EncInpos':
            return self._getter_enc_inpos
        elif sig == 'StatMoving':
            return self._getter_stat_moving
        elif sig == 'StatSettling':
            return self._getter_stat_settling
        elif sig == 'StatOutofwin':
            return self._getter_stat_outofwin
        elif sig == 'StatReady':
            return self._getter_stat_ready
        elif sig == 'StatStopcode':
            return self._getter_stat_stopcode
        elif sig == 'StatWarning':
            return self._getter_stat_warning
        elif sig == 'StatLim+':
            return self._getter_stat_limit_positive
        elif sig == 'StatLim-':
            return self._getter_stat_limit_negative
        elif sig == 'StatHome':
            return self._getter_stat_home
        elif sig == 'MeasI':
            return self._getter_meas_i
        elif sig == 'MeasIa':
            return self._getter_meas_ia
        elif sig == 'MeasIb':
            return self._getter_meas_ib
        elif sig == 'MeasVm':
            return self._getter_meas_vm
        else:
            msg = 'Internal error! No function would map to signal {}'.format(sig)
            raise Exception(msg)


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

        self.tick_interval = 100  # [milliseconds]
        self.ticker = QTimer()
        self._connect_signals()
        self.ticker.start(self.tick_interval)

    def _connect_signals(self):
        self.ticker.timeout.connect(self._tick)

    def get_available_drivers(self):
        return self.icepap_system.keys()

    @staticmethod
    def get_current_time():
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
        try:
            channel = Channel(self.icepap_system, icepap_addr, signal_name)
        except Exception as e:
            msg = 'Failed to create channel.\nAddr: {}\nSignal: {}\n{}'.format(icepap_addr, signal_name, e)
            raise Exception(msg)
        self.channel_id += 1
        self.channels_subscribed[self.channel_id] = channel
        return self.channel_id

    def start(self, subscription_id):
        if subscription_id in self.channels_subscribed.keys() and subscription_id not in self.channels_started.keys():
            self.channels_started[subscription_id] = self.channels_subscribed[subscription_id]

    def unsubscribe(self, subscription_id):
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
            except RuntimeError as e:  # Todo: Needed?
                msg = 'Failed to collect data for signal {}\n{}'.format(channel.sig_name, e)
                print(msg)
        self.ticker.start(self.tick_interval)
