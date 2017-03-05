class FaultsLoader():
    def __init__(self):
        self.conn = dbo.db_connect()
        # self.reg_shp = r'(.shp$)'
        self.shapefile = "./data/faults/sectionsALL.shp"


    def line_str(self, coords):
        line_strs = [str(p[0]) + ' ' + str(p[1]) for p in coords]
        line_str = 'LINESTRING((' + ','.join(line_strs) + '))'
        return poly_str

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
            line_str = self.line_str(f['coordinates'][0])
            data.append((name, ftype, length, sliprate, slipcode, slipsense,
                age, line_str, None))
            print (data)
            break

        query = "INSERT INTO claims_geo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return

loader = FaultsLoader()
loader.parse_faults()
