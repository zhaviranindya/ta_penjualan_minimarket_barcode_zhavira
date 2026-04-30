from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from datetime import datetime
from fpdf import FPDF
from flask import make_response

app = Flask(__name__)
app.secret_key = "zhavira_secret_key_123"

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'ta_penjualan_minimarket_barcode_zhavira'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return redirect(url_for('login_pengguna'))

@app.route('/login', methods=['GET', 'POST'])
def login_pengguna():
    if request.method == 'POST':
        username = request.form['username_zhavira']
        password = request.form['password_zhavira']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                u.id_user_zhavira,
                u.nama_user_zhavira,
                u.role_zhavira,
                p.nama_perusahaan_zhavira,
                p.nama_market_zhavira
            FROM tb_user_zhavira u
            JOIN tb_perusahaan_zhavira p
            ON u.id_perusahaan_zhavira = p.id_perusahaan_zhavira
            WHERE u.username_zhavira=%s AND u.password_zhavira=%s
        """, (username, password))

        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session['id_user_zhavira'] = user['id_user_zhavira']
            session['nama_user_zhavira'] = user['nama_user_zhavira']
            session['role_zhavira'] = user['role_zhavira']
            session['nama_perusahaan_zhavira'] = user['nama_perusahaan_zhavira']
            session['nama_market_zhavira'] = user['nama_market_zhavira']
            session['keranjang_zhavira'] = {}

            if user['role_zhavira'] == 'kasir':
                return redirect('/kasir')
            elif user['role_zhavira'] == 'staf':
                return redirect('/dashboard_staf')
            elif user['role_zhavira'] == 'manager':
                return redirect('/dashboard_manager')
            elif user['role_zhavira'] == 'admin':
                return redirect('/dashboard_admin')

        return render_template('login_pengguna_zhavira.html',
                               error="Username atau password salah")

    return render_template('login_pengguna_zhavira.html')

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total_user FROM tb_user_zhavira")
    data_u = cursor.fetchone()

    if data_u:
        total_user = data_u['total_user']
    else:
        total_user = 0

    cursor.close()
    conn.close()

    return render_template(
        'dasboard_admin_zhavira.html',
        total_user=total_user,
    )

@app.route('/dashboard_staf')
def dashboard_staf():
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira <= 0")
    notif = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dasboard_staf_zhavira.html', notif=notif)


@app.route('/dashboard_manager')
def dashboard_manager():
    if session.get('role_zhavira') != 'manager':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total_transaksi FROM tb_transaksi_zhavira")
    data1 = cursor.fetchone()

    if data1:
        total_transaksi = data1['total_transaksi']
    else:
        total_transaksi = 0

    cursor.close()
    conn.close()

    return render_template(
        'dasboard_manajer_zhavira.html',
        total_transaksi=total_transaksi
    )

@app.route('/user')
def data_user():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_user_zhavira")
    user1 = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('data_user_zhavira.html', user1=user1)

@app.route('/tambahuser', methods=['GET', 'POST'])
def tambahuser():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    if request.method == 'POST':
        id_user_zhavira = request.form.get('id_user_zhavira')
        id_perusahaan_zhavira = request.form.get('id_perusahaan_zhavira')
        username_zhavira = request.form.get('username_zhavira')
        password_zhavira = request.form.get('password_zhavira')
        nama_user_zhavira = request.form.get('nama_user_zhavira')
        role_zhavira = request.form.get('role_zhavira')

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tb_user_zhavira (id_user_zhavira, id_perusahaan_zhavira, username_zhavira, password_zhavira, nama_user_zhavira, role_zhavira)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_user_zhavira, id_perusahaan_zhavira, username_zhavira, password_zhavira, nama_user_zhavira, role_zhavira))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('data_user'))

    return render_template('tambah_user_zhavira.html')

@app.route('/edituser/<id_user_zhavira>', methods=['GET', 'POST'])
def edit_user(id_user_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_user_zhavira WHERE id_user_zhavira = %s", (id_user_zhavira,))
    user2 = cursor.fetchone()

    if not user2:
        cursor.close()
        conn.close()
        return f"Data dengan id_user_zhavira {id_user_zhavira} tidak ditemukan."

    if request.method == 'POST':
        id_perusahaan_zhavira = request.form.get('id_perusahaan_zhavira')
        username_zhavira = request.form.get('username_zhavira')
        password_zhavira = request.form.get('password_zhavira')
        nama_user_zhavira = request.form.get('nama_user_zhavira')
        role_zhavira = request.form.get('role_zhavira')

        update_query = """
            UPDATE tb_user_zhavira
            SET id_perusahaan_zhavira=%s, username_zhavira=%s, password_zhavira=%s, nama_user_zhavira=%s, role_zhavira=%s
            WHERE id_user_zhavira=%s
        """
        cursor.execute(update_query, (id_perusahaan_zhavira, username_zhavira, password_zhavira, nama_user_zhavira, role_zhavira, id_user_zhavira))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_user'))

    cursor.close()
    conn.close()
    return render_template('edithapus_user_zhavira.html', user2=user2)

@app.route('/hapususer/<id_user_zhavira>')
def hapus_user(id_user_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_user_zhavira WHERE id_user_zhavira = %s", (id_user_zhavira,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_user'))

@app.route('/perusahaan')
def data_perusahaan():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_perusahaan_zhavira")
    perusahaan = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('data_perusahaan_zhavira.html', perusahaan=perusahaan)

@app.route('/tambahperusahaan', methods=['GET', 'POST'])
def tambahperusahaan():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':

        cursor.execute("""
            SELECT id_perusahaan_zhavira
            FROM tb_perusahaan_zhavira
            ORDER BY id_perusahaan_zhavira DESC
            LIMIT 1
        """)
        last1 = cursor.fetchone()

        if last1:
            angka1 = int(last1['id_perusahaan_zhavira'][2:]) + 1
            id_perusahaan_zhavira = f"PC{angka1:03d}"
        else:
            id_perusahaan_zhavira = "PC001"

        nama_perusahaan_zhavira = "PT. PERTIWI MART INDONESIA"
        nama_market_zhavira = "PERTIWI MART"

        alamat_zhavira = request.form.get('alamat_zhavira')
        no_telp_zhavira = request.form.get('no_telp_zhavira')

        cursor.execute("""
            INSERT INTO tb_perusahaan_zhavira
            (id_perusahaan_zhavira, nama_perusahaan_zhavira, nama_market_zhavira, alamat_zhavira, no_telp_zhavira)
            VALUES (%s, %s, %s, %s, %s)
        """, (id_perusahaan_zhavira, nama_perusahaan_zhavira, nama_market_zhavira, alamat_zhavira, no_telp_zhavira))

        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('data_perusahaan'))

    cursor.close()
    conn.close()
    return render_template('tambah_perusahaan_zhavira.html')

@app.route('/editperusahaan/<id_perusahaan_zhavira>', methods=['GET', 'POST'])
def edit_perusahaan(id_perusahaan_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_perusahaan_zhavira WHERE id_perusahaan_zhavira = %s", (id_perusahaan_zhavira,))
    perusahaan1 = cursor.fetchone()

    if not perusahaan1:
        cursor.close()
        conn.close()
        return f"Data dengan id_perusahaan_zhavira {id_perusahaan_zhavira} tidak ditemukan."

    if request.method == 'POST':
        id_perusahaan_zhavira = request.form.get('id_perusahaan_zhavira')
        nama_perusahaan_zhavira = request.form.get('nama_perusahaan_zhavira')
        nama_market_zhavira = request.form.get('nama_market_zhavira')
        alamat_zhavira = request.form.get('alamat_zhavira')
        no_telp_zhavira = request.form.get('no_telp_zhavira')

        update_query = """
            UPDATE tb_perusahaan_zhavira
            SET nama_perusahaan_zhavira=%s, nama_market_zhavira=%s, alamat_zhavira=%s, no_telp_zhavira=%s
            WHERE id_perusahaan_zhavira=%s
        """
        cursor.execute(update_query, (nama_perusahaan_zhavira, nama_market_zhavira, alamat_zhavira, no_telp_zhavira, id_perusahaan_zhavira))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_perusahaan'))

    cursor.close()
    conn.close()
    return render_template('edithapus_perusahaan_zhavira.html', perusahaan1=perusahaan1)

@app.route('/hapusperusahaan/<id_perusahaan_zhavira>')
def hapus_perusahaan(id_perusahaan_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_perusahaan_zhavira WHERE id_perusahaan_zhavira = %s", (id_perusahaan_zhavira,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_perusahaan'))


@app.route('/barang')
def data_barang():
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        UPDATE tb_barang_zhavira
        SET status_zhavira = 
            CASE 
                WHEN stok_zhavira <= 0 THEN 'tidak tersedia'
                ELSE 'tersedia'
            END
    """)
    conn.commit()

    cursor.execute("SELECT * FROM tb_barang_zhavira")
    barang = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('data_barang_zhavira.html', barang=barang)

