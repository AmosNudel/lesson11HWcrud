from flask import Flask, render_template, request, jsonify, redirect, url_for
import pandas as pd

df = pd.read_csv('pets.csv')

app = Flask(__name__)

# Read
@app.route("/", methods=['GET'])
def home():
    pets_data = df.to_dict(orient='records')
    return render_template('index.html', pets=pets_data)

@app.route("/add", methods=["GET" , "POST"])
def add():
    global df
    if request.method == "GET":
        return render_template('add.html')
    else:
        data = request.get_json()
        new_id = df['ID'].max() + 1 if not df.empty else 1
        data['ID'] = new_id
        df = df._append(data, ignore_index=True)
        df.to_csv('pets.csv', index=False)
        return jsonify(df.to_dict(orient='records'))
    
@app.route("/del/<id>", methods=["DELETE"])
def delete_pet(id=0):
    global df
    pet_id = int(id)
    if pet_id in df['ID'].values:
        # Remove the pet from the DataFrame
        df = df[df['ID'] != pet_id]
        # Save the updated DataFrame back to CSV
        df.to_csv('pets.csv', index=False)
        return '', 200
    else:
        return '', 404

@app.route("/upd/<id>", methods=["GET", "PUT"])
def update_pet(id=0):
    global df
    pet_id = int(id)
    pet = df[df['ID'] == pet_id].iloc[0]
    if request.method == "GET":
        return render_template('update.html', pet=pet)
    elif request.method == "PUT":
        data = request.get_json()
        # Update the DataFrame directly
        df.loc[df['ID'] == pet_id, 'Name'] = data.get('Name')
        df.loc[df['ID'] == pet_id, 'Category'] = data.get('Category')
        df.loc[df['ID'] == pet_id, 'Price'] = data.get('Price')
        # Save the updated DataFrame back to CSV
        df.to_csv('pets.csv', index=False)
        return '', 204


if __name__=="__main__":
    app.run(debug=True)