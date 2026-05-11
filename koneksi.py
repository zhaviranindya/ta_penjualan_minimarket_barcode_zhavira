from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector
from datetime import datetime, date
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
            elif user['role_zhavira'] == 'admin':
                return redirect('/dashboard_admin')
            elif user['role_zhavira'] == 'owner':
                return redirect('/dashboard_owner')

        return render_template('login_pengguna_zhavira.html',
                               error="Username atau password salah")

    return render_template('login_pengguna_zhavira.html')

@app.route('/dashboard_owner')
def dashboard_owner():
    if session.get('role_zhavira') != 'owner':
        return redirect('/')
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT COUNT(*) as total_transaksi FROM tb_transaksi_zhavira")
    data_t = cursor.fetchone()

    if data_t:
        total_transaksi = data_t['total_transaksi']
    else:
        total_transaksi = 0
        

    cursor.close()
    conn.close()


    return render_template(
        'dasboard_owner_zhavira.html',
        total_transaksi=total_transaksi
    )

@app.route('/dashboard_admin')
def dashboard_admin():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira <= 0 AND status_zhavira = 'aktif'")
    notif_habis = cursor.fetchall()

    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira BETWEEN 1 AND 5 AND status_zhavira = 'aktif'")
    notif_menipis = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) as total_user FROM tb_user_zhavira")
    data_u = cursor.fetchone()

    if data_u:
        total_user = data_u['total_user']
    else:
        total_user = 0

    cursor.execute("SELECT COUNT(*) as total_transaksi FROM tb_transaksi_zhavira")
    data1 = cursor.fetchone()

    if data1:
        total_transaksi = data1['total_transaksi']
    else:
        total_transaksi = 0

    cursor.close()
    conn.close()

    return render_template(
        'dasboard_admin_zhavira.html',
        total_user=total_user,
        total_transaksi=total_transaksi,
        notif_habis=notif_habis, 
        notif_menipis=notif_menipis
    )

@app.route('/dashboard_staf')
def dashboard_staf():
    if session.get('role_zhavira') != 'staf':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira <= 0 AND status_zhavira = 'aktif'")
    notif_habis = cursor.fetchall()

    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira BETWEEN 1 AND 5 AND status_zhavira = 'aktif'")
    notif_menipis = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dasboard_staf_zhavira.html', 
                           notif_habis=notif_habis, 
                           notif_menipis=notif_menipis)

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

@app.route('/nonaktifkan/<id_user_zhavira>')
def nonaktifkan_user(id_user_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_user_zhavira SET status_user_zhavira='nonaktif' 
        WHERE id_user_zhavira=%s
    """, (id_user_zhavira,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('data_user'))

@app.route('/aktifkan/<id_user_zhavira>')
def aktifkan_user(id_user_zhavira):
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_user_zhavira SET status_user_zhavira='aktif' 
        WHERE id_user_zhavira=%s
    """, (id_user_zhavira,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('data_user'))

@app.route('/tambahuser', methods=['GET', 'POST'])
def tambahuser():
    if session.get('role_zhavira') != 'admin':
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_perusahaan_zhavira")
    daftar_perusahaan = cursor.fetchall()

    if request.method == 'POST':
        cursor.execute("""
            SELECT id_user_zhavira
            FROM tb_user_zhavira
            ORDER BY id_user_zhavira DESC
            LIMIT 1
        """)
        last2 = cursor.fetchone()

        if last2:
            angka2 = int(last2['id_user_zhavira'][2:]) + 1
            id_user_zhavira = f"U{angka2:03d}"
        else:
            id_user_zhavira = "U001"

        id_perusahaan_zhavira = request.form.get('id_perusahaan_zhavira')
        username_zhavira = request.form.get('username_zhavira')
        password_zhavira = request.form.get('password_zhavira')
        nama_user_zhavira = request.form.get('nama_user_zhavira')
        role_zhavira = request.form.get('role_zhavira')

        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_user_zhavira (id_user_zhavira, id_perusahaan_zhavira, username_zhavira, password_zhavira, nama_user_zhavira, role_zhavira)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (id_user_zhavira, id_perusahaan_zhavira, username_zhavira, password_zhavira, nama_user_zhavira, role_zhavira))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_user'))

    cursor.close()
    conn.close()
    return render_template('tambah_user_zhavira.html', daftar_perusahaan=daftar_perusahaan)

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

