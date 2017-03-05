import src.database_operations as dbo
import fiona
import os
import re


class ClaimsLoader():
    def __init__(self):
        self.conn = dbo.db_connect()
        self.reg_shp = r'((?i)[a-z]{1,5}_pls_\d{2,3}.shp$)'
        self.reg_txt = r'((?i)[a-z]{1,5}_total.txt)'
        self.main_dir = "./data/claims"

    def polygon_str(self, coords):
        poly_strs = [str(p[0]) + ' ' + str(p[1]) for p in coords]
        poly_str = 'POLYGON((' + ','.join(poly_strs) + '))'
        return poly_str

    def load_shapefile(self, file_path):
        # state = file_path.split('/')[-2]
        print ('Parsing shapefiles for %s' % file_path)
        layer = fiona.open(file_path)
        # layer.schema
        data = []
        for f in layer:
            try:
                mtrs = f['properties']['mtrs']
            except:
                try:
                    mtrs = f['properties']['MTRS']
                except:
                    mtrs = None
            claim_id = f['id']
            poly_str = self.polygon_str(f['geometry']['coordinates'][0])
            if len(poly_str) > 1000:
                continue
            data.append((claim_id, mtrs, poly_str, None))

        query = "INSERT INTO claims_geo VALUES (%s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return


    def load_claims_meta(self, file_path):
        print ('Parsing text file %s' % file_path)
        f = open(file_path, 'r')

        data = []
        for i, line in enumerate(f.readlines()):
            if i == 0:
                continue
            line = line.strip().split(',')
            data.append(tuple(line))

        query = "INSERT INTO claims_meta VALUES (%s, %s, %s, %s)"
        dbo.execute_query(self.conn, query, data, multiple=True)
        return

    def parse_claims(self):
        for root, dirs, files in os.walk(self.main_dir, topdown=False):
            for name in files:
                if re.match(self.reg_txt, name):
                    full_path = os.path.join(root, name)
                    self.load_claims_meta(full_path)
                if re.match(self.reg_shp, name):
                    full_path = os.path.join(root, name)
                    self.load_shapefile(full_path)
        return

loader = ClaimsLoader()
loader.parse_claims()
