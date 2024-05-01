import psycopg2

# Connect to your postgres DB
conn = psycopg2.connect("dbname=- user=- password=-")

# Open a cursor to perform database operations
cur = conn.cursor()


def get_headings(name):
    try:
        cur.execute("SELECT * FROM " + name)
        colnames = [desc[0] for desc in cur.description]
        return colnames
    except Exception as e:
        return e

def open_table(name):
    # Execute a query
    try:
        cur.execute("SELECT * FROM " + name)
        records = cur.fetchall()
        return records
    except Exception as e:
        return e


def insert_into(t_name, data):
    temp = ""
    temp2 = ""
    rec_to_insert = []
    for d in data.keys():
        rec_to_insert.append(data[d])
        temp += "%s" + ','
        temp2 += d + ','
    tup = tuple(rec_to_insert)

    post_ins = f""" INSERT INTO {t_name} ({temp2[:-1]}) VALUES ({temp[:-1]})"""
    try:
        cur.execute(post_ins, tup)
        conn.commit()
    except Exception as e:
        return e
    return "Готово"


def delete_from(t_name, id_name, id):
    sql = f'DELETE FROM {t_name} WHERE {id_name} = %s'
    try:
        cur.execute(sql, (id,))
        conn.commit()
    except Exception as e:
        return e
    return "Готово"

def modify(t_name, id_name, id, data):

    try:
        for d in data.keys():
            sql = f""" UPDATE {t_name}
                            SET {d} = %s
                            WHERE {id_name} = %s"""
            tup = (data[d], id)
            cur.execute(sql, tup)
        conn.commit()
    except Exception as e:
        return e
    return "Готово"


def get_head_for_sql(desc):
    try:
        colnames = [desc[0] for desc in desc]
        return colnames
    except Exception as e:
        return e

def select_org(org_name):
    try:
        sql = f"""SELECT auto_name, auto_num FROM org_autos JOIN orgs ON org_autos.org_id = orgs.orgs_id WHERE orgs.org_name = %s"""
        cur.execute(sql, (org_name,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_ad(ad_name):
    try:
        sql = f"""SELECT delivered_date, delivired_count FROM deliveries JOIN ad_goods ON ad_goods.good_id = deliveries.delivered_good WHERE ad_goods.good_name = %s"""
        cur.execute(sql, (ad_name,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_auto(client_name):
    try:
        sql = f"""SELECT auto_name, auto_num FROM customers_autos JOIN customers ON customers.cust_id = customers_autos.cust_id WHERE customers.customer_fio = %s"""
        cur.execute(sql, (client_name,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_us(us_name):
    try:
        sql = f"""SELECT auto_name, auto_num FROM customers_autos JOIN services ON services.serv_id = customers_autos.serv_id WHERE services.serv_name = %s"""
        cur.execute(sql, (us_name,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_box(us_name):
    try:
        sql = f"""SELECT box_name, box_capasity FROM boxes JOIN customers_autos ON boxes.box_id = customers_autos.box_id WHERE customers_autos.auto_num = %s"""
        cur.execute(sql, (us_name,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_red():
    try:
        sql = f"""SELECT box_name, box_capasity FROM boxes WHERE boxes.box_ready = %s"""
        cur.execute(sql, (True,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_or_num(or_num):
    try:
        sql = f"""SELECT org_name, doc_n FROM orgs JOIN org_autos ON org_autos.org_id = orgs.orgs_id WHERE org_autos.auto_num = %s"""
        cur.execute(sql, (or_num,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res


def usnum(au_num):
    try:
        sql = f"""SELECT serv_name FROM services JOIN customers_autos ON services.serv_id = customers_autos.serv_id WHERE customers_autos.auto_num = %s"""
        cur.execute(sql, (au_num,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def selec_work(au_num):
    try:
        sql = f"""SELECT date FROM workers_at_boxes JOIN workers ON workers.work_id = workers_at_boxes.worker_id WHERE workers.worker_fio = %s"""
        cur.execute(sql, (au_num,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res

def select_kauto(aut_bum):
    try:
        sql = f"""SELECT customer_fio, custom_num FROM customers JOIN customers_autos ON customers.cust_id = customers_autos.cust_id WHERE customers_autos.auto_num = %s"""
        cur.execute(sql, (aut_bum,))
        headers = get_head_for_sql(cur.description)
        res = [list(cur.fetchall()), headers]
    except Exception as e:
        return e
    return res
