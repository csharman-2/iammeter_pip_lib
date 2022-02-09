import unittest
import asyncio
from iammeter.power_meter import WEM3080T
from aioresponses import aioresponses
import json


class Test(unittest.TestCase):

    @aioresponses()
    def test_ensure_nem_data_included(self, mocked):

        iam = WEM3080T('mockmeter', 80, 'DEADBEEF')

        mock_data = {'method': 'uploadsn',
                           'mac': 'B0F8932F6F2F',
                           'version': '2.75.66', 'server': 'em', 'SN': 'DEADBEEF',
                           'Datas': [[247.6, 4.71, -1138, 1123.251, 995.285, 49.97, 0.98],
                                     [246.9, 4.96, -1218, 725.076, 1137.302, 49.97, 0.99],
                                     [241.9, 9.69, 2337, 2704.315, 637.038, 49.97, 1.00],
                                     [245.5, 0.00, -19, 3723.206, 1940.660, 49.97, 1.00]]}

        mocked.get('http://admin:admin@mockmeter:80/monitorjson', body=json.dumps(mock_data), status=200)

        response = asyncio.run(iam.get_data())

        self.assertIn('Voltage_Net', response.data)
        self.assertIn('Power_Net', response.data)
        self.assertIn('ImportEnergy_Net', response.data)
        self.assertIn('ExportGrid_Net', response.data)
        self.assertIn('Frequency_Net', response.data)
        self.assertIn('PF_Net', response.data)
