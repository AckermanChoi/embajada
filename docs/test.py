from app.database import get_connection
try:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT 1')
    print('✅ Conexión OK →', cur.fetchone())
    cur.close()
    conn.close()
except Exception as e:
    print('❌ Error de conexión →', e)
