from django.db import connection
import logging
import csv
from datetime import datetime as dt

logger=logging.getLogger('development')

# SQL for adding the data
sql_insert=("insert into result (measured_date, measured_value, point_id, place_id, created_at, updated_at) "
              "select * from (select%s as measured_date, %s as measured_value, %s as point_id, %s as place_id,"
              "%s as created_at, %s as updated_at) as tmp "
              "where not exists (select * from measured_date where point = %s and measured_date = %s)")

def regist_data(cursor,file_path):
    # read csv file
    try:
        file=open(file_path,newline='')
    except IOError:
        logger.warning('対象ファイルがありません:'+file_path)
        logger.warning('DB登録は行いません:'+file_path)
    else:
        logger.info('=== > Start DB登録 ===')
        with file:
            reader=csv.reader(file)
            header=next(reader) # skip header line

            """ tuple's format of add_data
            [   0,         ,1          ,2       ,3]  
            [measure_date, measured_value, point_id, place_id """
            for row in reader:
                str_time=[dt.now().strftime('%Y-%m-%d %H:%M:%S')]
                add_data=[]
                add_data.extend(row)        # read data from csv file
                add_data.extend(str_time)   # created_at

                add_data.extend(str_time)   # updated_at
                add_data.append(row[3])     # point id(対象レコードがDBに存在するかの確認用)
                add_data.append(row[0])     # 対象日時(対象レコードがDBに存在するかの確認用)
                logger.debug('add_data='+str(add_data))

                # addd the record
                cursor.execute(sql_insert,add_data)

            logger.info("=== End DB登録 ===")

# to register the data in csv file
def insert_csv_data(file_path):
    logger.info('=== csvデータ登録開始 ===')

    with connection.cursor() as cursor:
        regist_data(cursor,file_path)

    logger.info('=== csvデータ登録処理終了 ===')