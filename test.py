from OffSprings_DB import sql_offsprings
id = 20012
with sql_offsprings() as db:
    sql_persekolahan = f"SELECT id_persekolahan FROM keputusan_peperiksaan WHERE id_peperiksaan = {id}"
    id_persekolahan = db.query_data(sql_query=sql_persekolahan)
    id_persekolahan = id_persekolahan.loc[0,'id_persekolahan']

    print(id_persekolahan)
