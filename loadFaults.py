import src.database_operations as dbo
import fiona
import os
import re

class FaultsLoader():
    def __init__(self):
        self.conn = dbo.db_connect()
        # self.reg_shp = r'(.shp$)'
        self.shapefile = "./data/faults/sectionsALL.shp"


    def line_str(self, coords):
        if isinstance(coords, list):
            line_strs = [str(p[0]) + ' ' + str(p[1]) for p in coords]
        else:
            line_strs = [str(coords[0]) + ' ' + str(coords[1])]
        line_str = 'LINESTRING(' + ','.join(line_strs) + ')'
        return line_str

    def parse_faults(self):
        print ('Parsing shapefiles for %s' % self.shapefile)
        layer = fiona.open(self.shapefile)
        # layer.schema
        data = []
        for f in layer:
            d = dict(f['properties'])
            name = d.get('name', None)
            ftype = d.get('ftype', None)
            length = d.get('length', None)
            sliprate = d.get('sliprate', None)
            slipcode = d.get('slipcode', None)
            slipsense = d.get('slipsense', None)
            age = d.get('age', None)

            if f['geometry']:
                line_str = self.line_str(f['geometry']['coordinates'][0])
            else:
                line_str = None
            data.append((name, ftype, length, sliprate, slipcode, slipsense,
                age, line_str, None))

        query = "INSERT INTO faults VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return

loader = FaultsLoader()
loader.parse_faults()
