import logging
import os
import random
import pyodbc
from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
from datetime import datetime
from OffSprings_DB import sql_offsprings
from dateutil.relativedelta import relativedelta
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "your_secret_key"


@app.route('/')
def index():
    with sql_offsprings() as db:
        try:
            data = db.query_data("SELECT * FROM vw_offsprings_details")

            # Pastikan 'birth_date' dalam format datetime
            data['birth_date'] = pd.to_datetime(data['birth_date'], errors='coerce')

            today = pd.to_datetime("today")
            # Format umur sebagai "X tahun Y bulan"
            data['umur'] = data['birth_date'].apply(
                lambda x: f"{relativedelta(today, x).years} tahun {relativedelta(today, x).months} bulan"
                if pd.notnull(x) else "-"
            )
            return render_template('index.html', data=data.to_dict(orient='records'))
        except Exception as e:
            return f"Error retrieving data: {e}"

@app.route('/persekolahan', methods=['GET', "POST"])
def persekolahan():
    with sql_offsprings() as db:
        if request.method == 'POST':
            tahun_persekolahan = request.form['tahun_persekolahan']
            id_person = request.form['id_person']
            id_kelas = request.form['id_kelas']

            persekolahan_update = {
                'id_person': id_person,
                'id_kelas': id_kelas,
                'tahun_persekolahan': tahun_persekolahan
            }

            df_persekolahan = pd.DataFrame([persekolahan_update])

            db.insert_into_table(table_name='persekolahan', df=df_persekolahan)

        sql_persekolahan = 'SELECT * FROM vw_persekolahan'
        data_persekolahan = db.query_data(sql_persekolahan)
        sql_persons = 'SELECT * FROM person'
        persons = db.query_data(sql_persons)
        sql_kelas = 'SELECT * FROM kelas'
        data_kelas = db.query_data(sql_kelas)

        return render_template('persekolahan.html',
                               data_persekolahan=data_persekolahan.to_dict(orient='records'),
                               persons=persons.to_dict(orient='records'),
                               data_kelas=data_kelas.to_dict(orient='records')
                               )

@app.route('/tambah_sekolah', methods=['GET', 'POST'])
def insert_sekolah():
    with sql_offsprings() as db:
        data_sekolah = {
            'nama_sekolah': '',
            'alamat_sekolah_line1': '',
            'alamat_sekolah_line2': '',
            'alamat_sekolah_line3': '',
            'telefon_sekolah': ''
        }

        if request.method == "POST":
            data_sekolah['nama_sekolah'] = request.form['nama_sekolah']
            data_sekolah['alamat_sekolah_line1'] = request.form['alamat_sekolah_line1']
            data_sekolah['alamat_sekolah_line2'] = request.form['alamat_sekolah_line2']
            data_sekolah['alamat_sekolah_line3'] = request.form['alamat_sekolah_line3']
            data_sekolah['telefon_sekolah'] = request.form['telefon_sekolah']

            df_sekolah = pd.DataFrame([data_sekolah])
            db.insert_into_table(table_name='sekolah', df=df_sekolah)

        # Query latest data to display
        query_sekolah = "SELECT * FROM sekolah"
        inserted_sekolah = db.query_data(query_sekolah)

        return render_template(
            'tambah_sekolah.html',
            data=data_sekolah,
            inserted_sekolah=inserted_sekolah.to_dict(orient='records')
        )


@app.route('/tambah_guru', methods=['GET', 'POST'])
def insert_guru():
    with sql_offsprings() as db:
        data_guru = {
            'id_guru': '',
            'nama_guru': '',
            'email_guru': '',
            'phone_number': ''
        }

        if request.method == "POST":
            data_guru['nama_guru'] = request.form['nama_guru']
            data_guru['email_guru'] = request.form['email_guru']
            data_guru['phone_number'] = request.form['phone_number']

            df_guru = pd.DataFrame([data_guru])
            db.insert_into_table(table_name='guru', df=df_guru)

        # Query latest data to display
        query_guru = "SELECT * FROM guru"
        inserted_guru = db.query_data(query_guru)

        return render_template(
            'tambah_guru.html',
            data=data_guru,
            inserted_guru=inserted_guru.to_dict(orient='records')
        )


