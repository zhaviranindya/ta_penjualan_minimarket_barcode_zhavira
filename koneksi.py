from flask import Flask, request, render_template, redirect, url_for, session
import mysql.connector

app = Flask(__name__)
app.secret_key = "zhavira_secret_key_123"

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'db_penjualan_minimarket_barcode_zhavira'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return redirect(url_for('login_pengguna'))

@app.route('/login', methods=['GET', 'POST'])
def login_pengguna():
    try:
        if request.method == 'POST':
            username_zhavira = request.form['username_zhavira']
            password_zhavira = request.form['password_zhavira']

            conn = get_db_connection()
            cursor = conn.cursor(dictionary=True)

            cursor.execute("""
                SELECT id_user_zhavira, nama_user_zhavira, role_zhavira
                FROM tb_user_zhavira
                WHERE username_zhavira = %s 
                AND password_zhavira = %s
            """, (username_zhavira, password_zhavira))

            user = cursor.fetchone()
            cursor.close()
            conn.close()

            if user:
                session['id_user_zhavira'] = user['id_user_zhavira']
                session['nama_user_zhavira'] = user['nama_user_zhavira']
                session['role_zhavira'] = user['role_zhavira']
                session['keranjang_zhavira'] = {}

                if user['role_zhavira'] == 'kasir':
                    return redirect('/kasir')
                elif user['role_zhavira'] == 'staf':
                    return redirect('/dashboard_staf')
                elif user['role_zhavira'] == 'manager':
                    return redirect('/dashboard_manager')
            else:
                return render_template(
                    'login_pengguna_zhavira.html',
                    error="Username atau password salah"
                )

        return render_template('login_pengguna_zhavira.html')

    except Exception as e:
        return f"Error login: {e}"


@app.route('/dashboard_staf')
def dashboard_staf():
    try:
        if session.get('role_zhavira') != 'staf':
            return redirect('/')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("SELECT * FROM tb_barang_zhavira")
        barang = cursor.fetchall()

        cursor.execute("SELECT * FROM tb_barang_zhavira WHERE stok_zhavira <= 0")
        notif = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template(
            'dasboard_staf_zhavira.html',
            barang=barang,
            notif=notif
        )

    except Exception as e:
        return f"Error dashboard staf: {e}"

@app.route('/dashboard_manager')
def dashboard_manager():
    try:
        if session.get('role_zhavira') != 'manager':
            return redirect('/login')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        cursor.execute("""
            SELECT 
                l.tanggal_zhavira AS tanggal,
                u.nama_user_zhavira AS nama_user,
                l.total_penjualan_zhavira AS total,
                t.metode_bayar_zhavira AS metode
            FROM tb_laporan_keuangan_zhavira l
            JOIN tb_transaksi_zhavira t
                ON l.id_transaksi_zhavira = t.id_transaksi_zhavira
            JOIN tb_user_zhavira u
                ON t.id_user_zhavira = u.id_user_zhavira
            ORDER BY l.tanggal_zhavira DESC
        """)
        transaksi = cursor.fetchall()

        cursor.execute("""
            SELECT nama_barang_zhavira AS nama_barang
            FROM tb_barang_zhavira
            WHERE stok_zhavira <= 0
        """)
        notif = cursor.fetchall()

        cursor.close()
        conn.close()

        return render_template('dasboard_manajer_zhavira.html',
            transaksi=transaksi, notif=notif)
    except Exception as e:
        return str(e)

@app.route('/logout')
def logout():
    try:
        session.clear()
        return redirect('/')
    except Exception as e:
        return f"Logout error: {e}"


if __name__ == '__main__':
    app.run(debug=True)