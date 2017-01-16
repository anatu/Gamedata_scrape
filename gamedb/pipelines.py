# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import csv
import os
import cStringIO
import codecs
from gamedb import settings
from gamedb.items import VgChartzMetaItem
from gamedb.items import VgChartzSalesItem_10wks
from gamedb.items import VgChartzSalesItem_annual
# import cstringIO
# import codecs

path_root = "C:/users/anatu/desktop/ZZ_Tech/keyscrape/gamedb/"

class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        print(row)
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

def write_to_csv(item, filepath):
    writer = UnicodeWriter(open(filepath, 'a'), lineterminator = "\n")
    row = [item[key] for key in item.keys()]
    writer.writerow(row)

class VgChartzPipeline(object):

    def open_spider(self, spider):

        if spider.name == "vgchartz":
            meta_file = open("vgchartz_meta_output.csv", 'a')
            writer = UnicodeWriter(meta_file, lineterminator = "\n")
            writer.writerow(VgChartzMetaItem.fields.keys())
            meta_file.close()

            tenwk_file = open("vgchartz_10wk_output.csv", 'a')
            writer = UnicodeWriter(tenwk_file, lineterminator = "\n")
            writer.writerow(VgChartzSalesItem_10wks.fields.keys())
            tenwk_file.close()

            annual_file = open("vgchartz_annual_output.csv", 'a')
            writer = UnicodeWriter(annual_file, lineterminator = "\n")
            writer.writerow(VgChartzSalesItem_annual.fields.keys())
            annual_file.close()



    def process_item(self, item, spider):

        if spider.name == "vgchartz":

            if isinstance(item, VgChartzMetaItem):
                # filepath = os.path.join(path_root, "vgchartz_meta_output.csv")
                filepath = "vgchartz_meta_output.csv"
                write_to_csv(item, filepath)

            if isinstance(item, VgChartzSalesItem_10wks):
                # filepath = os.path.join(path_root, "vgchartz_10wk_output.csv")
                filepath = "vgchartz_10wk_output.csv"
                write_to_csv(item, filepath)

            if isinstance(item, VgChartzSalesItem_annual):
                # filepath = os.path.join(path_root, "vgchartz_annual_output.csv")
                filepath = "vgchartz_annual_output.csv"
                write_to_csv(item, filepath)

        return item



#############################################################################


# class UnicodeWriter:
#     """
#     A CSV writer which will write rows to CSV file "f",
#     which is encoded in the given encoding.
#     """

#     def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
#         # Redirect output to a queue
#         self.queue = cStringIO.StringIO()
#         self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
#         self.stream = f
#         self.encoder = codecs.getincrementalencoder(encoding)()

#     def writerow(self, row):
#       out_vector = []
#       for s in row:
#           if s == None:
#               out_vector.append(s)
#           else:
#               out_vector.append(s.encode("utf-8"))
#         # self.writer.writerow([s.encode("utf-8") for s in row])
#         self.writer.writerow(out_vector)
#         # Fetch UTF-8 output from the queue ...
#         data = self.queue.getvalue()
#         data = data.decode("utf-8")
#         # ... and reencode it into the target encoding
#         data = self.encoder.encode(data)
#         # write to the target stream
#         self.stream.write(data)
#         # empty queue
#         self.queue.truncate(0)

#     def writerows(self, rows):
#         for row in rows:
#             self.writerow(row)