@app.route('/barang')
def data_barang():
    if session.get('role_zhavira') not in ['admin', 'staf']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM tb_barang_zhavira")
    barang_db = cursor.fetchall()

    today = datetime.now().date()

    barang = []

    for b in barang_db:
        harga_asli = b['harga_zhavira']
        nilai_diskon = int(b['diskon_zhavira']) if b['diskon_zhavira'] else 0
        tgl_mulai = b.get('tanggal_mulai_diskon_zhavira')
        tgl_selesai = b.get('tanggal_selesai_diskon_zhavira')

        diskon_aktif = False
        if tgl_mulai and tgl_selesai:
            if not isinstance(tgl_mulai, date):
                tgl_mulai = datetime.strptime(str(tgl_mulai), "%Y-%m-%d").date()
            if not isinstance(tgl_selesai, date):
                tgl_selesai = datetime.strptime(str(tgl_selesai), "%Y-%m-%d").date()

            if tgl_mulai <= today <= tgl_selesai:
                diskon_aktif = True

        if diskon_aktif:
            harga_final = harga_asli - (harga_asli * nilai_diskon / 100)
        else:
            harga_final = harga_asli

        b['harga_final'] = int(harga_final)
        b['diskon_aktif'] = diskon_aktif
        b['diskon_zhavira'] = nilai_diskon 

        barang.append(b)

    cursor.close()
    conn.close()

    return render_template('data_barang_zhavira.html', barang=barang)

