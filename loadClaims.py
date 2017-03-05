import src.database_operations as dbo
import fiona
import os
import re



class ClaimsLoader():
    def __init__(self):
        self.conn = dbo.db_connect()
        self.reg_shp = r'((?i)[a-z]{1,5}_pls_\d{2,3}(?:_Project)?.shp$)'
        self.reg_txt = r'((?i)[a-z]{1,5}_total.txt)'
        self.main_dir = "./data/claims"
        self.completed_files = ['AK_pls_07', 'AK_total', '/AZ_pls_10',
            'AZ_TOTAL', 'AR_TOTAL', 'CA_pls_10', 'CA_TOTAL', 'CO_pls_10',
            'CO_TOTAL', 'FL_pls_10', 'FL_TOTAL', 'ID_pls_10', 'ID_TOTAL',
            'MT_pls_10', 'MT_TOTAL', 'NE_pls_10', 'NE_TOTAL', 'NV_pls_10',
            ]

    def polygon_str(self, coords):
        poly_strs = [str(p[0]) + ' ' + str(p[1]) for p in coords]
        poly_str = 'POLYGON((' + ','.join(poly_strs) + '))'
        return poly_str

    def load_shapefile(self, filepath):
        # state = filepath.split('/')[-2]
        print ('Parsing shapefiles for %s' % filepath)
        if self.check_file(filepath):
            return
        layer = fiona.open(filepath)
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

    def check_file(self, filepath):
        file_check = False
        for f in self.completed_files:
            if f in filepath:
                print ('Text file has already been parsed. Moving on...')
                return True
        return file_check

    def load_claims_meta(self, filepath):
        print ('Parsing text file %s' % filepath)
        if self.check_file(filepath):
            return
        f = open(filepath, 'r')

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
