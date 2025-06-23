import pandas as pd

from OffSprings_DB import sql_offsprings

with sql_offsprings() as db:
    sql_summary_keputusan = """
                        SELECT a.id_peperiksaan, a.nama_peperiksaan, a.tarikh_peperiksaan, e.full_name, f.nama_kelas, SUM(c.markah) AS total_score, AVG(c.markah) AS average_score, COUNT(b.id_subjek_peperiksaan) as total_subjects
                        FROM peperiksaan a
                        LEFT JOIN subjek_peperiksaan b
                        ON a.id_peperiksaan = b.id_peperiksaan
                        LEFT JOIN keputusan_peperiksaan c
                        ON b.id_subjek_peperiksaan = c.id_subjek_peperiksaan
                        LEFT JOIN persekolahan d
                        ON a.id_persekolahan = d.id_persekolahan
                        LEFT JOIN person e
                        ON d.id_person = e.id_person
                        LEFT JOIN kelas f
                        ON d.id_kelas = f.id_kelas
                        GROUP BY a.id_peperiksaan, a.nama_peperiksaan, a.tarikh_peperiksaan, e.full_name, f.nama_kelas
                    """
    data_summary_peperiksaan = db.query_data(sql_summary_keputusan)
    data_summary_peperiksaan = data_summary_peperiksaan.fillna(0.00)
    print(data_summary_peperiksaan)
