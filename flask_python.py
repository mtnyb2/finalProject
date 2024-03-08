import contextlib
import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, send_file, send_from_directory
import sqlite3


app = Flask(__name__)

@contextlib.contextmanager
def _get_cursor():
    conn = sqlite3.connect('Manual Database.db') 
    yield conn.cursor()
    conn.commit()
    conn.close()


@app.route("/worker/<id>", methods=['GET', 'POST'])
def get_worker_details(id: str):
    with _get_cursor() as cursor:
        if request.method == 'GET':
            worker_result = cursor.execute('SELECT * FROM worker WHERE id=?', (id,)).fetchone()
            id, name, fname, city, address, phone_num, email, gender, department, role, cared_by, emergency_contact_name, emergency_contact_phone = worker_result
            worker_details = ({
                "id": id,
                "name": name,
                "fname": fname,
                "city": city,
                "phone_num": phone_num,
                "gender": gender,
                "department":  department,
                "role": role,
                "cared_by": cared_by,
                "emergency_contact_name": emergency_contact_name,
                "emergency_contact_phone": emergency_contact_phone
            })
            return worker_details
        else:
            id = request.form.get('id')
            name = request.form.get('name')
            fname = request.form.get('fname')
            city = request.form.get('city')
            address = request.form.get('address')
            phone_num = request.form.get('phone_num')
            email = request.form.get('email')
            gender = request.form.get('gender')
            department = request.form.get('department')
            role = request.form.get('role')
            cared_by = request.form.get('cared_by')
            emergency_contact_name = request.form.get('emergency_contact_name')
            emergency_contact_phone = request.form.get('emergency_contact_phone')
            try:
                cursor.execute("""UPDATE worker SET
                                id = ?,
                                name = ?,
                                fname = ?,
                                city = ?,
                                address = ?,
                                phone_num = ?,
                                email = ?,
                                gender = ?,
                                department = ?
                                role = ?,
                                cared_by= ?,
                                emergency_contact_name = ?,
                                emergency_contact_phone = ?""",
                                (id, name, fname, city, address, phone_num, email, gender, department, role, cared_by, emergency_contact_name, emergency_contact_phone))
                return "Worker updated"
            except Exception as e:
                print(f"Failed to update worker {name} {fname} with id = {id}")
                return "Failed to insert", 400



def _get_all_sales_for_customer(curosr, customer_id: int):
    statement = """SELECT sale.id, sale.sale_timestamp, sale.status, item.manufacturer_name, item.price, item.id
      from 'OnlineSelling' sale join 'SaleToItem' sale_to_item on sale_to_item.sale_id = sale.id 
      join 'MarketingItems' item on item.id = sale_to_item.item_id
      where sale.customer_id = ?;"""
    all_items_and_sales = curosr.execute(statement, (customer_id,)).fetchall()
    
    sales = {}
    for row in all_items_and_sales:
        sale_id, timestamp, status, manufacturer_name, price, item_id = row
        if sale_id in sales.keys():
            sales[sale_id]['items_sold'].append({"manufacturer_name": manufacturer_name,
                                                "price": price,
                                                "item_id": item_id})
        else:
            sales[sale_id] = {'timestamp': timestamp, 'id': sale_id, 'status': status, 'items_sold': [
                {"manufacturer_name": manufacturer_name,
                                                "price": price,
                                                'item_id': item_id}
            ]}
    return [sale for sale in sales.values()]


@app.route("/customers", methods=['GET', 'POST'])
def get_customers():
    with _get_cursor() as cursor:
        if request.method == 'GET':
            args = request.args
            if not args:
                all_customers_result = cursor.execute("SELECT * FROM 'Customers'")
                customers = [dict(id=row[0], name=row[1], phone_number=row[2], email=row[3], address=row[4], age=row[5]) for row in all_customers_result.fetchall()]
                return jsonify(customers)
            else:
                if 'search' in args:
                    the_query = "SELECT * FROM 'Customers' customer where customer.name || customer.phone_number || customer.email || customer.address || customer.age like (?)"
                    all_customers_result = cursor.execute(the_query, (f"%{args['search']}%",))
                    customers = [dict(id=row[0], name=row[1], phone_number=row[2], email=row[3], address=row[4], age=row[5]) for row in all_customers_result.fetchall()]
                    for customer in customers:
                        customer['sales'] = _get_all_sales_for_customer(cursor, customer['id'])
                    return customers
                else:
                    query_parts = []
                    values = []
                    for key in args.keys():
                        if key in ['name', 'phone_number', 'email', 'address', 'age']:
                            query_parts.append(f"{key} = ?")
                            values.append(args[key])
                    query_string = " AND ".join(query_parts)
                    sql_query = "SELECT * FROM Customers"
                    if query_parts:
                        sql_query += f" WHERE {query_string}"
                    all_customers_result = cursor.execute(sql_query, values)
                    customers = [dict(id=row[0], name=row[1], phone_number=row[2], email=row[3], address=row[4], age=row[5]) for row in all_customers_result.fetchall()]
                    return jsonify(customers)
        elif request.method == 'POST':
            data = request.json
            try:
                cursor.execute('INSERT INTO "Customers" (id, name, phone_number, email, address, age) VALUES (?, ?, ?, ?, ?, ?)',
                               (data['id'], data['name'], data['phone_number'], data['email'], data['address'], data['age']))
                return jsonify({"success": True, "message": "Customer added successfully"}), 201
            except Exception as e:
                print(f"Failed to insert customer {data['name']} with id {data['id']}: {e}")
                return jsonify({"success": False, "message": "Failed to insert customer"}), 400