@app.route('/tambah_kelas', methods=['GET', 'POST'])
def insert_kelas():
    with sql_offsprings() as db:
        data_kelas = {
            'id_cat_kelas': '',
            'nama_kelas': '',
            'id_guru': '',
            'id_sekolah': ''
        }

        if request.method == "POST":
            data_kelas['id_cat_kelas'] = request.form['id_cat_kelas']
            data_kelas['nama_kelas'] = request.form['nama_kelas']
            data_kelas['id_guru'] = request.form['id_guru']
            data_kelas['id_sekolah'] = request.form['id_sekolah']

            df_kelas = pd.DataFrame([data_kelas])
            db.insert_into_table(table_name='kelas', df=df_kelas)

        # Query latest data to display
        query_cat_kelas = "SELECT * FROM cat_kelas"
        cat_kelas = db.query_data(query_cat_kelas)

        query_sekolah = "SELECT * FROM sekolah"
        data_sekolah = db.query_data(query_sekolah)

        query_kelas = "SELECT * FROM vw_kelas"
        inserted_kelas = db.query_data(query_kelas)

        query_guru = "SELECT * FROM guru"
        data_guru = db.query_data(query_guru)

        return render_template(
            'tambah_kelas.html',
            data=data_kelas,
            inserted_kelas=inserted_kelas.to_dict(orient='records'),
            cat_kelas=cat_kelas.to_dict(orient='records'),
            data_sekolah=data_sekolah.to_dict(orient='records'),
            data_guru=data_guru.to_dict(orient='records')
        )


