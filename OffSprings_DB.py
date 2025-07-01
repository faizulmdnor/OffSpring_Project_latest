import pyodbc
from sqlalchemy import create_engine
import pandas as pd
import logging

from sqlalchemy.dialects.mssql.information_schema import columns

DATABASE = 'OffSprings'
SERVER = 'FAIZULONXY\\SQLEXPRESS'

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class sql_offsprings:
    def __init__(self):
        self.conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection=yes;')
        self.cursor = self.conn.cursor()
        self.engine = create_engine(f'mssql+pyodbc://@{SERVER}/{DATABASE}?driver=SQL+Server&trusted_connection=yes')
        logger.info("Database connection established")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
            logger.info("Cursor closed")
        if self.conn:
            self.conn.close()
            logger.info("Connection closed")

    def query_data(self, sql_query):
        logger.info(f"Executing query: {sql_query}")
        return pd.read_sql(sql_query, self.engine)

    def update_guru(self, update_dict: dict):
        sql_update_guru = f'''
            UPDATE guru SET
                nama_guru = ?,
                email_guru = ?,
                phone_number = ?
            WHERE id_guru = ?
        '''
        values = (
            update_dict['nama_guru'],
            update_dict['email_guru'],
            update_dict['phone_number'],
            update_dict['id_guru']
        )
        try:
            logger.info(f"Updating table guru for id_guru {update_dict['id_guru']}")
            self.cursor.execute(sql_update_guru, values)
            self.conn.commit()
            logger.info("Update commited successfully.")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error updating table: {e}")

    def update_table_offsprings(self, table_name:str, update_dict: dict):
        sql_update = f'''
            UPDATE {table_name} SET
                full_name = ?,
                kad_pengenalan = ?,
                sijil_kelahiran = ?,
                email_school_work = ?,
                email_personal = ?,
                phone_number = ?,
                id_cat = ?
            WHERE id_person = ?
        '''
        values = (
            update_dict['full_name'],
            update_dict['kad_pengenalan'],
            update_dict['sijil_kelahiran'],
            update_dict['email_school_work'],
            update_dict['email_personal'],
            update_dict['phone_number'],
            update_dict['id_cat'],
            update_dict['id_person']  # used in WHERE clause
        )

        try:
            logger.info(f"Updating table {table_name} for id_person {update_dict['id_person']}")
            self.cursor.execute(sql_update, values)
            self.conn.commit()
            logger.info("Update committed successfully")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error updating table: {e}")

    def insert_into_table(self, table_name: str, df: pd.DataFrame):
        # Identify auto-increment ID column based on table
        id_column = 'id_' + table_name  # e.g., id_guru, id_sekolah

        if id_column in df.columns:
            df = df.drop(columns=[id_column])

        columns = ', '.join(df.columns)
        placeholder = ', '.join('?' * len(df.columns))
        columns_check = ' AND '.join([f"{col}=?" for col in df.columns])

        sql_check = f'''
            SELECT COUNT(*)
            FROM {table_name}
            WHERE {columns_check}
        '''
        sql_insert = f'''
            INSERT INTO {table_name} ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone()[0] > 0
                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f"Insert data {tuple(row)} into {table_name}: Success!")
                else:
                    logger.info(f"Data {tuple(row)}: Exists!")
                    any_exists = True
                    return any_exists
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f"Insert Error: {e}")

    def insert_into_peperiksaan(self, df:pd.DataFrame):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?'*len(df.columns))
        columns_check = ' AND '.join([f'{col}=?' for col in df.columns])
        sql_check = f'''
            SELECT COUNT(*)
            FROM peperiksaan
            WHERE {columns_check}  
        '''
        sql_insert = f'''
            INSERT INTO peperiksaan ({columns}) VALUES ({placeholder})
         '''
        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone() [0] > 0

                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f"Insert data {tuple(row)} into peperiksaan: success!")
                else:
                    logger.info(f"Data {tuple(row)}: Exists")
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f"Insert Error: {e}")

    def insert_into_guru(self, df:pd.DataFrame):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?'*len(df.columns))
        columns_check = ' AND '.join([f'{col}=?' for col in df.columns])
        sql_check = f'''
            SELECT COUNT(*)
            FROM guru
            WHERE {columns_check}
        '''
        sql_insert = f'''
            INSERT INTO guru ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone() [0] > 0
                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f"Insert data {tuple(row)} into guru: Success!")
                else:
                    logger.info(f"Data {tuple(row)}: Exists")
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f"Insert Error: {e}")

    def insert_keputusan_matapelajaran(self, df: pd.DataFrame):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?'*len(df.columns))
        columns_check = ' AND '.join([f'{col}=?' for col in df.columns])
        sql_check = f'''
            SELECT COUNT(*)
            FROM keputusan_peperiksaan
            WHERE {columns_check}   
        '''
        sql_insert = f'''
            INSERT INTO keputusan_peperiksaan ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone() [0] > 0
                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f'Insert data {tuple(row)} into keputusan_peperiksaan: Success!')
                else:
                    logger.info(f"Data {tuple(row)}: Exists")
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f'Insert Error: {e}')

    def update_kelas(self, update_kelas: dict):

        sql_update_kelas = '''
            UPDATE kelas SET
                id_cat_kelas = ?,
                id_guru = ?,
                nama_kelas = ?,
                id_sekolah = ?
            WHERE id_kelas = ?           
        '''

        values = (
            update_kelas['id_cat_kelas'],
            update_kelas['id_guru'],
            update_kelas['nama_kelas'],
            update_kelas['id_sekolah'],
            update_kelas['id_kelas']
        )

        try:
            logger.info(f"Updating table kelas for id_kelas {update_kelas['id_kelas']}")
            self.cursor.execute(sql_update_kelas, values)
            self.conn.commit()
            logger.info("Update committed successfully")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error updating table: {e}")

    def delete_data(self, table_name: str, id: int, key: str):
        sql_delete = f'''
            DELETE FROM {table_name}
            WHERE {key} = ?
        '''

        try:
            self.cursor.execute(sql_delete, (id,))
            self.conn.commit()
            logger.info(f'Delete successfully for id {id}.')
        except Exception as e:
            self.conn.rollback()
            logger.error(f'Fail to delete: {e}')

    def delete_subjek_peperiksaan(self, id_peperiksaan, id_subjek_peperiksaan):
        sql_delete_subjek_peperiksaan = """
                DELETE FROM subjek_peperiksaan
                WHERE id_peperiksaan = ?
                AND id_subjek_peperiksaan = ?  
            """
        values = (id_peperiksaan, id_subjek_peperiksaan)
        try:
            self.cursor.execute(sql_delete_subjek_peperiksaan, values)
            self.conn.commit()
            logger.info(f"Delete success {id_subjek_peperiksaan}")
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Delete failed: {e}")
            return False

    def update_sekolah(self, update_sekolah: dict):

        sql_update_sekolah = '''
            UPDATE sekolah SET
                nama_sekolah = ?,
                alamat_sekolah_line1 = ?,
                alamat_sekolah_line2 = ?,
                alamat_sekolah_line3 = ?,
                telefon_sekolah = ?
            WHERE id_sekolah = ?      
        '''

        values = (
            update_sekolah['nama_sekolah'],
            update_sekolah['alamat_sekolah_line1'],
            update_sekolah['alamat_sekolah_line2'],
            update_sekolah['alamat_sekolah_line3'],
            update_sekolah['telefon_sekolah'],
            update_sekolah['id_sekolah']
        )

        try:
            logger.info(f"Updating table sekolah for id_sekolah {update_sekolah['id_sekolah']}")
            self.cursor.execute(sql_update_sekolah, values)
            self.conn.commit()
            logger.info("Update committed successfully")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error updating table: {e}")

    def update_persekolahan(self, update_persekolahan: dict, id: int):
        sql_update_persekolahan = f'''
            UPDATE persekolahan SET
                id_person = ?,
                id_kelas = ?,
                tahun_persekolahan = ?
            WHERE id_persekolahan = ?
        '''

        values = (
            update_persekolahan['id_person'],
            update_persekolahan['id_kelas'],
            update_persekolahan['tahun_persekolahan'],
            id
        )
        try:
            logger.info(f'Updating table persekolahan for id_persekolahan: {id}')
            self.cursor.execute(sql_update_persekolahan, values)
            self.conn.commit()
            logger.info('Update committed successfully.')
        except Exception as e:
            self.conn.rollback()
            logger.error(f'Error updating table: {e}')

    def update_table_peperiksaan(self, update: dict):
        sql_update_peperiksaan = '''
            UPDATE peperiksaan 
            SET nama_peperiksaan = ?,
                tahun_peperiksaan = ?,
                tarikh_peperiksaan = ?
            WHERE id_peperiksaan = ?
        '''

        values = (
            update['nama_peperiksaan'],
            update['tahun_peperiksaan'],
            update['tarikh_peperiksaan'],
            update['id_peperiksaan']
        )
        try:
            logger.info(f"Updating table peperiksaan for id_peperiksaan: {update['id_peperiksaan']}")
            self.cursor.execute(sql_update_peperiksaan, values)
            self.conn.commit()
            logger.info(f"Table update successfully.")
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Error updating table peperiksaan: {e}")

    def update_keputusan(self, update: dict):
        sql_update_keputusan = '''
            UPDATE keputusan_peperiksaan
            SET markah = ?, 
                gred = ?, 
                tahap_penguasaan = ?
            WHERE id_peperiksaan= ? AND id_keputusan_peperiksaan = ? 
        '''
        values = (
            update['markah'],
            update['gred'],
            update['tahap_penguasaan'],
            update['id_peperiksaan'],
            update['id_keputusan_peperiksaan']
        )

        try:
            logger.info(f"Updating keputusan, id = {update['id_keputusan_peperiksaan']}")
            self.cursor.execute(sql_update_keputusan, values)
            self.conn.commit()
            logger.info("update successfully.")
            return True

        except Exception as e:
            self.conn.rollback()
            logger.warning(f'Update keputusan id: {update['id_keputusan_peperiksaan']} failed. error: {e}')
            return False


    def query_offsprings(self, sql_query, values: dict):
        try:
            self.cursor.execute(sql_query, tuple(values.values()))  # SQL Server ODBC expects tuple/list for params
            data = self.cursor.fetchall()  # fetch all rows after executing
            return data
        except Exception as e:
            logger.error(f"query failed: {sql_query, values} \n{e}")
            return None

    def insert_subjek_peperiksaan(self, df: pd.DataFrame):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?'*len(df.columns))
        columns_check = ' AND '.join([f'{col}=?' for col in df.columns])
        sql_check = f'''
            SELECT COUNT(*)
            FROM subjek_peperiksaan
            WHERE {columns_check}   
        '''
        sql_insert = f'''
            INSERT INTO subjek_peperiksaan ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone() [0] > 0
                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f'Insert data {tuple(row)} into table subjek_peperiksaan: Success!')
                else:
                    logger.info(f"Data {tuple(row)}: Exists")
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f'Insert Error: {e}')

    def insert_result_exam(self, result: pd.DataFrame):
        columns = ', '.join(result.columns)
        placeholder = ', '.join('?'*len(result.columns))
        columns_check = ' AND '.join([f'{col}=?' for col in result.columns])
        sql_check = f"""
                SELECT COUNT(*)
                FROM keputusan_peperiksaan
                WHERE {columns_check}  
            """
        sql_result_insert = f"""
                INSERT INTO keputusan_peperiksaan ({columns}) VALUES ({placeholder})
            """

        try:
            for index, row in result.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone() [0] > 0
                if not exists:
                    self.cursor.execute(sql_result_insert, tuple(row))
                    self.conn.commit()

                    logger.info(f"Insert data {tuple(row)} into table keputusan_peperiksaan: success!")
                    return True
                else:
                    logger.info(f"Data {tuple(row)}: Exists.")
                    return False
        except Exception as e:
            self.conn.rollback()
            logger.error(f"Insert error: {e}")
            return False

    def query_one(self, query, params=None):
        cursor = self.conn.cursor()
        cursor.execute(query, params or [])
        row = cursor.fetchone()
        if row:
            columns = [column[0] for column in cursor.description]
            return dict(zip(columns, row))
        return None

    def get_exam_result_by_ids(self, id_peperiksaan, id_subjek_peperiksaan):
        query = """
            SELECT *
            FROM vw_keputusan_peperiksaan
            WHERE id_peperiksaan = ? AND id_subjek_peperiksaan = ?
        """
        return self.query_one(query, (id_peperiksaan, id_subjek_peperiksaan))

    def get_exam_result_by_ids1(self, id_peperiksaan, id_keputusan_peperiksaan):
        query = """
            SELECT *
            FROM vw_keputusan_peperiksaan
            WHERE id_peperiksaan = ? AND id_subjek_peperiksaan = ?
        """
        return self.query_one(query, (id_peperiksaan, id_keputusan_peperiksaan))

    def delete_exam_result(self, id_peperiksaan, id_keputusan_peperiksaan):
        sql_delete = """
            DELETE FROM keputusan_peperiksaan
            WHERE id_peperiksaan = ? 
            AND id_keputusan_peperiksaan = ?
        """

        try:
            self.cursor.execute(sql_delete, (id_peperiksaan, id_keputusan_peperiksaan))
            self.conn.commit()
            logger.info(f'Delete successfully for id {id_keputusan_peperiksaan}.')
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(f'Fail to delete: {e}')
            return False

    def insert_into_comment(self, df: pd.DataFrame):
        columns = ', '.join(df.columns)
        placeholder = ', '.join('?' * len(df.columns))
        columns_check = ' AND '.join([f"{col}=?" for col in df.columns])

        sql_check = f'''
            SELECT COUNT(*)
            FROM komen_keputusan
            WHERE {columns_check}
        '''
        sql_insert = f'''
            INSERT INTO komen_keputusan ({columns}) VALUES ({placeholder})
        '''

        try:
            for index, row in df.iterrows():
                self.cursor.execute(sql_check, tuple(row))
                exists = self.cursor.fetchone()[0] > 0
                if not exists:
                    self.cursor.execute(sql_insert, tuple(row))
                    self.conn.commit()
                    logger.info(f"Insert data {tuple(row)} into komen_keputusan: Success!")
                    return True
                else:
                    logger.info(f"Data {tuple(row)}: Exists!")
                    return False
        except pyodbc.Error as e:
            self.conn.rollback()
            logger.error(f"Insert Error: {e}")
            return False

    def update_komen(self, update: dict):
        update = f"""
            UPDATE komen_keputusan
            SET komen_oleh = ?,
                komen = ?
            WHERE id_komen = ?
            AND id_peperiksaan = ?    
        """

        values = (
            update['komen_oleh'],
            update['komen'],
            update['id_komen'],
            update['id_peperiksaan']
        )
        try:
            logger.info(f"Updating komen id: {update['id_komen']}")
            self.cursor.execute(update, values)
            self.conn.commit()
            logger.info(f"Update komen, success")
            return True

        except Exception as e:
            self.conn.rollback()
            logger.warning(f'Update komen id: {update['id_komen']} failed. error: {e}')
            return False

    def update_id_jadual_subjek_peperiksaan(self, update:dict):
        update_subjek_peperiksaan = f"""
            UPDATE subjek_peperiksaan
            SET id_jadual = ?
            WHERE id_peperiksaan = ?
            AND id_subjek_peperiksaan = ?    
        """
        values = (
            update['id_jadual'],
            update['id_peperiksaan'],
            update['id_subjek_peperiksaan']
        )
        try:
            logger.info(f"Insert id_jadual {update['id_jadual']} into subjek peperiksaan table {update['id_subjek_peperiksaan']}")
            self.cursor.execute(update_subjek_peperiksaan, values)
            self.conn.commit()
            logger.info(f"Inserted id_jadual {update['id_jadual']} into subjek peperiksaan table {update['id_subjek_peperiksaan']}" )
            return True
        except Exception as e:
            logger.warning(f"FAILED: updating id_jadual {update['id_jadual']} into subjek peperiksaan table, error: {e}")
            self.conn.rollback()
            return False

    def update_jadual(self, update:dict):
        update_sql = """
            UPDATE jadual_peperiksaan
            SET tarikh = ?,
                mula = ?,
                tamat = ?
            WHERE id_jadual = ?   
        """

        values = (
            update['tarikh'],
            update['mula'],
            update['tamat'],
            update['id_jadual']
        )

        try:
            logger.info(f"Updating jadual: {update['id_jadual']}")
            self.cursor.execute(update_sql, values)
            self.conn.commit()
            logger.info(f"Update jadual, success: {update['id_jadual']}")
            return True
        except Exception as e:
            logger.warning(f"Updating failed: {e}")
            return False

