from flask import Flask, render_template, request, redirect, url_for,flash
import pandas as pd
from datetime import datetime
from OffSprings_DB import sql_offsprings

app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route('/')
def index():
    with sql_offsprings() as db:
        try:
            data = db.query_data("SELECT * FROM vw_offsprings_details")
            # You can print or process data here if needed
            return render_template('index.html', data=data.to_dict(orient='records'))
        except Exception as e:
            return f"Error retrieving data: {e}"

@app.route('/persekolahan', methods=['GET', "POST"])
def persekolahan():
    with sql_offsprings() as db:
        if request.method=='POST':
            tahun_persekolahan = request.form['tahun_persekolahan']
            id_person = request.form['id_person']
            id_kelas = request.form['id_kelas']

            persekolahan_update = {
                'id_person':id_person,
                'id_kelas':id_kelas,
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
                'kad_pengenalan':kad_pengenalan,
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
                'id_sekolah':id_sekolah,
                'nama_sekolah':nama_sekolah,
                'alamat_sekolah_line1':alamat_sekolah_line1,
                'alamat_sekolah_line2':alamat_sekolah_line2,
                'alamat_sekolah_line3':alamat_sekolah_line3,
                'telefon_sekolah':telefon_sekolah
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
                'id_kelas':id_kelas,
                'tahun_persekolahan':tahun_persekolahan
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
    with sql_offsprings() as db:
        data_peperiksaan = db.query_data("SELECT * FROM vw_keputusan_peperiksaan")
        return render_template('peperiksaan.html',
                               data_peperiksaan=data_peperiksaan.to_dict(orient='records'))

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
            id_person = request.form['id_person']
            id_kelas = request.form['id_kelas']

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

            else:
                print("No data found")


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
        query_peperiksaan = 'SELECT * FROM peperiksaan'
        data_exam = db.query_data(query_peperiksaan)

        sql_kelas = 'SELECT id_kelas, nama_kelas FROM kelas'
        nama_kelas = db.query_data(sql_kelas)

        sql_person = 'select id_person, full_name from person'
        persons = db.query_data(sql_person)

        return render_template('add_peperiksaan.html',
                               exams=data_exam.to_dict(orient='records'),
                               list_kelas=nama_kelas.to_dict(orient='records'),
                               persons=persons.to_dict(orient='records'))

@app.route('/edit_peperiksaan/<int:id>', methods=['GET', 'POST'])
def edit_peperiksaan(id):
    with sql_offsprings() as db:
        if request.method == 'POST':
            nama_peperiksaan = request.form['nama_peperiksaan'].strip()
            tahun_peperiksaan = request.form['tahun_peperiksaan'].strip()
            tarikh_peperiksaan = request.form['tarikh_peperiksaan'].strip()
            tarikh_peperiksaan = datetime.strptime(tarikh_peperiksaan, '%Y-%m-%d').strftime('%Y-%m-%d')
            update_peperiksaan = {
                'nama_peperiksaan':nama_peperiksaan,
                'tahun_peperiksaan':tahun_peperiksaan,
                'tarikh_peperiksaan':tarikh_peperiksaan,
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

@app.route('/keputusan_matapelajaran', methods=['GET', 'POST'])
def keputusan_matapelajaran():
    with sql_offsprings() as db:
        if request.method == 'POST':
            id_persekolahan = request.form['id_persekolahan'].strip()
            id_peperiksaan = request.form['id_peperiksaan'].strip()
            id_subjek_list = request.form.getlist('id_subjek[]')
            markah_list = request.form.getlist('markah[]')
            gred_list = request.form.getlist('gred[]')

            for id_subjek, markah, gred in zip(id_subjek_list, markah_list, gred_list):
                keputusan_matapelajaran = {
                    'id_persekolahan': id_persekolahan,
                    'id_peperiksaan': id_peperiksaan,
                    'id_subjek': id_subjek.strip(),
                    'markah': markah.strip(),
                    'gred': gred.strip()
                }
                df_keputusan_matapelajaran = pd.DataFrame([keputusan_matapelajaran])
                db.insert_keputusan_matapelajaran(df_keputusan_matapelajaran)

        sql_data_persekolahan = "SELECT * FROM vw_persekolahan"
        sql_data_peperiksaan ="""
            select a.id_peperiksaan, a.tarikh_peperiksaan, a.nama_peperiksaan, c.full_name, d.nama_kelas, a.id_persekolahan
            from peperiksaan a
            join persekolahan b
            on a.id_persekolahan = b.id_persekolahan
            join person c
            on c.id_person = b.id_person
            join kelas d
            on d.id_kelas = b.id_kelas

            """
        sql_subjek = "SELECT * FROM subjek"

        data_persekolahan = db.query_data(sql_data_persekolahan)
        data_peperiksaan = db.query_data(sql_data_peperiksaan)
        data_subjek = db.query_data(sql_subjek)

        return render_template('tambah_keputusan_matapelajaran.html',
                               data_persekolahan=data_persekolahan.to_dict(orient='records'),
                               data_peperiksaan=data_peperiksaan.to_dict(orient='records'),
                               data_subjek=data_subjek.to_dict(orient='records')
                               )

@app.route('/details_peperiksaan/<int:id>', methods=['GET', 'POST'])
def details_peperiksaan(id):
    with sql_offsprings() as db:
        if request.method=="POST":
            print(id)


            sql_persekolahan = f"SELECT id_persekolahan FROM keputusan_peperiksaan WHERE id_peperiksaan = {id}"
            id_persekolahan = db.query_data(sql_query=sql_persekolahan)
            id_persekolahan = id_persekolahan.loc[0, 'id_persekolahan']
            id_peperiksaan = id
            id_subjek_list = request.form.getlist('id_subjek[]')
            markah_list = request.form.getlist('markah[]')
            gred_list = request.form.getlist('gred[]')

            print(id_persekolahan, id_peperiksaan, id_subjek_list, markah_list, gred_list)

            for id_subjek, markah, gred in zip(id_subjek_list, markah_list, gred_list):
                keputusan_matapelajaran = {
                    'id_persekolahan': id_persekolahan,
                    'id_peperiksaan': id_peperiksaan,
                    'id_subjek': id_subjek.strip(),
                    'markah': markah.strip(),
                    'gred': gred.strip()
                }
                df_keputusan_matapelajaran = pd.DataFrame([keputusan_matapelajaran])
                print(df_keputusan_matapelajaran)
                db.insert_keputusan_matapelajaran(df_keputusan_matapelajaran)

        sql_details =f'''
            SELECT 
                p.id_peperiksaan, p.nama_peperiksaan, b.full_name, 
                c.nama_kelas, k.id_keputusan, s.nama_subjek, 
                k.markah, k.gred
            FROM keputusan_peperiksaan k
            LEFT JOIN peperiksaan p ON k.id_peperiksaan = p.id_peperiksaan
            LEFT JOIN subjek s ON s.id_subjek = k.id_subjek
            LEFT JOIN persekolahan a ON a.id_persekolahan = k.id_persekolahan
            LEFT JOIN person b ON a.id_person = b.id_person
            LEFT JOIN kelas c ON c.id_kelas = a.id_kelas
            WHERE p.id_peperiksaan = {id}
        '''
        data = db.query_data(sql_details)  # Assuming query_data accepts parameterized queries

        sql_subjek = "SELECT * FROM subjek"
        data_subjek = db.query_data(sql_subjek)

        if data.empty:
            return render_template('details_peperiksaan.html', details=[])

        return render_template('details_peperiksaan.html',
                               details=data.to_dict(orient='records'),
                               data_subjek=data_subjek.to_dict(orient="records"))

@app.route('/edit_keputusan/<int:id_peperiksaan>/<int:id_keputusan>', methods=['GET', 'POST'])
def edit_keputusan(id_peperiksaan, id_keputusan):
    with sql_offsprings() as db:
        if request.method == 'POST':
            update_keputusan = {
            'markah': request.form['markah'],
            'gred': request.form['gred'],
            'id_keputusan': id_keputusan
            }
            db.update_keputusan(update_keputusan)

            return redirect(url_for('details_peperiksaan', id=id_peperiksaan))

        sql_keputusan = f'''
                select p.id_peperiksaan, b.full_name, c.nama_kelas, k.id_keputusan, s.nama_subjek, k.markah, k.gred
                from keputusan_peperiksaan k
                LEFT JOIN peperiksaan p
                ON k.id_peperiksaan = p.id_peperiksaan
                LEFT JOIN subjek s
                ON s.id_subjek = k.id_subjek
                LEFT JOIN persekolahan a
                ON a.id_persekolahan = k.id_persekolahan
                left join person b
                ON a.id_person = b.id_person
                Left join kelas c
                ON c.id_kelas = a.id_kelas
                WHERE k.id_keputusan = {id_keputusan}              
            '''
        keputusan = db.query_data(sql_keputusan).to_dict(orient='records')

        return render_template('edit_keputusan.html', id_peperiksaan=id_peperiksaan, keputusan=keputusan )

@app.route('/delete_keputusan/<int:id_peperiksaan>/<int:id_keputusan>', methods=['POST'])
def delete_keputusan(id_peperiksaan, id_keputusan):
    with sql_offsprings() as db:
        db.delete_data(table_name='keputusan_peperiksaan', id=id_keputusan, key='id_keputusan')
    return redirect(url_for('details_peperiksaan', id=id_peperiksaan))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