@app.route('/nonaktifkan/<kode_barang_zhavira>')
def nonaktifkan_barang(kode_barang_zhavira):
    if session.get('role_zhavira') not in ['admin', 'staf']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_barang_zhavira SET status_zhavira='nonaktif' 
        WHERE kode_barang_zhavira=%s
    """, (kode_barang_zhavira,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('data_barang'))

@app.route('/aktifkan/<kode_barang_zhavira>')
def aktifkan_barang(kode_barang_zhavira):
    if session.get('role_zhavira') not in ['admin', 'staf']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE tb_barang_zhavira SET status_zhavira='aktif' 
        WHERE kode_barang_zhavira=%s
    """, (kode_barang_zhavira,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect(url_for('data_barang'))

@app.route('/tambahbarang', methods=['GET', 'POST'])
def tambahbarang():
    if session.get('role_zhavira') not in ['admin', 'staf']:
        return redirect('/')

    if request.method == 'POST':
        kode_barang_zhavira = request.form.get('kode_barang_zhavira')
        nama_barang_zhavira = request.form.get('nama_barang_zhavira')
        harga_zhavira = int(request.form.get('harga_zhavira'))
        stok_zhavira = int(request.form.get('stok_zhavira'))

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO tb_barang_zhavira (kode_barang_zhavira, nama_barang_zhavira, harga_zhavira, stok_zhavira)
            VALUES (%s, %s, %s, %s)
        """, (kode_barang_zhavira, nama_barang_zhavira, harga_zhavira, stok_zhavira))
        
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('data_barang'))

    return render_template('tambah_barang_zhavira.html')

@app.route('/editbarang/<kode_barang_zhavira>', methods=['GET', 'POST'])
def edit_barang(kode_barang_zhavira):
    if session.get('role_zhavira') not in ['admin', 'staf']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tb_barang_zhavira WHERE kode_barang_zhavira = %s", (kode_barang_zhavira,))
    barang = cursor.fetchone()

    if not barang:
        cursor.close()
        conn.close()
        return f"Data dengan kode_barang_zhavira {kode_barang_zhavira} tidak ditemukan."

    if barang['status_zhavira'] == 'nonaktif':
        cursor.close()
        conn.close()
        return redirect(url_for('data_barang'))

    if request.method == 'POST':
        nama_barang_zhavira = request.form.get('nama_barang_zhavira')
        harga_zhavira = request.form.get('harga_zhavira')
        diskon_zhavira = request.form.get('diskon_zhavira')
        tgl_mulai = request.form.get('tanggal_mulai_diskon_zhavira') or None
        tgl_selesai = request.form.get('tanggal_selesai_diskon_zhavira') or None
        diskon_zhavira = int(diskon_zhavira) if diskon_zhavira else 0
        harga_zhavira = int(harga_zhavira) if harga_zhavira else 0
        tambah_stok = request.form.get('tambah_stok_zhavira')
        tambah_stok = int(tambah_stok) if tambah_stok and int(tambah_stok) > 0 else 0

        stok_lama = barang['stok_zhavira']  
        stok_baru = stok_lama + tambah_stok  


        update_query = """
            UPDATE tb_barang_zhavira
            SET nama_barang_zhavira=%s, harga_zhavira=%s, stok_zhavira=%s,
                diskon_zhavira=%s, tanggal_mulai_diskon_zhavira=%s, tanggal_selesai_diskon_zhavira=%s
            WHERE kode_barang_zhavira=%s
        """
        cursor.execute(update_query, (nama_barang_zhavira, harga_zhavira, stok_baru,
                                        diskon_zhavira, tgl_mulai, tgl_selesai, kode_barang_zhavira))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('data_barang'))

    cursor.close()
    conn.close()
    return render_template('edithapus_barang_zhavira.html', barang=barang)

@app.route('/keuangan')
def laporan_keuangan():
    if session.get('role_zhavira') not in ['admin', 'kasir', 'owner']:
        return redirect('/')
        
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    periode = request.args.get('periode', 'hari')
    tgl_mulai = request.args.get('tgl_mulai', '')
    tgl_selesai = request.args.get('tgl_selesai', '')

    filter_tanggal = ""
    params = []
    if tgl_mulai and tgl_selesai:
        filter_tanggal = "WHERE DATE(tanggal_waktu_zhavira) BETWEEN %s AND %s"
        params = [tgl_mulai, tgl_selesai]

    if tgl_mulai and tgl_selesai:
        query = f"""
            SELECT 
                DATE(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM(
                    CASE 
                        WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                        AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                        AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                            AND b.tanggal_selesai_diskon_zhavira
                        THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                        ELSE 0
                    END
                ) as total_diskon,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira t
            JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
            JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
            {filter_tanggal}
            GROUP BY DATE(tanggal_waktu_zhavira)
            ORDER BY perperiode
        """
    else:
        if periode == 'jam':
            query = f"""
                SELECT 
                    DATE_FORMAT(tanggal_waktu_zhavira, '%H:%i') as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai,
                    CASE 
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 7 AND 22 THEN 'normal'
                        WHEN HOUR(tanggal_waktu_zhavira) = 23 AND MINUTE(tanggal_waktu_zhavira) = 0 THEN 'normal'
                        ELSE 'diluar'
                    END as status_jam
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY DATE_FORMAT(tanggal_waktu_zhavira, '%H:%i')
                ORDER BY perperiode
            """
        elif periode == 'sesi':
            query = f"""
                SELECT 
                    CASE 
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 7 AND 13 THEN 'Pagi (07:00-13:59)'
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 14 AND 17 THEN 'Siang (14:00-17:59)'
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 18 AND 23 THEN 'Sore (18:00-23:00)'
                        ELSE 'Luar Jam Operasional'
                    END as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY perperiode
            """
        elif periode == 'hari':
            query = f"""
                SELECT 
                    DATE(tanggal_waktu_zhavira) as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY DATE(tanggal_waktu_zhavira)
                ORDER BY perperiode
            """
        elif periode == 'minggu':
            query = f"""
                SELECT 
                    CONCAT(
                        'Minggu ke-', 
                        CEIL(DAY(tanggal_waktu_zhavira) / 7),
                        ' ',
                        CASE MONTH(tanggal_waktu_zhavira)
                            WHEN 1 THEN 'Januari' WHEN 2 THEN 'Februari' WHEN 3 THEN 'Maret'
                            WHEN 4 THEN 'April' WHEN 5 THEN 'Mei' WHEN 6 THEN 'Juni'
                            WHEN 7 THEN 'Juli' WHEN 8 THEN 'Agustus' WHEN 9 THEN 'September'
                            WHEN 10 THEN 'Oktober' WHEN 11 THEN 'November' WHEN 12 THEN 'Desember'
                        END,
                        ' ', YEAR(tanggal_waktu_zhavira)
                    ) as perperiode,
                    YEAR(tanggal_waktu_zhavira) as thn,
                    MONTH(tanggal_waktu_zhavira) as bln,
                    CEIL(DAY(tanggal_waktu_zhavira) / 7) as minggu_ke,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY thn, bln, minggu_ke
                ORDER BY thn, bln, minggu_ke
            """
        elif periode == 'bulan':
            query = f"""
                SELECT 
                    CASE MONTH(tanggal_waktu_zhavira)
                        WHEN 1 THEN 'Januari' WHEN 2 THEN 'Februari' WHEN 3 THEN 'Maret'
                        WHEN 4 THEN 'April' WHEN 5 THEN 'Mei' WHEN 6 THEN 'Juni'
                        WHEN 7 THEN 'Juli' WHEN 8 THEN 'Agustus' WHEN 9 THEN 'September'
                        WHEN 10 THEN 'Oktober' WHEN 11 THEN 'November' WHEN 12 THEN 'Desember'
                    END as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY MONTH(tanggal_waktu_zhavira)
                ORDER BY MONTH(tanggal_waktu_zhavira)
            """
        else:
            query = f"""
                SELECT 
                    YEAR(tanggal_waktu_zhavira) as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM(
                        CASE 
                            WHEN b.tanggal_mulai_diskon_zhavira IS NOT NULL
                            AND b.tanggal_selesai_diskon_zhavira IS NOT NULL
                            AND DATE(t.tanggal_waktu_zhavira) BETWEEN b.tanggal_mulai_diskon_zhavira 
                                                                AND b.tanggal_selesai_diskon_zhavira
                            THEN (b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira
                            ELSE 0
                        END
                    ) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY YEAR(tanggal_waktu_zhavira)
            """

    cursor.execute(query, params)
    data = cursor.fetchall()
    total_omzet = sum(d['total_penjualan'] or 0 for d in data)
    cursor.close()
    conn.close()

    return render_template(
        'laporan_keuangan_zhavira.html',
        data=data,
        total_omzet=total_omzet,
        periode=periode,
        tgl_mulai=tgl_mulai,
        tgl_selesai=tgl_selesai
    )


@app.route('/cetak_laporan_keuangan')
def cetak_laporan_keuangan():
    if session.get('role_zhavira') not in ['admin', 'kasir', 'owner']:
        return redirect('/')

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    periode = request.args.get('periode', 'hari')
    tgl_mulai = request.args.get('tgl_mulai', '')
    tgl_selesai = request.args.get('tgl_selesai', '')

    filter_tanggal = ""
    params = []
    if tgl_mulai and tgl_selesai:
        filter_tanggal = "WHERE DATE(tanggal_waktu_zhavira) BETWEEN %s AND %s"
        params = [tgl_mulai, tgl_selesai]

    if tgl_mulai and tgl_selesai:
        query = f"""
            SELECT 
                DATE(tanggal_waktu_zhavira) as perperiode,
                COUNT(*) as jumlah_transaksi,
                SUM(total_belanja_zhavira) as total_penjualan,
                SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
            FROM tb_transaksi_zhavira t
            JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
            JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
            {filter_tanggal}
            GROUP BY DATE(tanggal_waktu_zhavira)
            ORDER BY perperiode
        """
    else:
        if periode == 'jam':
            query = f"""
                SELECT 
                    DATE_FORMAT(tanggal_waktu_zhavira, '%H:%i') as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai,
                    CASE 
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 7 AND 22 THEN 'normal'
                        WHEN HOUR(tanggal_waktu_zhavira) = 23 AND MINUTE(tanggal_waktu_zhavira) = 0 THEN 'normal'
                        ELSE 'diluar'
                    END as status_jam
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY DATE_FORMAT(tanggal_waktu_zhavira, '%H:%i')
                ORDER BY perperiode
            """
        elif periode == 'sesi':
            query = f"""
                SELECT 
                    CASE 
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 7 AND 13 THEN 'Pagi (07:00-13:59)'
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 14 AND 17 THEN 'Siang (14:00-17:59)'
                        WHEN HOUR(tanggal_waktu_zhavira) BETWEEN 18 AND 23 THEN 'Sore (18:00-23:00)'
                        ELSE 'Luar Jam Operasional'
                    END as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY perperiode
            """
        elif periode == 'hari':
            query = f"""
                SELECT 
                    DATE(tanggal_waktu_zhavira) as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY DATE(tanggal_waktu_zhavira)
                ORDER BY perperiode
            """
        elif periode == 'minggu':
            query = f"""
                SELECT 
                    CONCAT(
                        'Minggu ke-', 
                        CEIL(DAY(tanggal_waktu_zhavira) / 7),
                        ' ',
                        CASE MONTH(tanggal_waktu_zhavira)
                            WHEN 1 THEN 'Januari' WHEN 2 THEN 'Februari' WHEN 3 THEN 'Maret'
                            WHEN 4 THEN 'April' WHEN 5 THEN 'Mei' WHEN 6 THEN 'Juni'
                            WHEN 7 THEN 'Juli' WHEN 8 THEN 'Agustus' WHEN 9 THEN 'September'
                            WHEN 10 THEN 'Oktober' WHEN 11 THEN 'November' WHEN 12 THEN 'Desember'
                        END,
                        ' ', YEAR(tanggal_waktu_zhavira)
                    ) as perperiode,
                    YEAR(tanggal_waktu_zhavira) as thn,
                    MONTH(tanggal_waktu_zhavira) as bln,
                    CEIL(DAY(tanggal_waktu_zhavira) / 7) as minggu_ke,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY thn, bln, minggu_ke
                ORDER BY thn, bln, minggu_ke
            """
        elif periode == 'bulan':
            query = f"""
                SELECT 
                    CASE MONTH(tanggal_waktu_zhavira)
                        WHEN 1 THEN 'Januari' WHEN 2 THEN 'Februari' WHEN 3 THEN 'Maret'
                        WHEN 4 THEN 'April' WHEN 5 THEN 'Mei' WHEN 6 THEN 'Juni'
                        WHEN 7 THEN 'Juli' WHEN 8 THEN 'Agustus' WHEN 9 THEN 'September'
                        WHEN 10 THEN 'Oktober' WHEN 11 THEN 'November' WHEN 12 THEN 'Desember'
                    END as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY MONTH(tanggal_waktu_zhavira)
                ORDER BY MONTH(tanggal_waktu_zhavira)
            """
        else:
            query = f"""
                SELECT 
                    YEAR(tanggal_waktu_zhavira) as perperiode,
                    COUNT(*) as jumlah_transaksi,
                    SUM(total_belanja_zhavira) as total_penjualan,
                    SUM((b.harga_zhavira * b.diskon_zhavira / 100) * d.jumlah_zhavira) as total_diskon,
                    SUM(CASE WHEN metode_bayar_zhavira='tunai' THEN total_belanja_zhavira ELSE 0 END) as tunai
                FROM tb_transaksi_zhavira t
                JOIN tb_detail_transaksi_zhavira d ON t.id_transaksi_zhavira = d.id_transaksi_zhavira
                JOIN tb_barang_zhavira b ON d.kode_barang_zhavira = b.kode_barang_zhavira
                {filter_tanggal}
                GROUP BY YEAR(tanggal_waktu_zhavira)
            """

    cursor.execute(query, params)
    data = cursor.fetchall()
    total_omzet = sum(d['total_penjualan'] or 0 for d in data)
    cursor.close()
    conn.close()

    pdf = FPDF(orientation='P', unit='mm', format='A4')
    pdf.add_page()

    pdf.set_font("Arial", size=14, style='B')
    judul_periode = periode.capitalize()
    if tgl_mulai and tgl_selesai:
        judul_periode += f" ({tgl_mulai} s/d {tgl_selesai})"
    pdf.cell(0, 10, f"Laporan Keuangan - Periode: {judul_periode}", ln=True, align='C')
    pdf.ln(5)

    w_per = 35
    w_jml = 30
    w_pen = 42
    w_dis = 41
    w_tun = 42

    pdf.set_font("Arial", size=10, style='B')
    pdf.set_fill_color(227, 6, 19)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(w_per, 10, "Periode", border=1, align='C', fill=True)
    pdf.cell(w_jml, 10, "Jml Transaksi", border=1, align='C', fill=True)
    pdf.cell(w_pen, 10, "Total Penjualan", border=1, align='C', fill=True)
    pdf.cell(w_dis, 10, "Diskon", border=1, align='C', fill=True)
    pdf.cell(w_tun, 10, "Tunai", border=1, align='C', fill=True)
    pdf.ln()

    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=10)
    for d in data:
        pdf.cell(w_per, 9, str(d['perperiode']), border=1, align='C')
        pdf.cell(w_jml, 9, str(d['jumlah_transaksi']), border=1, align='C')
        pdf.cell(w_pen, 9, f"Rp {int(d['total_penjualan'] or 0):,.0f}", border=1, align='R')
        pdf.cell(w_dis, 9, f"Rp {int(d['total_diskon'] or 0):,.0f}", border=1, align='R')
        pdf.cell(w_tun, 9, f"Rp {int(d['tunai'] or 0):,.0f}", border=1, align='R')
        pdf.ln()

    pdf.set_font("Arial", size=10, style='B')
    pdf.cell(w_per + w_jml, 10, "TOTAL OMZET", border=1, align='C')
    pdf.cell(w_pen + w_dis + w_tun, 10, f"Rp {int(total_omzet):,.0f}", border=1, align='R', ln=True)

    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', f'attachment; filename="laporan_{periode}.pdf"')
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
            harga_asli = data['harga_zhavira']
            nilai_diskon = data.get('diskon_zhavira') or 0
            tgl_mulai = data.get('tanggal_mulai_diskon_zhavira')
            tgl_selesai = data.get('tanggal_selesai_diskon_zhavira')

            today = datetime.now().date()
            diskon_aktif = False

            if tgl_mulai and tgl_selesai:
                if isinstance(tgl_mulai, str):
                    tgl_mulai = datetime.strptime(tgl_mulai, "%Y-%m-%d").date()
                if isinstance(tgl_selesai, str):
                    tgl_selesai = datetime.strptime(tgl_selesai, "%Y-%m-%d").date()

                if tgl_mulai <= today <= tgl_selesai:
                    diskon_aktif = True

            harga_final = harga_asli - (harga_asli * nilai_diskon / 100) if diskon_aktif else harga_asli

            preview_zhavira = {
                'kode': data['kode_barang_zhavira'],
                'nama': data['nama_barang_zhavira'],
                'harga': int(harga_final),
                'harga_asli': harga_asli,
                'diskon': nilai_diskon, 
                'diskon_aktif': diskon_aktif
            }
        else:
            error = "Barang tidak ditemukan!"

    if request.method == 'POST' and 'tambah' in request.form:
        kode_barang_zhavira = request.form['kode_barang_zhavira']
        nama_barang_zhavira = request.form['nama_barang_zhavira']
        jumlah_zhavira = int(request.form['jumlah_zhavira'])

        cursor.execute("""
            SELECT stok_zhavira, harga_zhavira,
               diskon_zhavira,
               tanggal_mulai_diskon_zhavira,
               tanggal_selesai_diskon_zhavira
            FROM tb_barang_zhavira
            WHERE kode_barang_zhavira = %s
        """, (kode_barang_zhavira,))

        barang_db = cursor.fetchone()

        if not barang_db:
            error = "Barang tidak ditemukan!"

        elif barang_db['stok_zhavira'] <= 0:
            error = "Stok habis!"

        else:
            stok = barang_db['stok_zhavira']
            item_keranjang = session['keranjang_zhavira'].get(kode_barang_zhavira, {})
            jumlah_lama = item_keranjang.get('jumlah_zhavira', 0)
            total_permintaan = jumlah_lama + jumlah_zhavira

            if total_permintaan > stok:
                error = f"Stok tidak mencukupi! Sisa stok: {stok}"
            else:
                harga_asli = barang_db['harga_zhavira']
                diskon = barang_db.get('diskon_zhavira') or 0
                tgl_mulai = barang_db.get('tanggal_mulai_diskon_zhavira')
                tgl_selesai = barang_db.get('tanggal_selesai_diskon_zhavira')
                
                today = datetime.now().date()
                diskon_aktif = False

                if tgl_mulai and tgl_selesai:
                    if not isinstance(tgl_mulai, date):
                        tgl_mulai = datetime.strptime(str(tgl_mulai), "%Y-%m-%d").date()
                    
                    if not isinstance(tgl_selesai, date):
                        tgl_selesai = datetime.strptime(str(tgl_selesai), "%Y-%m-%d").date()

                    if tgl_mulai <= today <= tgl_selesai:
                        diskon_aktif = True

                if diskon_aktif:
                    harga_final = int(harga_asli - (harga_asli * diskon / 100))
                else:
                    harga_final = int(harga_asli)

                if kode_barang_zhavira in session['keranjang_zhavira']:
                    session['keranjang_zhavira'][kode_barang_zhavira]['jumlah_zhavira'] += jumlah_zhavira
                else:
                    urutan_baru = len(session['keranjang_zhavira']) + 1
                    session['keranjang_zhavira'][kode_barang_zhavira] = {
                        'nama_barang_zhavira': nama_barang_zhavira,
                        'harga_zhavira': harga_final,
                        'harga_asli': harga_asli,
                        'jumlah_zhavira': jumlah_zhavira,
                        'urutan': urutan_baru  
                    }

                item = session['keranjang_zhavira'][kode_barang_zhavira]
                item['subtotal_zhavira'] = item['jumlah_zhavira'] * item['harga_zhavira']
            
                session.modified = True
                return redirect(url_for('transaksi_kasir'))
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

            items_terurut = sorted(
                session['keranjang_zhavira'].items(),
                key=lambda x: x[1].get('urutan', 0)
            )

            for kode_barang_zhavira, item in items_terurut:
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
            session.pop('keranjang_zhavira', None)
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
    if session.get('role_zhavira') != 'kasir':
        return redirect('/')

    if 'keranjang_zhavira' in session:
        if kode_barang_zhavira in session['keranjang_zhavira']:
            session['keranjang_zhavira'].pop(kode_barang_zhavira)
            session.modified = True

    return redirect('/kasir')

@app.route('/struk/<id_transaksi>')
def cetak_struk(id_transaksi):
    if session.get('role_zhavira') != 'kasir':
        return redirect('/')

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
        SELECT d.*, b.nama_barang_zhavira, b.harga_zhavira as harga_normal
        FROM tb_detail_transaksi_zhavira d
        JOIN tb_barang_zhavira b
        ON d.kode_barang_zhavira = b.kode_barang_zhavira
        WHERE d.id_transaksi_zhavira = %s
        ORDER BY d.id_detail_zhavira ASC
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

    
    tinggi_header = 45 
    
    tinggi_footer = 40 
    
    tinggi_barang = 0
    for item in detail:
        
        tinggi_barang += 8 
        
        if int(item['harga_zhavira']) < int(item['harga_normal']):
            tinggi_barang += 3

    tinggi_kertas = tinggi_header + tinggi_barang + tinggi_footer

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

    total_hemat = 0

    CHAR_WIDTH = 32 

    for item in detail:
        nama = item['nama_barang_zhavira']
        qty = item['jumlah_zhavira']
        harga_jual = int(item['harga_zhavira'])
        harga_normal = int(item['harga_normal'])
        subtotal = int(item['subtotal_zhavira'])

        pdf.multi_cell(0, 3, nama)
        pdf.ln(0)

        ada_diskon = harga_jual < harga_normal

        if ada_diskon:
            subtotal_normal = harga_normal * qty
            kiri = f"{qty} x {harga_normal:,.0f}"
            kanan = f"{subtotal_normal:,.0f}"
            spasi = CHAR_WIDTH - len(kiri) - len(kanan)
            if spasi < 1: spasi = 1
            pdf.cell(0, 3, kiri + (" " * spasi) + kanan, ln=True)

            potongan = (harga_normal - harga_jual) * qty
            total_hemat += potongan
            label_disc = f"Disc {int(round((harga_normal - harga_jual) / harga_normal * 100))}%"
            kanan_disc = f"-{potongan:,.0f}"
            spasi = CHAR_WIDTH - len(label_disc) - len(kanan_disc)
            if spasi < 1: spasi = 1
            pdf.set_font("Courier", 'I', size=7)
            pdf.cell(0, 3, label_disc + (" " * spasi) + kanan_disc, ln=True)
            pdf.set_font("Courier", size=7)

            kanan_final = f"{subtotal:,.0f}"
            spasi = CHAR_WIDTH - len(kanan_final)
            if spasi < 1: spasi = 1
            pdf.cell(0, 3, (" " * spasi) + kanan_final, ln=True)

        else:
            kiri = f"{qty} x {harga_jual:,.0f}"
            kanan = f"{subtotal:,.0f}"
            spasi = CHAR_WIDTH - len(kiri) - len(kanan)
            if spasi < 1: spasi = 1
            pdf.cell(0, 3, kiri + (" " * spasi) + kanan, ln=True)

    pdf.ln(1)
    total_item += qty


    pdf.cell(0, 3, "-"*32, ln=True)

    def row(label, value, bold=False):
        val_str = str(value)
        spasi = CHAR_WIDTH - len(label) - len(val_str)
        if spasi < 1:
            spasi = 1
        baris = label + (" " * spasi) + val_str
        if bold:
            pdf.set_font("Courier", 'B', size=7)
        pdf.cell(0, 3, baris, ln=True)
        if bold:
            pdf.set_font("Courier", size=7)

    total_sebelum_diskon = 0
    for item in detail:
        harga_normal = int(item['harga_normal'])
        qty = item['jumlah_zhavira']
        total_sebelum_diskon += harga_normal * qty

    row("Item", total_item)
    row("Total", f"{total_sebelum_diskon:,.0f}")

    if total_hemat > 0:
        row("Hemat", f"-{total_hemat:,.0f}", bold=True)
        row("Anda Bayar", f"{transaksi['total_belanja_zhavira']:,.0f}")
    else:
        row("Anda Bayar", f"{transaksi['total_belanja_zhavira']:,.0f}")

    row("Tunai", f"{transaksi['uang_bayar_zhavira']:,.0f}")
    row("Kembali", f"{transaksi['kembalian_zhavira']:,.0f}")

    pdf.cell(0, 3, "-"*32, ln=True)
    pdf.cell(0, 4, "TERIMA KASIH", ln=True, align='C')

    response = make_response(bytes(pdf.output(dest='S')))
    response.headers.set('Content-Type', 'application/pdf')
    response.headers.set('Content-Disposition', 'attachment; filename="struk.pdf"') 

    return response

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
