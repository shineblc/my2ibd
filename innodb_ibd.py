import json
import re
import os
import numpy as np
from datetime import datetime


class innodb_ibd():
    def __init__(self):
        pass

    def get_json(self, base_dir):
        pass

    def get_dir(self):
        abs_path = os.path.abspath(__file__)
        base_path = os.path.dirname(abs_path)
        p1 = os.path.join(base_path, 'ibd_json')
        data = os.listdir(p1)
        json_list = []
        for data1 in data:
            json_list.append(os.path.join(p1, data1))
        return json_list

    def get_ddl(self):
        ibd_list = self.get_dir()
        for idb_js in ibd_list:
            with open(f"{idb_js}", "r", encoding='utf-8') as f:
                data = json.load(f)
            data_ddl = data[1]
            data_engine = data[2]
            engine = data_engine.get('object').get('dd_object').get('engine')
            comment = data_engine.get('object').get('dd_object').get('comment')
            table_name = data_ddl.get('object').get('dd_object').get('name')
            cols = ''
            hn = "'"
            coll = {}
            column_list = []
            column_listidx = []
            ddl = f"CREATE TABLE {table_name}"
            cols = ''
            for column in data_ddl['object']['dd_object']['columns']:
                if column['name'] in ['DB_TRX_ID', 'DB_ROLL_PTR', 'DB_ROW_ID', 'FTS_DOC_ID']:
                    continue
                else:
                    column_list.append(column['name'])

                    cols += f"\n{column['name']} {column['column_type_utf8']}{'' if column['is_nullable'] else ' NOT NULL '}" \
                            f"{' DEFAULT NULL' if column['default_value_null'] and column['default_value_utf8'] != 'CURRENT_TIMESTAMP' else ''}" \
                            f"{' NULL ' if column['update_option'] == 'CURRENT_TIMESTAMP' else ''}" \
                            f"{' default ' + hn + column['default_value_utf8'] + hn if column['default_value_utf8'] and column['default_value_utf8'] != 'CURRENT_TIMESTAMP' else ''}" \
                            f"{' AUTO_INCREMENT ' if column['is_auto_increment'] else ''} {' DEFAULT ' + column['default_value_utf8'] if column['default_value_utf8'] == 'CURRENT_TIMESTAMP' and column['update_option'] != 'CURRENT_TIMESTAMP' else ''}" \
                            f"{' DEFAULT ' + column['default_value_utf8'] + ' ON ' + 'UPDATE ' + column['update_option'] if column['default_value_utf8'] == 'CURRENT_TIMESTAMP' and column['update_option'] == 'CURRENT_TIMESTAMP' else ''} " \
                            f"{' comment ' + hn + column['comment'] + hn if column['comment'] else ''},"

            index_name = data_ddl.get('object').get('dd_object').get('indexes')
            foreign_name = data_ddl.get('object').get('dd_object').get('foreign_keys')
            indexl = []
            pk = "PRIMARY KEY"
            ix = "index "
            full = "FULLTEXT KEY "
            for i in index_name:

                # 对于全局索引，只是利用的type去做简单判断，唯一索引和全局索引在ibd中 并没有显示字段表示，故不做处理
                idx_name = f"{pk if i['name'] == 'PRIMARY' else ''}{ix + i['name'] if i['name'] != 'PRIMARY' and i['type'] != 4 else ''}{full + i['name'] if i['type'] == 4 else ''}"

                idxl = []
                for idx_c in i['elements']:
                    if idx_c['length'] < 4294967295:
                        idxl.append(idx_c['column_opx'])

                if len(idxl) == 0:
                    continue
                # for nnn in idxl:
                indexl.append(f'{idx_name}({",".join([column_list[x] for x in idxl])})')
            foreign_key_list=[]
            for foreign_i in foreign_name:
                for elements in foreign_i['elements']:
                    # CONSTRAINT `fk_boy_girl_boy` FOREIGN KEY (`boy_id`) REFERENCES `boy` (`id`),
                    fidx_name = f"{'CONSTRAINT ' + foreign_i['name'] +' FOREIGN KEY' +  '(' + column_list[elements.get('column_opx')] + ')' + ' REFERENCES ' +foreign_i['referenced_table_name']+ ' (' + elements['referenced_column_name'] + ')'}"
                    foreign_key_list.append(fidx_name)
            indexl2 = list(np.unique(indexl))
            index = ",".join([x for x in indexl2])
            foreign_index=",".join([x for x in foreign_key_list])
            print(foreign_index)
            col_index = f"{cols}\n{index}" if len(index) > 0 else f"{cols[:-1]}"
            ddl = f"{ddl}({col_index},{foreign_index}) ENGINE={engine} {' COMMENT ' + hn + comment + hn if comment else ''};".strip()
            ddl_res = re.sub(' +', ' ', ddl)
            now = datetime.now()  # 获得当前时间
            timestr = now.strftime("%Y_%m_%d")
            path_sql = 'sql' + timestr
            if not os.path.exists(path_sql):
                os.makedirs(path_sql)
            with open("{}/{}.sql".format(path_sql, table_name), mode='w', encoding='utf-8') as sql_object:
                sql_object.write(ddl_res)
            return ddl_res


if __name__ == '__main__':
    res = innodb_ibd()
    res.get_ddl()
