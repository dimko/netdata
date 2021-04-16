# -*- coding: utf-8 -*-
# Description: example netdata python.d module
# Author: Put your name here (your github login)
# SPDX-License-Identifier: GPL-3.0-or-later

from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler
from dataclasses import dataclass
import threading

from bases.FrameworkServices.SimpleService import SimpleService


@dataclass
class Chart:
    name: str = None
    title: str = "Mocked chart"
    units: str = "percentage"
    family: str = "resources"
    context: str = "test.mock"
    chart_type: str = "stacked"


@dataclass
class Payload:
    dimensions: list = None
    charts: dict = None
    chart_info: Chart = Chart()


priority = 90000

ORDER = [
    'mock',
]

CHARTS = {
    'mock': {
        'options': [Payload.chart_info.name, Payload.chart_info.title, Payload.chart_info.units,
                    Payload.chart_info.family, Payload.chart_info.context, Payload.chart_info.chart_type],
        'lines': [
            k for k, v in Payload.charts.items()
        ] if Payload.charts else [['mock1']]
    }
}


class S(BaseHTTPRequestHandler):

    def _parse_request_queries(self):
        parsed_url = urlparse(f"{self.headers.get('Host')}{self.path}")
        return parse_qs(parsed_url.query)

    def do_GET(self):
        params = self._parse_request_queries()
        if self.path.startswith('/charts'):
            Payload.charts = {k: v[0].split(",")[0] for k, v in params.items()}
        if self.path.startswith('/chart_info'):
            Payload.chart_info = Chart(name=next((v[0].split(",") for k, v in params.items() if k == 'name'),
                                                 Chart.name),
                                       title=next((v[0].split(",")[0] for k, v in params.items() if k == 'title'),
                                                  Chart.title),
                                       units=next((v[0].split(",")[0] for k, v in params.items() if k == 'units'),
                                                  Chart.units),
                                       family=next((v[0].split(",")[0] for k, v in params.items() if k == 'family'),
                                                   Chart.family),
                                       context=next((v[0].split(",")[0] for k, v in params.items() if k == 'context'),
                                                    Chart.context),
                                       chart_type=next(
                                           (v[0].split(",")[0] for k, v in params.items() if k == 'chart_type'),
                                           Chart.chart_type))
        return self.send_response(200)


class Service(SimpleService):
    def __init__(self, configuration=None, name=None):
        SimpleService.__init__(self, configuration=configuration, name=name)
        self.order = ORDER
        self.definitions = CHARTS
        self.run_mock_server = self.start_server()

    def get_chart_options(self):
        return

    @staticmethod
    def check():
        return True

    def get_data(self):
        data = dict()
        charts = Payload.charts

        chart = self.charts['mock']
        chart.params['title'] = Payload.chart_info.title
        chart.params['name'] = Payload.chart_info.name
        chart.params['units'] = Payload.chart_info.units
        chart.params['family'] = Payload.chart_info.family
        chart.params['context'] = Payload.chart_info.context
        chart.params['chart_type'] = Payload.chart_info.chart_type
        chart.refresh()

        if charts:
            for chart in self.charts['mock']:
                if chart not in charts.keys():
                    self.charts['mock'].del_dimension([chart])
            for k, v in charts.items():
                if k not in self.charts['mock']:
                    self.charts['mock'].add_dimension([k])
                data[k] = v

        return data

    def start_server(self):
        thread = threading.Thread(target=HTTPServer(('localhost', 8000), S).serve_forever)
        thread.daemon = True
        return thread.start()
