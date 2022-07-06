from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

conn = psycopg2.connect("dbname='items' host='localhost'")
cursor = conn.cursor()

@app.route('/weapon/add', methods=(['POST']))
def add_weapon():
  form = request.form
  name = form.get('name')
  if name =='':
    return jsonify("Name is required!"), 400
  type = form.get('type')
  if type =='':
    return jsonify("Type is required!"), 400
  damage = form.get('damage')
  size = form.get('size')
  rating = form.get('rating', '5')
  if rating.isnumeric():
    rating = int(rating)
  else:
    return jsonify('Rating must be numeric'), 400
  
  cursor.execute("INSERT INTO weapons (name, type, damage, size, rating) VALUES(%s,%s,%s,%s,%s)",(name, type, damage, size, rating))
  conn.commit()
  return jsonify('Weapon added'), 200

@app.route('/weapon/edit/<weapon_id>', methods=(['POST']))
def edit_weapon(weapon_id):
  if weapon_id.isnumeric():
    weapon_id = int(weapon_id)
  else:
    return jsonify('ID must be numeric'), 400
  results = cursor.execute('SELECT id FROM weapons WHERE id = %s', [weapon_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No weapon found, please try again.'), 404
  form = request.form
  name = form.get('name')
  if name =='':
    return jsonify("Name is required!"), 400
  type = form.get('type')
  if type =='':
    return jsonify("Type is required!"), 400
  damage = form.get('damage')
  size = form.get('size')
  rating = form.get('rating', '5')
  if rating.isnumeric():
    rating = int(rating)
  else:
    return jsonify('Rating must be numeric'), 400
  
  cursor.execute("UPDATE weapons SET (name, type, damage, size, rating) = (%s,%s,%s,%s,%s) WHERE id = %s",(name, type, damage, size, rating, weapon_id))
  conn.commit()
  return jsonify('Weapon edited'), 200

# @app.route('/weapon/<weapon_name>', methods=(['GET']))
# def get_weapon_by_name(weapon_name):
#   results = cursor.execute('SELECT id, name, type, damage, size, rating FROM weapons WHERE LOWER(name) LIKE %s', [f'%{weapon_name.lower()}%'])
#   results= cursor.fetchone()
#   if results == None:
#     return jsonify('No weapon found, please try again.'), 404
#   results_dictionary = {
#     'id' : results[0],
#     'name' : results[1],
#     'type' : results[2],
#     'damage' : results[3],
#     'size' : results[4],
#     'rating' : results[5]
#   }
#   return jsonify(results_dictionary),200

@app.route('/weapon/<weapon_id>', methods=(['GET']))
def get_weapon_by_name(weapon_id):
  if weapon_id.isnumeric():
    weapon_id = int(weapon_id)
  else:
    return jsonify('ID must be numeric'), 400
  results = cursor.execute('SELECT id, name, type, damage, size, rating FROM weapons WHERE id = %s', [weapon_id])
  results= cursor.fetchone()
  if results == None:
    return jsonify('No weapon found, please try again.'), 404
  results_dictionary = {
    'id' : results[0],
    'name' : results[1],
    'type' : results[2],
    'damage' : results[3],
    'size' : results[4],
    'rating' : results[5]
  }
  return jsonify(results_dictionary),200

@app.route('/weapon/delete/<weapon_id>', methods=(['DELETE']))
def delete_weapon_by_id(weapon_id):
  if weapon_id.isnumeric():
    weapon_id = int(weapon_id)
  else:
    return jsonify('ID must be numeric'), 400
  result = cursor.execute('SELECT name, id FROM weapons WHERE id = %s', [weapon_id])
  result= cursor.fetchone()
  if result == None:
    return jsonify('No weapon found, please try again.'), 404
  cursor.execute('DELETE from weapons WHERE id = %s', [weapon_id])
  conn.commit()
  return jsonify(f'Weapon ({result[0]}, ID#{result[1]}) deleted'), 200


@app.route('/weapons/list', methods=(['GET']))
def get_all_weapons():
  results = cursor.execute('SELECT id, name, type, damage, size, rating FROM weapons')
  results = cursor.fetchall()
  list_of_weapons = []

  for x in results:
    list_of_weapons.append({
    'id' : x[0],
    'name' : x[1],
    'type' : x[2],
    'damage' : x[3],
    'size' : x[4],
    'rating' : x[5]
    })
  
  
  return jsonify({'weapons' : list_of_weapons}),200

if __name__ == "__main__":
  app.run()

# CREATE TABLE IF NOT EXISTS Weapons (
#   id serial PRIMARY KEY,
#   Name VARCHAR NOT NULL,
#   Type VARCHAR NOT NULL,
#   Damage VARCHAR,
#   Size VARCHAR,
#   Rating INT DEFAULT 5
# );