@app.route('/edit_guru/<id>', methods=['GET', 'POST'])
def edit_guru(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_guru = request.form['id_guru']
            nama_guru = request.form['nama_guru']
            email_guru = request.form['email_guru']
            phone_number = request.form['phone_number']

            update_guru = {
                'id_guru': id_guru,
                'nama_guru': nama_guru,
                'email_guru': email_guru,
                'phone_number': phone_number
            }
            db.update_guru(update_dict=update_guru)
            return redirect(url_for('insert_guru'))
        query = f"SELECT * FROM guru WHERE id_guru = {id}"

        data = db.query_data(query)
        if data.empty:
            return "Data not found:", 404

        return render_template('edit_guru.html',
                               data=data.iloc[0].to_dict())


@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_offsprings(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_person = request.form['id_person']
            full_name = request.form['full_name']
            kad_pengenalan = request.form['kad_pengenalan']
            sijil_kelahiran = request.form['sijil_kelahiran']
            gender = request.form['gender']
            email_school_work = request.form['email_school_work']
            email_personal = request.form['email_personal']
            phone_number = request.form['phone_number']
            id_cat = request.form['id_cat']

            update_data = {
                'id_person': id_person,
                'full_name': full_name,
                'kad_pengenalan': kad_pengenalan,
                'sijil_kelahiran': sijil_kelahiran,
                'gender': gender,
                'email_school_work': email_school_work,
                'email_personal': email_personal,
                'phone_number': phone_number,
                'id_cat': id_cat
            }
            table_name = 'person'
            db.update_table_offsprings(table_name=table_name, update_dict=update_data)

            return redirect(url_for('index'))

        query = f"SELECT * FROM vw_offsprings_details WHERE id_person = '{id}'"
        data = db.query_data(query)
        if data.empty:
            return "Data not found", 404
        sql_kategori = f'select id_cat, category from category'
        kategori = db.query_data(sql_kategori)

        return render_template('edit_offsprings.html',
                               data=data.iloc[0].to_dict(),
                               kategori=kategori.to_dict(orient='records')
                               )


@app.route('/edit_kelas/<id>', methods=['GET', 'POST'])
def edit_kelas(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_kelas = request.form['id_kelas']
            id_cat_kelas = request.form['id_cat_kelas']
            id_guru = request.form['id_guru']
            nama_kelas = request.form['nama_kelas']
            id_sekolah = request.form['id_sekolah']

            update_kelas = {
                'id_kelas': id_kelas,
                'id_cat_kelas': id_cat_kelas,
                'id_guru': id_guru,
                'nama_kelas': nama_kelas,
                'id_sekolah': id_sekolah
            }
            db.update_kelas(update_kelas)

            return redirect(url_for('insert_kelas'))

        query = f"SELECT * FROM kelas WHERE id_kelas = {id}"
        data = db.query_data(query)
        query_kelas = 'SELECT * FROM cat_kelas'
        cat_kelas = db.query_data(query_kelas)
        query_guru = 'SELECT * FROM guru'
        guru = db.query_data(query_guru)
        query_sekolah = 'SELECT * FROM sekolah'
        sekolah = db.query_data(query_sekolah)

        if data.empty:
            return "Data not found", 404

        return render_template('edit_kelas.html',
                               data=data.iloc[0].to_dict(),
                               cat_kelas=cat_kelas.to_dict(orient='records'),
                               guru=guru.to_dict(orient='records'),
                               sekolah=sekolah.to_dict(orient='records')
                               )


@app.route('/delete_kelas/<id>', methods=['POST'])
def delete_kelas(id):
    with sql_offsprings() as db:
        db.delete_data(table_name='kelas', id=id, key='id_kelas')

    return redirect(url_for('insert_kelas'))


@app.route('/edit_sekolah/<id>', methods=['GET', 'POST'])
def edit_sekolah(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_sekolah = request.form['id_sekolah']
            nama_sekolah = request.form['nama_sekolah']
            alamat_sekolah_line1 = request.form['alamat_sekolah_line1']
            alamat_sekolah_line2 = request.form['alamat_sekolah_line2']
            alamat_sekolah_line3 = request.form['alamat_sekolah_line3']
            telefon_sekolah = request.form['telefon_sekolah']

            update_sekolah = {
                'id_sekolah': id_sekolah,
                'nama_sekolah': nama_sekolah,
                'alamat_sekolah_line1': alamat_sekolah_line1,
                'alamat_sekolah_line2': alamat_sekolah_line2,
                'alamat_sekolah_line3': alamat_sekolah_line3,
                'telefon_sekolah': telefon_sekolah
            }
            db.update_sekolah(update_sekolah)
            return redirect(url_for('insert_sekolah'))

        query = f'SELECT * FROM sekolah WHERE id_sekolah = {id}'
        data = db.query_data(query)

        if data.empty:
            return "Data not found", 404

        return render_template('edit_sekolah.html', data=data.iloc[0].to_dict())


@app.route('/delete_sekolah/<id>', methods=['POST'])
def delete_sekolah(id):
    with sql_offsprings() as db:
        db.delete_data(table_name='sekolah', id=id, key='id_sekolah')

    return redirect(url_for('insert_sekolah'))


@app.route('/delete_guru/<id>', methods=['POST'])
def delete_guru(id):
    with sql_offsprings() as db:
        db.delete_data(table_name='guru', id=id, key='id_guru')

    return redirect(url_for('insert_guru'))


@app.route('/edit_persekolahan/<id>', methods=['GET', 'POST'])
def edit_persekolahan(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_person = request.form['id_person']
            id_kelas = request.form['id_kelas']
            tahun_persekolahan = request.form['tahun_persekolahan']

            update_persekolahan = {
                'id_person': id_person,
                'id_kelas': id_kelas,
                'tahun_persekolahan': tahun_persekolahan
            }

            db.update_persekolahan(update_persekolahan, id)
            return redirect(url_for('persekolahan'))

        query = f'''
            SELECT p.id_persekolahan, o.id_person, k.id_kelas, p.tahun_persekolahan, o.full_name, k.nama_kelas
            FROM persekolahan p
            LEFT JOIN person o
            ON p.id_person = o.id_person
            LEFT JOIN kelas k
            ON p.id_kelas = k.id_kelas
        
            WHERE p.id_persekolahan = {id}      
        '''
        data = db.query_data(query)
        sql_persons = 'SELECT * FROM person'
        persons = db.query_data(sql_persons)
        sql_data_kelas = 'SELECT * FROM kelas'
        data_kelas = db.query_data(sql_data_kelas)

        record = data.iloc[0].to_dict()

        if data.empty:
            return "Data not found", 404

        return render_template('edit_persekolahan.html',
                               data=record,
                               persons=persons.to_dict(orient='records'),
                               data_kelas=data_kelas.to_dict(orient='records')
                               )


@app.route('/delete_persekolahan/<id>', methods=['POST'])
def delete_persekolahan(id):
    with sql_offsprings() as db:
        db.delete_data(table_name='persekolahan', id=id, key='id_persekolahan')
    return redirect(url_for('persekolahan'))


@app.route('/peperiksaan', methods=['GET', 'POST'])
def peperiksaan():
    cari = []
    with sql_offsprings() as db:
        if request.method == "POST":
            full_name = request.form['nama']
            kelas = request.form['kelas']

            cari_sql = f"""
                    SELECT a.id_peperiksaan, e.full_name, f.nama_kelas, g.nama_sekolah, a.nama_peperiksaan, a.tarikh_peperiksaan
                    FROM peperiksaan a
                    LEFT JOIN persekolahan d
                    ON a.id_persekolahan = d.id_persekolahan
                    LEFT JOIN person e
                    ON d.id_person = e.id_person
                    LEFT JOIN kelas f
                    ON d.id_kelas = f.id_kelas
                    LEFT JOIN sekolah g
                    ON f.id_sekolah = g.id_sekolah
                    WHERE e.full_name like '%{full_name}%'
                    AND f.nama_kelas = '{kelas}'
            """
            df_cari = db.query_data(cari_sql)
            cari = df_cari.to_dict(orient='records')

        sql_data_peperiksaan = f"""
                    SELECT a.id_peperiksaan, e.full_name, f.nama_kelas, g.nama_sekolah, a.nama_peperiksaan, a.tarikh_peperiksaan
                    FROM peperiksaan a
                    LEFT JOIN persekolahan d
                    ON a.id_persekolahan = d.id_persekolahan
                    LEFT JOIN person e
                    ON d.id_person = e.id_person
                    LEFT JOIN kelas f
                    ON d.id_kelas = f.id_kelas
                    LEFT JOIN sekolah g
                    ON f.id_sekolah = g.id_sekolah
                """
        data_peperiksaan = db.query_data(sql_data_peperiksaan)

        return render_template('peperiksaan.html',
                               data_peperiksaan=data_peperiksaan.to_dict(orient="records"),
                               cari=cari)

@app.route('/add_subject', methods=['GET', 'POST'])
def add_subject():
    with sql_offsprings() as db:
        if request.method == 'POST':
            nama_subjek = request.form.get('subject', '').strip()
            if not nama_subjek:
                flash("Field 'Matapelajaran' cannot be empty.", "danger")
                return redirect(url_for('add_subject'))

            # Insert new subject into the database
            data = {'nama_subjek': nama_subjek}
            df = pd.DataFrame([data])
            exists = db.insert_into_table(table_name='subjek', df=df)

            if exists:
                flash(f"Matapelajaran '{nama_subjek}' telah wujud!", "warning")
            else:
                flash(f"Matapelajaran '{nama_subjek}' berjaya ditambah.", "success")

        query_subject = 'SELECT * FROM subjek'
        subjects = db.query_data(query_subject)
        return render_template('add_subject.html',
                               subjects=subjects.to_dict(orient='records'))


@app.route('/add_peperiksaan', methods=['GET', 'POST'])
def add_peperiksaan():
    with sql_offsprings() as db:
        if request.method == 'POST':
            nama_peperiksaan = request.form['nama_peperiksaan'].strip()
            tahun_peperiksaan = request.form['tahun_peperiksaan'].strip()
            tarikh_peperiksaan = request.form['tarikh_peperiksaan'].strip()
            id_persekolahan = request.form['id_persekolahan'].strip()

            if not nama_peperiksaan or not tahun_peperiksaan or not tarikh_peperiksaan:
                flash("Please fill all fields.", "danger")
                return redirect(url_for('add_peperiksaan'))

            try:
                # Ensure date format is correct
                tarikh_peperiksaan = datetime.strptime(tarikh_peperiksaan, '%Y-%m-%d').strftime('%Y-%m-%d')
                update_peperiksaan = {
                    'nama_peperiksaan': nama_peperiksaan,
                    'tahun_peperiksaan': tahun_peperiksaan,
                    'tarikh_peperiksaan': tarikh_peperiksaan,
                    'id_persekolahan': id_persekolahan
                }
                df_peperiksaan = pd.DataFrame([update_peperiksaan])
                db.insert_into_peperiksaan(df=df_peperiksaan)
                flash(f"Peperiksaan '{nama_peperiksaan}' added successfully.", "success")

            except ValueError:
                flash("Invalid date format. Please use YYYY-MM-DD.", "danger")
                return redirect(url_for('add_peperiksaan'))
        query_peperiksaan = """
                                SELECT a.id_peperiksaan, a.nama_peperiksaan, a.tarikh_peperiksaan, a.tahun_peperiksaan, c.full_name, d.nama_kelas, e.nama_sekolah
                                FROM peperiksaan a
                                LEFT JOIN persekolahan b
                                ON a.id_persekolahan = b.id_persekolahan
                                LEFT JOIN person c
                                ON b.id_person = c.id_person
                                LEFT JOIN kelas d
                                ON b.id_kelas = d.id_kelas
                                LEFT JOIN sekolah e
                                ON d.id_sekolah = e.id_sekolah
                            """
        data_exam = db.query_data(query_peperiksaan)

        sql_details_person = """select a.id_persekolahan, a.tahun_persekolahan, b.full_name, c.nama_kelas, d.nama_sekolah
                            from persekolahan a
                            LEFT JOIN person b
                            ON a.id_person = b.id_person
                            LEFT JOIN kelas c
                            ON a.id_kelas = c.id_kelas
                            LEFT JOIN sekolah d
                            ON d.id_sekolah = c.id_sekolah
                        """
        details_person = db.query_data(sql_details_person)

        return render_template('add_peperiksaan.html',
                               exams=data_exam.to_dict(orient='records'),
                               details_person=details_person.to_dict(orient="records"))


@app.route('/edit_peperiksaan/<int:id>', methods=['GET', 'POST'])
def edit_peperiksaan(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            nama_peperiksaan = request.form['nama_peperiksaan'].strip()
            tahun_peperiksaan = request.form['tahun_peperiksaan'].strip()
            tarikh_peperiksaan = request.form['tarikh_peperiksaan'].strip()
            tarikh_peperiksaan = datetime.strptime(tarikh_peperiksaan, '%Y-%m-%d').strftime('%Y-%m-%d')
            update_peperiksaan = {
                'nama_peperiksaan': nama_peperiksaan,
                'tahun_peperiksaan': tahun_peperiksaan,
                'tarikh_peperiksaan': tarikh_peperiksaan,
                'id_peperiksaan': id
            }
            db.update_table_peperiksaan(update_peperiksaan)
            return redirect(url_for('add_peperiksaan'))

        sql_data_peperiksaan = f"""SELECT a.*, b.full_name, b.nama_kelas, b.nama_sekolah
                                    FROM peperiksaan a
                                    LEFT JOIN vw_persekolahan b
                                    ON a.id_persekolahan = b.id_persekolahan
                                    WHERE id_peperiksaan = {id}
                                """
        data_peperiksaan = db.query_data(sql_data_peperiksaan)

        return render_template('edit_peperiksaan.html',
                               data=data_peperiksaan.to_dict(orient='records')[0]
                               )

@app.route('/delete_peperiksaan/<id>', methods=['POST'])
def delete_peperiksaan(id):
    with sql_offsprings() as db:
        db.delete_data(table_name='peperiksaan', id=id, key='id_peperiksaan')
    return redirect(url_for('add_peperiksaan'))

@app.route('/view_results/<int:id_peperiksaan>', methods=['GET', 'POST'])
def view_results(id_peperiksaan):
    with sql_offsprings() as db:
        performance_query = f"""
                SELECT 
                    id_peperiksaan,
                    nama_peperiksaan,
                    COUNT(id_subjek_peperiksaan) AS Total_Subjek,
                    SUM(markah) AS Jumlah_Markah,
                    AVG(markah) AS Purata_Markah,
                    ROUND((SUM(markah) * 100.0) / (COUNT(id_subjek_peperiksaan) * 100), 2) AS Peratus
                FROM vw_keputusan_peperiksaan
                WHERE id_keputusan_peperiksaan IS NOT NULL
                AND id_peperiksaan = {id_peperiksaan}
                GROUP BY id_peperiksaan, nama_peperiksaan
            """
        performance_df = db.query_data(performance_query)

        performance = performance_df.to_dict(orient="records")
        analisa_query = f"""
                SELECT *
                FROM vw_analisa_keputusan
                WHERE id_peperiksaan = {id_peperiksaan}  
                """
        analisa_df = db.query_data(analisa_query)
        analisa = analisa_df.to_dict(orient="records")

        sql_keputusan_peperiksaan = f"""
            SELECT * FROM vw_keputusan_peperiksaan
            WHERE id_peperiksaan = {id_peperiksaan} 
        """
        records = db.query_data(sql_keputusan_peperiksaan).to_dict(orient="records")
        for row in records:
            id_val, id_markah, id_tp = row.get('id_keputusan_peperiksaan'), row.get("markah"), row.get("tahap_penguasaan")
            if id_val is not None and not pd.isna(id_val):
                row["id_keputusan_peperiksaan"] = int(id_val)
                row["markah"] = int(id_markah)
                row["tahap_penguasaan"] = int(id_tp)
            else:
                row["id_keputusan_peperiksaan", "markah", "tahap_penguasaan"] = ""

        return render_template("view_results.html",
                               details=records,
                               data=performance,
                               analisa=analisa,
                               id_peperiksaan=id_peperiksaan)

@app.route('/daftar_subjek/<int:id_peperiksaan>', methods=['GET', 'POST'])
def daftar_subjek(id_peperiksaan):
    with sql_offsprings() as db:
        if request.method == "POST":
            id_peperiksaan = id_peperiksaan
            id_subjek_list = request.form.getlist('nama_subjek[]')

            for i in range(len(id_subjek_list)):
                update_subjek_peperiksaan = {
                    'id_peperiksaan':id_peperiksaan,
                    'id_subjek':id_subjek_list[i]
                }
                df_update_subjek_peperiksaan = pd.DataFrame([update_subjek_peperiksaan])
                try:
                    db.insert_subjek_peperiksaan(df_update_subjek_peperiksaan)
                    flash(f"Daftar subjek berjaya", "success")
                except Exception as e:
                    flash("Daftar subjek gagal", "danger")

            return redirect(url_for('daftar_subjek', id_peperiksaan=id_peperiksaan))

        sql_senarai_subjek = "SELECT id_subjek, nama_subjek FROM subjek"
        senarai_subjek = db.query_data(sql_senarai_subjek).to_dict(orient="records")

        sql_details = f"""SELECT * FROM vw_peperiksaan WHERE id_peperiksaan={id_peperiksaan}"""
        details = db.query_data(sql_details).to_dict(orient="records")

        sql_registered_subject = f"""
            SELECT * FROM vw_daftar_peperiksaan WHERE id_peperiksaan = {id_peperiksaan} 
        """

        registered_subject_list = db.query_data(sql_registered_subject)
        registered_subject_list['id_jadual'] = registered_subject_list['id_jadual'].fillna(0).astype(int)
        registered_subject_list = registered_subject_list.sort_values(by=['tarikh', 'mula'], na_position='last')

        if registered_subject_list.empty:
            flash("Tiada subjek didaftarkan.", "info")
            registered_subject_list = []



        return render_template("daftar_subjek.html",
                               senarai_subjek=senarai_subjek,
                               details=details,
                               subjects=registered_subject_list.to_dict(orient="records"))

@app.route('/delete_registered_subject/<int:id_peperiksaan>/<int:id_subjek_peperiksaan>', methods=["GET", "POST"])
def delete_registered_subject(id_peperiksaan, id_subjek_peperiksaan):
    with sql_offsprings() as db:
        subject_del = db.delete_subjek_peperiksaan(id_peperiksaan, id_subjek_peperiksaan)
        if subject_del:
            flash(f"id_subjek_peperiksaan: {id_subjek_peperiksaan} berjaya dipadam", "success")
        else:
            flash(f"id_subjek_peperiksaan: {id_subjek_peperiksaan} tidak berjaya dipadam", "danger")

        return redirect(url_for('daftar_subjek', id_peperiksaan=id_peperiksaan))

@app.route('/insert_exam_results/<int:id_peperiksaan>/<int:id_subjek_peperiksaan>', methods=["GET", "POST"])
def insert_exam_results(id_peperiksaan, id_subjek_peperiksaan):
    with sql_offsprings() as db:
        if request.method == "POST":
            update_result = {
                'id_peperiksaan': id_peperiksaan,
                'id_subjek_peperiksaan': id_subjek_peperiksaan,
                'markah': request.form['markah'].strip(),
                'gred': request.form['gred'].strip(),
                'tahap_penguasaan': request.form['tahap_penguasaan'].strip()
            }
            df_updated_result = pd.DataFrame([update_result])
            result_updated = db.insert_result_exam(df_updated_result)

            if result_updated:
                flash(f"id_subjek_peperiksaan: {id_subjek_peperiksaan} berjaya dimuatnaik", "success")
            else:
                flash(f"id_subjek_peperiksaan: {id_subjek_peperiksaan} tidak berjaya dimuatnaik", "danger")

            return redirect(url_for('view_results', id_peperiksaan=id_peperiksaan))
        else:
            details = db.get_exam_result_by_ids(id_peperiksaan, id_subjek_peperiksaan)
            if not details:
                flash("Maklumat tidak dijumpai.", "danger")
                return redirect(url_for('view_results', id_peperiksaan=id_peperiksaan))

            return render_template("insert_exam_results.html", details=details)

@app.route('/edit_exam_results/<int:id_peperiksaan>/<int:id_keputusan_peperiksaan>', methods=["GET", "POST"])
def edit_exam_results(id_peperiksaan, id_keputusan_peperiksaan):
    with sql_offsprings() as db:
        if request.method == "POST":
            update_results = {
                'markah': request.form['markah'].strip(),
                'gred':request.form['gred'].strip(),
                'tahap_penguasaan':request.form['tahap_penguasaan'].strip(),
                'id_peperiksaan':id_peperiksaan,
                'id_keputusan_peperiksaan':id_keputusan_peperiksaan
            }
            updated = db.update_keputusan(update_results)
            if updated:
                flash("Update success.", "success")
            else:
                flash("Update failed", "warning")
            return redirect(url_for('view_results', id_peperiksaan=id_peperiksaan))

        sql_keputusan_peperiksaan = f"""
                SELECT * FROM vw_keputusan_peperiksaan
                WHERE id_peperiksaan = {id_peperiksaan}
                AND id_keputusan_peperiksaan = {id_keputusan_peperiksaan}  
            """
        details = db.query_data(sql_keputusan_peperiksaan)
        return render_template("edit_exam_results.html",
                               details=details.to_dict(orient="records"))

@app.route('/delete_exam_result/<int:id_peperiksaan>/<int:id_keputusan_peperiksaan>', methods=["GET", "POST"])
def delete_exam_result(id_peperiksaan, id_keputusan_peperiksaan):
    with sql_offsprings() as db:

        if request.method == "POST":
            try:
                deleted = db.delete_exam_result(id_peperiksaan, id_keputusan_peperiksaan)
                if deleted:
                    flash(f"Successful delete ID Keputusan: {id_keputusan_peperiksaan}", "success")
                    logging.info(f"Successful delete ID Keputusan: {id_keputusan_peperiksaan}")
                else:
                    flash(f"Failed to delete ID Keputusan: {id_keputusan_peperiksaan}", "warning")
                    logging.info(f"Failed delete ID Keputusan: {id_keputusan_peperiksaan}")
            except Exception as e:
                logging.warning(f"Failed delete ID Keputusan: {id_keputusan_peperiksaan}: {e}")
            return redirect(url_for('view_results', id_peperiksaan=id_peperiksaan))

        sql_results_to_delete = f"""
            SELECT *
            FROM vw_keputusan_peperiksaan
            WHERE id_peperiksaan = {id_peperiksaan}
            AND id_keputusan_peperiksaan = {id_keputusan_peperiksaan}    
        """
        data = db.query_data(sql_results_to_delete)
        return render_template('delete_exam_result.html',
                                details=data.to_dict(orient="records"))

@app.route('/add_comments/<int:id_peperiksaan>', methods=['GET', 'POST'])
def add_comments(id_peperiksaan):
    with sql_offsprings() as db:
        if request.method == "POST":
            comment_to_insert = {
                'komen_oleh': request.form['komen_oleh'].strip(),
                'komen': request.form['komen'].strip(),
                'id_peperiksaan': id_peperiksaan
            }
            df_comment_insert = pd.DataFrame([comment_to_insert])
            comment_inserted = db.insert_into_comment(df=df_comment_insert)
            if comment_inserted:
                flash("Berjaya memuatnaik komen", "success")
            else:
                flash("Gagal memuatnaik komen", "warning")

        komen_query = f"""
                select k.timestamp, k.id_komen, k.id_peperiksaan,  p.nama_peperiksaan, k.komen_oleh, k.komen
                from komen_keputusan k
                JOIN peperiksaan p
                ON k.id_peperiksaan = p.id_peperiksaan                 
                WHERE p.id_peperiksaan = {id_peperiksaan}
            """
        df_comments = db.query_data(komen_query)
        if not df_comments.empty:
            df_comments['timestamp'] = pd.to_datetime(df_comments['timestamp'], errors='coerce').dt.strftime(
                "%Y-%m-%d %H:%M")
            details = df_comments.to_dict(orient="records")
        else:
            details = None

        return render_template("add_comments.html",
                               id_peperiksaan=id_peperiksaan,
                               details=details)
@app.route('/edit_comments/<int:id_peperiksaan>/<int:id_komen>', methods=['GET', 'POST'])
def edit_comments(id_peperiksaan, id_komen):
    with sql_offsprings() as db:
        if request.method == 'POST':
            komen_update = [{
                'id_komen': id_komen,
                'id_peperiksaan': id_peperiksaan,
                'komen_oleh': request.form['komen_oleh'],
                'komen': request.form['komen']
            }]

            updated = db.update_komen(komen_update)
            if updated:
                flash(f"Update komen id: {updated['id_komen']} success", "success")
            else:
                flash(f"Update komen id: {updated['id_komen']} success", "warning")

            return redirect(url_for('add_comment'), id_peperiksaan=id_peperiksaan)
        komen_sql = f"""
            SELECT *
            FROM komen_keputusan
            WHERE id_komen = {id_komen}
            AND id_peperiksaan = {id_peperiksaan}   
        """
        komen_df = db.query_data(komen_sql)
        komen = komen_df.to_dict(orient="records")

        return render_template('edit_comment.html',
                               details=komen,
                               id_komen=id_komen,
                               id_peperiksaan=id_peperiksaan)

@app.route('/add_jadual/<int:id_peperiksaan>/<int:id_subjek_peperiksaan>', methods=['GET', 'POST'])
def add_jadual(id_peperiksaan, id_subjek_peperiksaan):
    with sql_offsprings() as db:
        if request.method == 'POST':
            data_jadual = {
                'tarikh': request.form['tarikh'],
                'mula': request.form['masa_mula'],
                'tamat': request.form['masa_tamat']
            }
            df_jadual = pd.DataFrame([data_jadual])

            try:
                db.insert_into_table(table_name='jadual_peperiksaan', df=df_jadual)
                flash("Berjaya simpan tarikh dan masa peperiksaan", "success")
                query_jadual = """
                        SELECT TOP 1 id_jadual
                        FROM jadual_peperiksaan
                        ORDER BY created_datetime desc  
                    """

                df_id_jadual = db.query_data(query_jadual)
                id_jadual = df_id_jadual.loc[0, 'id_jadual']
                update = {
                    'id_jadual':int(id_jadual),
                    'id_peperiksaan': id_peperiksaan,
                    'id_subjek_peperiksaan': id_subjek_peperiksaan
                }

                try:
                    updated = db.update_id_jadual_subjek_peperiksaan(update)
                    if updated:
                        flash(f"Berjaya kemaskini id_jadual: {id_jadual}", "success")
                    else:
                        flash(f"Gagal kemaskini id_jadual: {id_jadual}", "warning")
                except Exception as e:
                    logging.warning(e)

            except Exception as e:
                flash("Gagal simpan tarikh dan masa peperiksaan", "warning")

            return redirect(url_for('daftar_subjek', id_peperiksaan=id_peperiksaan,
                                        id_subjek_peperiksaan=id_subjek_peperiksaan))

        query_details =f"""
                SELECT *
                FROM vw_daftar_peperiksaan
                WHERE id_peperiksaan = {id_peperiksaan}
                AND id_subjek_peperiksaan = {id_subjek_peperiksaan}
            """
        df_details = db.query_data(query_details)

    return render_template('add_jadual.html',
                           details = df_details.to_dict(orient='records'),
                           id_peperiksaan=id_peperiksaan,
                           id_subjek_peperiksaan = id_subjek_peperiksaan)

@app.route('/edit_jadual/<int:id_jadual>/<int:id_peperiksaan>', methods=['GET', 'POST'])
def edit_jadual(id_jadual, id_peperiksaan):
    with sql_offsprings() as db:
        if request.method=='POST':
            update = {
                'id_jadual': id_jadual,
                'tarikh': request.form['tarikh'],
                'mula': request.form['mula'],
                'tamat': request.form['tamat']
            }

            try:
                updated = db.update_jadual(update)
                if updated:
                    flash(f"Kemaskini jadual berjaya: {id_jadual}", "success")
                else:
                    flash(f"Kemaskini jadual gagal: {id_jadual}", "success")
            except Exception as e:
                flash(f"Kemaskini jadual gagal: {id_jadual}: {e}", "success")
            return redirect(url_for('daftar_subjek', id_peperiksaan=id_peperiksaan))

        query_jadual = f"""
                        SELECT * 
                        FROM vw_daftar_peperiksaan
                        WHERE id_peperiksaan = {id_peperiksaan}
                        AND id_jadual = {id_jadual}  
                    """
        df_details = db.query_data(query_jadual)
        details = df_details.to_dict(orient='records')

        return render_template('edit_jadual.html',
                               details=details)
@app.route("/typing_test", methods=['GET', 'POST'])
def typing_test():
    with sql_offsprings() as db:
        directory = 'static/artikel'
        txt_files = [f for f in os.listdir(directory) if f.endswith('.txt')]

        contents = []
        for txt_file in txt_files:
            filepath = os.path.join(directory, txt_file)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                contents.append(content)

        articles = [{'article': f, 'content': c} for f, c in zip(txt_files, contents)]
        selected_filename = request.args.get('article') or (articles[0]['article'] if articles else '')
        selected_article = next((a for a in articles if a['article'] == selected_filename), articles[0])

        sql_person = "SELECT id_person, full_name FROM person"
        df_person = db.query_data(sql_person)

        if request.method == 'POST':
            data = {
                'id_person': request.form['id_person'].strip(),
                'wpm': request.form['wpm'].strip(),
                'accuracy': request.form['accuracy'].strip(),
                'duration': request.form['duration'].strip(),
                'articles': request.form['article']
            }
            df_data = pd.DataFrame([data])

            try:
                db.insert_into_typing_results(df=df_data)
                logger.info("Typing test result inserted.")
            except Exception as e:
                logger.error(f"Failed to insert the results, error: {e}")

            # Force reload with selected article after POST
            return redirect(url_for('typing_test', article=request.form['article']))

        return render_template("typing_test.html",
                               articles=articles,
                               article=selected_article,
                               person=df_person.to_dict(orient='records'))


@app.route('/keputusan_menaip', methods=['GET', 'POST'])
def keputusan_menaip():
    with sql_offsprings() as db:
        sql_menaip = """SELECT p.full_name, k.*
                        FROM typing_results k
                        LEFT JOIN person p
                        ON p.id_person = k.id_person 
                    """

        df_menaip = db.query_data(sql_menaip)
        df_menaip = df_menaip.sort_values('full_name')

        df_percubaan = df_menaip.groupby('full_name').agg({
            'wpm': 'mean',
            'accuracy': 'mean',
            'duration': 'mean',
            'articles': 'nunique',
            'timestamp': 'count'
        }).reset_index()

        df_percubaan.rename(columns={
            'wpm': 'purata_wpm',
            'accuracy': 'purata_accuracy',
            'duration': 'purata_duration_saat',
            'articles': 'jumlah_artikel_dicuba',
            'timestamp': 'bilangan_percubaan'
        }, inplace=True)

    return render_template('keputusan_menaip.html',
                           details=df_menaip.to_dict(orient='records'),
                           percubaan = df_percubaan.to_dict(orient='records'))

@app.route('/delete_result_menaip/<int:id>', methods=['POST'])
def delete_result_menaip(id):
    with sql_offsprings() as db:
       try:
           db.delete_menaip(id)
           flash("Berjaya memadam keputusan menaip.")
           return redirect(url_for('keputusan_menaip'))
       except Exception as e:
           flash("Gagal memadam keputusan peperiksaan.")
           return redirect(url_for('keputusan_menaip'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