@contextlib.contextmanager
def _get_cursor():
    conn = sqlite3.connect('Manual Database.db') 
    yield conn.cursor()
    conn.commit()
    conn.close()


@app.route("/customerService", methods=['GET', 'POST'])
def get_customers_tickets():
    with _get_cursor() as cursor:
        if request.method == 'GET':
            statement = """SELECT customer.name,
              customer.address,
                complaint.sale_id,
                  complaint.id,
                   customer.id,
                    complaint.details,
                      complaint.type,
                        complaint.created_date,
                          complaint.last_updated,
                          complaint.status,
                          customer.phone_number
                             FROM 'CustomerService' complaint join 'Customers' customer on customer.id = complaint.customer_id"""
            arguments = [statement]
            if 'search' in request.args:
                statement += "where customer.name || customer.address || complaint.details || complaint.type || complaint.status like (?)"
                arguments.append((f"%{request.args['search']}%",))
            all_customers_tickets_result = cursor.execute(*arguments)
            customers_tickets = []
            for customer_name, customer_address, sale_id, ticket_id, customer_id, details, \
                  complaint_type, created_date, last_updated, status, phone_number in all_customers_tickets_result.fetchall():
                customers_tickets.append({
                    "ticket_id": ticket_id,
                    "sale_id": sale_id,
                    "details": details,
                    "customer_id": customer_id,
                    "customer_name": customer_name,
                    "phone_number": phone_number,
                    "customer_address": customer_address,
                    "complaint_type": complaint_type,
                    "last_updated": last_updated,
                    "created_date": created_date,
                    "status": status
                })
            return customers_tickets
        else:
            customer_id = request.form.get('customer_id')
            sale_id = request.form.get('sale_id')
            details = request.form.get('customer_text')
            timestamp = datetime.datetime.now()
            compaint_type = request.form.get('complaint_type')
            status = "חדש"
            try:
                cursor.execute('INSERT INTO "CustomerService" (customer_id, sale_id, details, created_date, status, last_updated, type) VALUES (?, ?, ?, ?, ?, ?, ?)', (customer_id, sale_id, details, timestamp, status, timestamp, compaint_type))
                return "INSERTED"
            except Exception as e:
                print(f"Failed to open new ticket for sale number {sale_id}")
                return "Failed to insert", 400


@app.route("/customerService/<ticket_id>", methods=['GET', 'POST', 'DELETE'])
def get_customer_tickets(ticket_id: str):
    with _get_cursor() as cursor:
        if request.method == 'GET':
            ticket_result = cursor.execute('SELECT * FROM CustomerService WHERE ticket_id=?', (ticket_id,)).fetchone()
            ticket_id, sale_id, details, resolved_by, worker_id, timestamp, status = ticket_result
            customer_details = ({
                "ticket_id": ticket_id,
                "sale_id": sale_id,
                "details": details,
                "resolved_by": resolved_by,
                "worker_id": worker_id,
                "timestamp": timestamp,

                "status": status
            })
            return customer_details
        elif request.method == 'POST':
            details = request.form.get('customer_text')
            timestamp = datetime.datetime.now()
            compaint_type = request.form.get('complaint_type')
            status = request.form.get('status')
            
            try:
                cursor.execute("""UPDATE CustomerService SET
                               details = ?,
                               last_updated = ?,
                               status = ?,
                               type = ? where id = ?""",
                               (details, timestamp, status, compaint_type, ticket_id))
                return "Ticket is updated"
            except Exception as e:
                print(f"Failed to update ticked with id = {ticket_id}. Error {e}")
                return "Failed to insert", 400
            ##מחיקה של פניה פתוחה
        else:
            statment = """DELETE FROM 'CustomerService' where id = ?"""
            cursor.execute(statment, (ticket_id,))
            return "OK", 200
        


@app.route('/new-ticket')
def new_ticket():
    return render_template('add_ticket.html')

@app.route('/customer-search')
def customer_search():
    return render_template('customer_search.html')

@app.route('/customer-service')
def customer_service():
    return render_template('customer_service.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login.html')
def login_page():
    return render_template('login.html')

@app.route('/splash.jpg')
def backgroung_image():
    return send_file("templates/64994452421978.jpg")

@app.route('/static/<item>')
def static_serve(item):
    return send_from_directory('static', item)

@app.route('/api/items')
def get_items():
    # Example: Fetching items from a database
    items = [{"id": 1, "name": "Item 1"}, {"id": 2, "name": "Item 2"}]  # This should be replaced with your database query
    return jsonify(items)


@app.route('/api/submit-ticket', methods=['POST'])
def submit_ticket():
    data = request.json
    selected_item_id = data['itemId']
    comment = data['comment']
    # Here, you would insert the data into your database
    print(f"Item ID: {selected_item_id}, Comment: {comment}")  # Placeholder for actual database insertion
    return jsonify({"success": True, "message": "Ticket submitted successfully"})


if __name__ == '__main__':
    # connet to SQLite DB 
    # make endpoit with POST method to register a new worker, use the SQLite3 cursor to put the row in the DB.
    app.run(debug=True, port=5002)