@app.route('/tambahbarang', methods=['GET', 'POST'])
def tambahbarang():
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

    if request.method == 'POST':
        kode_barang_zhavira = request.form.get('kode_barang_zhavira')
        nama_barang_zhavira = request.form.get('nama_barang_zhavira')
        harga_zhavira = request.form.get('harga_zhavira')
        stok_zhavira = int(request.form.get('stok_zhavira'))

        if stok_zhavira <= 0:
            status_zhavira = 'tidak tersedia'
        else:
            status_zhavira = 'tersedia'

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_barang_zhavira (kode_barang_zhavira, nama_barang_zhavira, harga_zhavira, stok_zhavira, status_zhavira)
            VALUES (%s, %s, %s, %s, %s)
        """, (kode_barang_zhavira, nama_barang_zhavira, harga_zhavira, stok_zhavira, status_zhavira))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('data_barang'))

    return render_template('tambah_barang_zhavira.html')

@app.route('/editbarang/<kode_barang_zhavira>', methods=['GET', 'POST'])
def edit_barang(kode_barang_zhavira):
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE kode_barang_zhavira = %s", (kode_barang_zhavira,))
    barang = cursor.fetchone()

    if not barang:
        cursor.close()
        conn.close()
        return f"Data dengan kode_barang_zhavira {kode_barang_zhavira} tidak ditemukan."

    if request.method == 'POST':
        nama_barang_zhavira = request.form.get('nama_barang_zhavira')
        harga_zhavira = request.form.get('harga_zhavira')
        stok_zhavira = int(request.form.get('stok_zhavira'))

        if stok_zhavira <= 0:
            status_zhavira = 'tidak tersedia'
        else:
            status_zhavira = 'tersedia'

        update_query = """
            UPDATE tb_barang_zhavira
            SET nama_barang_zhavira=%s, harga_zhavira=%s, stok_zhavira=%s, status_zhavira=%s
            WHERE kode_barang_zhavira=%s
        """
        cursor.execute(update_query, (nama_barang_zhavira, harga_zhavira, stok_zhavira, status_zhavira, kode_barang_zhavira))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_barang'))

    cursor.close()
    conn.close()
    return render_template('edithapus_barang_zhavira.html', barang=barang)

@app.route('/hapusbarang/<kode_barang_zhavira>')
def hapus_barang(kode_barang_zhavira):
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tb_barang_zhavira WHERE kode_barang_zhavira = %s", (kode_barang_zhavira,))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_barang'))

@app.route('/keuangan')
def laporan_keuangan():
    if session.get('role_zhavira') != 'manager':
        return redirect('/')
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    periode = request.args.get('periode') 

    if periode == 'jam':
        query = """
            SELECT 
                CONCAT(HOUR(tanggal_waktu_zhavira), ':00') as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai           
                FROM tb_transaksi_zhavira
            GROUP BY HOUR(tanggal_waktu_zhavira)
        """

    elif periode == 'sesi':
        query = """
            SELECT 
                CASE 
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 8 AND 13 THEN 'Pagi'
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 14 AND 17 THEN 'Siang'
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 18 AND 22 THEN 'Sore'
                END as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai            
                FROM tb_transaksi_zhavira
            GROUP BY perperiode
        """

    elif periode == 'hari':
        query = """
            SELECT 
                DATE(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira
            GROUP BY DATE(tanggal_waktu_zhavira)
        """

    elif periode == 'minggu':
        query = """
            SELECT 
                CONCAT('2026 - Minggu ', WEEK(tanggal_waktu_zhavira,1)) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY YEAR(tanggal_waktu_zhavira), WEEK(tanggal_waktu_zhavira,1)
        """

    elif periode == 'bulan':
        query = """
            SELECT 
                CASE MONTH(tanggal_waktu_zhavira)
                    WHEN 1 THEN 'Januari'
                    WHEN 2 THEN 'Februari'
                    WHEN 3 THEN 'Maret'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'Mei'
                    WHEN 6 THEN 'Juni'
                    WHEN 7 THEN 'Juli'
                    WHEN 8 THEN 'Agustus'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'Oktober'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'Desember'
                END as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY MONTH(tanggal_waktu_zhavira)
            ORDER BY MONTH(tanggal_waktu_zhavira)
        """

    else:
        query = """
            SELECT 
                YEAR(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY YEAR(tanggal_waktu_zhavira)
        """

    cursor.execute(query)
    data = cursor.fetchall()

    total_omzet = sum(d['total_penjualan'] or 0 for d in data)

    cursor.close()
    conn.close()

    return render_template(
        'laporan_keuangan_zhavira.html',
        data=data,
        total_omzet=total_omzet,
        periode=periode
    )

@app.route('/cetak_laporan_keuangan')
def cetak_laporan_keuangan():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    periode = request.args.get('periode') 

    if periode == 'jam':
        query = """
            SELECT 
                CONCAT(HOUR(tanggal_waktu_zhavira), ':00') as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai           
                FROM tb_transaksi_zhavira
            GROUP BY HOUR(tanggal_waktu_zhavira)
        """

    elif periode == 'sesi':
        query = """
            SELECT 
                CASE 
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 8 AND 13 THEN 'Pagi'
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 14 AND 17 THEN 'Siang'
                    WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 18 AND 22 THEN 'Sore'
                END as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai            
                FROM tb_transaksi_zhavira
            GROUP BY perperiode
        """

    elif periode == 'hari':
        query = """
            SELECT 
                DATE(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira
            GROUP BY DATE(tanggal_waktu_zhavira)
        """

    elif periode == 'minggu':
        query = """
            SELECT 
                CONCAT('2026 - Minggu ', WEEK(tanggal_waktu_zhavira,1)) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY YEAR(tanggal_waktu_zhavira), WEEK(tanggal_waktu_zhavira,1)
        """

    elif periode == 'bulan':
        query = """
            SELECT 
                CASE MONTH(tanggal_waktu_zhavira)
                    WHEN 1 THEN 'Januari'
                    WHEN 2 THEN 'Februari'
                    WHEN 3 THEN 'Maret'
                    WHEN 4 THEN 'April'
                    WHEN 5 THEN 'Mei'
                    WHEN 6 THEN 'Juni'
                    WHEN 7 THEN 'Juli'
                    WHEN 8 THEN 'Agustus'
                    WHEN 9 THEN 'September'
                    WHEN 10 THEN 'Oktober'
                    WHEN 11 THEN 'November'
                    WHEN 12 THEN 'Desember'
                END as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY MONTH(tanggal_waktu_zhavira)
            ORDER BY MONTH(tanggal_waktu_zhavira)
        """

    else:
        query = """
            SELECT 
                YEAR(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira
            GROUP BY YEAR(tanggal_waktu_zhavira)
        """

    cursor.execute(query)
    data = cursor.fetchall()
    total_omzet = sum(d['total_penjualan'] or 0 for d in data)
    cursor.close()
    conn.close()

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()
    
    pdf.set_font("Arial", size=14, style='B')
    pdf.cell(0, 10, f"Laporan Keuangan - Periode: {periode.capitalize()}", ln=True, align='C')
    pdf.ln(5)

    pdf.set_font("Arial", size=10, style='B')
    pdf.set_fill_color(227, 6, 19) 
    pdf.set_text_color(255, 255, 255)
    
    pdf.cell(40, 10, "Periode", border=1, align='C', fill=True)
    pdf.cell(40, 10, "Jml Transaksi", border=1, align='C', fill=True)
    pdf.cell(55, 10, "Total Penjualan", border=1, align='C', fill=True)
    pdf.cell(55, 10, "Tunai", border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    for d in data:
        pdf.cell(40, 9, str(d['perperiode']), border=1, align='C')
        pdf.cell(40, 9, str(d['jumlah_transaksi']), border=1, align='C')
        pdf.cell(55, 9, f"Rp {int(d['total_penjualan'] or 0):,.0f}", border=1, align='R')
        pdf.cell(55, 9, f"Rp {int(d['tunai'] or 0):,.0f}", border=1, align='R')
        pdf.ln()

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(80, 10, "TOTAL OMZET", border=1, align='C')
    pdf.cell(110, 10, f"Rp {int(total_omzet):,.0f}", border=1, align='R', ln=True)

    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', f'attachment; filename=laporan_{periode}.pdf')
    return response

@app.route('/kasir', methods=['GET', 'POST'])
def transaksi_kasir():
    if session.get('role_zhavira') != 'kasir':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT kode_barang_zhavira, nama_barang_zhavira FROM tb_barang_zhavira")
    daftar_barang_zhavira = cursor.fetchall()

    if 'keranjang_zhavira' not in session:
        session['keranjang_zhavira'] = {}

    error = None
    preview_zhavira = None
    jumlah_zhavira = None

    if request.method == 'POST' and 'cek' in request.form:
        keyword_zhavira = request.form['kode_barang_input']
        jumlah_zhavira = int(request.form['jumlah_input'])

        cursor.execute("""
            SELECT * FROM tb_barang_zhavira
            WHERE kode_barang_zhavira=%s 
            OR nama_barang_zhavira LIKE %s
        """, (keyword_zhavira, f"%{keyword_zhavira}%"))

        data = cursor.fetchone()

        if data:
            preview_zhavira = {
                'kode_zhavira': data['kode_barang_zhavira'],
                'nama_zhavira': data['nama_barang_zhavira'],
                'harga_zhavira': data['harga_zhavira']
            }
        else:
            error = "Barang tidak ditemukan!"

    if request.method == 'POST' and 'tambah' in request.form:
        kode_barang_zhavira = request.form['kode_barang_zhavira']
        nama_barang_zhavira = request.form['nama_barang_zhavira']
        harga_zhavira = int(request.form['harga_zhavira'])
        jumlah_zhavira = int(request.form['jumlah_zhavira'])

        if kode_barang_zhavira in session['keranjang_zhavira']:
            session['keranjang_zhavira'][kode_barang_zhavira]['jumlah_zhavira'] += jumlah_zhavira
        else:
            session['keranjang_zhavira'][kode_barang_zhavira] = {
                'nama_barang_zhavira': nama_barang_zhavira,
                'harga_zhavira': harga_zhavira,
                'jumlah_zhavira': jumlah_zhavira
            }

        session['keranjang_zhavira'][kode_barang_zhavira]['subtotal_zhavira'] = \
            session['keranjang_zhavira'][kode_barang_zhavira]['jumlah_zhavira'] * harga_zhavira

        session.modified = True
        preview_zhavira = None
        jumlah_zhavira = None

    total_belanja_zhavira = sum(
        item['subtotal_zhavira']
        for item in session['keranjang_zhavira'].values()
    )

    if request.method == 'POST' and 'cetak' in request.form:
        if not session['keranjang_zhavira']:
            return redirect('/kasir')

        metode_bayar_zhavira = request.form['metode_bayar_zhavira']
        uang_bayar_zhavira = int(request.form['uang_bayar_zhavira'])

        if uang_bayar_zhavira < total_belanja_zhavira:
            error = "Uang tidak cukup!"
        else:
            kembalian_zhavira = uang_bayar_zhavira - total_belanja_zhavira

            cursor.execute("""
                SELECT id_transaksi_zhavira
                FROM tb_transaksi_zhavira
                ORDER BY id_transaksi_zhavira DESC
                LIMIT 1
            """)
            last = cursor.fetchone()

            if last:
                angka = int(last['id_transaksi_zhavira'][2:]) + 1
                id_transaksi = f"TX{angka:04d}"
            else:
                id_transaksi = "TX0001"

            cursor.execute("""
                INSERT INTO tb_transaksi_zhavira
                (id_transaksi_zhavira, id_user_zhavira,
                 metode_bayar_zhavira, total_belanja_zhavira,
                 uang_bayar_zhavira, kembalian_zhavira)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                id_transaksi,
                session['id_user_zhavira'],
                metode_bayar_zhavira,
                total_belanja_zhavira,
                uang_bayar_zhavira,
                kembalian_zhavira
            ))

            for kode_barang_zhavira, item in session['keranjang_zhavira'].items():
                cursor.execute("""
                    INSERT INTO tb_detail_transaksi_zhavira
                    (id_transaksi_zhavira, kode_barang_zhavira,
                     harga_zhavira, jumlah_zhavira, subtotal_zhavira)
                    VALUES (%s, %s, %s, %s, %s)
                """, (
                    id_transaksi,
                    kode_barang_zhavira,
                    item['harga_zhavira'],
                    item['jumlah_zhavira'],
                    item['subtotal_zhavira']
                ))

                cursor.execute("""
                    UPDATE tb_barang_zhavira
                    SET stok_zhavira = stok_zhavira - %s
                    WHERE kode_barang_zhavira = %s
                """, (item['jumlah_zhavira'], kode_barang_zhavira))

            conn.commit()
            session['keranjang_zhavira'] = {}
            session.modified = True
            return redirect(url_for('cetak_struk', id_transaksi=id_transaksi))

    cursor.close()
    conn.close()

    return render_template(
        'kasir_transaksi_zhavira.html',
        keranjang=session['keranjang_zhavira'],
        total_belanja_zhavira=total_belanja_zhavira,
        error=error,
        preview_zhavira=preview_zhavira,
        jumlah_zhavira=jumlah_zhavira,
        daftar_barang_zhavira=daftar_barang_zhavira 
    )

@app.route('/hapusitem/<kode_barang_zhavira>')
def hapus_item(kode_barang_zhavira):
    if 'keranjang_zhavira' in session:
        if kode_barang_zhavira in session['keranjang_zhavira']:
            session['keranjang_zhavira'].pop(kode_barang_zhavira)
            session.modified = True

    return redirect('/kasir')

@app.route('/struk/<id_transaksi>')
def cetak_struk(id_transaksi):

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT t.*, u.nama_user_zhavira
        FROM tb_transaksi_zhavira t
        JOIN tb_user_zhavira u
        ON t.id_user_zhavira = u.id_user_zhavira
        WHERE t.id_transaksi_zhavira = %s
    """, (id_transaksi,))
    transaksi = cursor.fetchone()

    cursor.execute("""
        SELECT d.*, b.nama_barang_zhavira
        FROM tb_detail_transaksi_zhavira d
        JOIN tb_barang_zhavira b
        ON d.kode_barang_zhavira = b.kode_barang_zhavira
        WHERE d.id_transaksi_zhavira = %s
    """, (id_transaksi,))
    detail = cursor.fetchall()

    cursor.execute("""
        SELECT p.*
        FROM tb_perusahaan_zhavira p
        JOIN tb_user_zhavira u 
        ON p.id_perusahaan_zhavira = u.id_perusahaan_zhavira
        WHERE u.id_user_zhavira = %s
    """, (transaksi['id_user_zhavira'],))
    perusahaan2 = cursor.fetchone()

    cursor.close()
    conn.close()

    tinggi_dasar = 65
    tinggi_item = len(detail) * 8
    tinggi_kertas = tinggi_dasar + tinggi_item

    pdf = FPDF(orientation='P', unit='mm', format=(58, tinggi_kertas))
    pdf.set_auto_page_break(auto=False, margin=0) 
    pdf.add_page()

    pdf.set_left_margin(4)
    pdf.set_right_margin(4)

    pdf.set_font("Courier", size=7)

    pdf.cell(0, 4, perusahaan2['nama_market_zhavira'], ln=True, align='C')
    pdf.cell(0, 3, perusahaan2['nama_perusahaan_zhavira'], ln=True, align='C')
    pdf.cell(0, 3, perusahaan2['alamat_zhavira'], ln=True, align='C')
    pdf.cell(0, 3, f"Telp: {perusahaan2['no_telp_zhavira']}", ln=True, align='C')

    pdf.ln(1)
    pdf.cell(0, 3, "-"*32, ln=True)

    pdf.cell(0, 3, f"ID : {id_transaksi}", ln=True)
    pdf.cell(0, 3, f"Kasir : {transaksi['nama_user_zhavira']}", ln=True)
    pdf.cell(0, 3, f"Tgl : {datetime.now().strftime('%d-%m-%Y %H:%M')}", ln=True)

    pdf.cell(0, 3, "-"*32, ln=True)

    total_item = 0

    for item in detail:
        nama = item['nama_barang_zhavira']
        qty = item['jumlah_zhavira']
        harga = int(item['harga_zhavira'])
        subtotal = int(item['subtotal_zhavira'])

        pdf.multi_cell(0, 3, nama) 

        kiri = f"{qty}x{harga}"
        kanan = f"{subtotal}"

        pdf.cell(28, 3, kiri)
        pdf.cell(0, 3, kanan, ln=True, align='R')

        total_item += qty

    pdf.cell(0, 3, "-"*32, ln=True)

    def row(label, value):
        pdf.cell(28, 3, label)
        pdf.cell(0, 3, str(value), ln=True, align='R')

    row("Item", total_item)
    row("Total", transaksi['total_belanja_zhavira'])
    row("Tunai", transaksi['uang_bayar_zhavira'])
    row("Kembali", transaksi['kembalian_zhavira'])

    pdf.cell(0, 3, "-"*32, ln=True)
    pdf.cell(0, 4, "TERIMA KASIH", ln=True, align='C')

    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment', filename='struk.pdf') 

    return response

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
