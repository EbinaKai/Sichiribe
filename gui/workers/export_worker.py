from PySide6.QtCore import Signal, QThread
from cores.exporter import Exporter
import logging

class ExportWorker(QThread):
    def __init__(self, params):
        super().__init__()
        self.params = params
        self.ep = Exporter(params['format'], params['out_dir'])
        self.logger = logging.getLogger('__main__').getChild(__name__)
        self.logger.info('Exporter Worker loaded')

    def run(self):
        data = self.ep.format(self.params['results'], self.params['failed_rates'], self.params['timestamps'])
        self.ep.export(data)
        
        return None
        