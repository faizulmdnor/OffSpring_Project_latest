from OffSprings_DB import sql_offsprings
id_person = 101011
id_kelas = 255
with sql_offsprings() as db:
    sql_persekolahan = '''
        SELECT id_persekolahan
        FROM persekolahan
        WHERE id_person = ?
        AND id_kelas  = ?
    '''

    values = {
        'id_person': id_person,
        'id_kelas': id_kelas
    }
    result = db.query_offsprings(sql_query=sql_persekolahan, values=values)
    if result:
        id_persekolahan = result[0][0]
        print(id_persekolahan)
    else:
        print("No data found")

