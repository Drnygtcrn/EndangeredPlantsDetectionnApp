import base64
import os
import requests
import numpy as np
from flask import Flask, request, jsonify
from flask_cors import CORS
# from keras.models import load_model
from tensorflow.keras.preprocessing import image
from tensorflow.python.estimator import keras
import tensorflow as tf
from PIL import Image
import pyodbc

app = Flask(__name__)
CORS(app)


#siniflar = ['Alyssum Artvinense', 'Astragalus Beypazaricus', 'Campanula Seraglio', 'Centaurium Erythraea',
#               'Hypericum Fissurale', 'Centaurea Kilaea', 'Larkspur', 'Lathyrus Libani',
#               'Lilium Ciliatum', 'Lotus Corniculatus', 'Nonea Karsensis', 'Vuralia Turcica', 'Pyrus Serikensis',
#               'Rhodothamnus Sessilifolius', 'Rumex Bithynicus', 'Centaurea Tchihatcheffii', 'Thermopsis Turcica',
#               'Allium Czelghauricum', 'Allium Peroninianum', 'Galanthus Trojanus']

siniflar = ['Alyssum Artvinense', 'Astragalus Beypazaricus', 'Campanula Seraglio', 'Centaurium Erythraea',
               'Hypericum Fissurale', 'Centaurea Kilaea', 'Larkspur', 'Lathyrus Libani',
               'Lilium Ciliatum', 'Lotus Corniculatus','Nesli Tükenmemekte Olan Bitkiler',
                'Nonea Karsensis', 'Vuralia Turcica', 'Pyrus Serikensis',
               'Rhodothamnus Sessilifolius', 'Rumex Bithynicus', 'Centaurea Tchihatcheffii', 'Thermopsis Turcica',
               'Allium Czelghauricum', 'Allium Peroninianum', 'Galanthus Trojanus']




server = "DESKTOP-276LK4V\\SQLEXPRESS"
database = "KisaDeneme"
username = "DESKTOP-276LK4V\\User"
driver = '{ODBC Driver 17 for SQL Server}'





#@app.route("/getNesliByName", methods=['GET'])
def getirnesli(Latin):
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Nesli WHERE Latin = ?", (Latin,))
    data = cursor.fetchall()
    response = []
    for row in data:
        encoded_image = base64.b64encode(row.Fotograf).decode('utf-8')
        Isim = row.Isim,
        Aciklama=row.Aciklama,
        Latin = row.Latin
        return Isim,Aciklama,encoded_image,Latin



#------------------------------------------ Sık Sorulan Sorular ------------------------
@app.route("/getSSS", methods=['GET'])
def getir():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes')
    cursor = conn.cursor()
    cursor.execute('SELECT Id,Soru,Cevap FROM Sss')
    data = cursor.fetchall()
    response = []
    for row in data:
        response.append({
            'Id': row.Id,
            'Soru': row.Soru,
            'Cevap':row.Cevap
        })

    #conn.close()

    return jsonify(response)


#------------------------------- Nesli Tükenmekte Olanlar -------------------------------
@app.route("/getNesli", methods=['GET'])
def nesli():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Nesli')   #Id,Isim,Latin,Aciklama,Tarih
    data = cursor.fetchall()
    response = []
    for row in data:
        encoded_image = base64.b64encode(row.Fotograf).decode('utf-8')
        response.append({
            'Id': row.Id,
            'Isim': row.Isim,
            'Latin':row.Latin,
            'Aciklama':row.Aciklama,
            'Tarih':row.Tarih,
            'Fotograf' : encoded_image
        })

    #conn.close()  # Veritabanı bağlantısını kapat

    return jsonify(response)


#-------------------------------------------- Prediction -----------------------------------------------

@app.route("/predict", methods=['POST','GET'])
def predict():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'})
    else:
        file = request.files['file']
        filename = file.filename
        file_path = os.path.join(r'static', filename)

        file.save(file_path)

        img = image.load_img(file_path, target_size=(180, 180))

        img_array = image.img_to_array(img)

        img_array = np.expand_dims(img_array, axis=0)

        xd = np.vstack([img_array])


        model = tf.keras.models.load_model('Model.h5')


        prediction = model.predict(xd)


        predicted_class = np.argmax(prediction)


        product = siniflar[predicted_class]

        Isim,Aciklama,Fotograf,Latin = getirnesli(product)


        return jsonify({'result': product, 'Isim': Isim,'Aciklama' : Aciklama,'Fotograf' : Fotograf,'Latin': Latin})

#---------------------------------------------------------postKonum---------------
def get_location_details(latitude, longitude):
    #url = f"https://nominatim.openstreetmap.org/reverse?lat={latitude}&lon={longitude}&format=json"
    url = f"https://api.bigdatacloud.net/data/reverse-geocode-client?latitude={latitude}&longitude={longitude}&localityLanguage=en"
    response = requests.get(url)
    data = response.json()  #Reverse location nominatim api



    city = data.get('city') # or address.get('locality') or address.get('village')
    locality = data.get('locality')      # address.get('neighbourhood')  or address.get('suburb')

    return city, locality

@app.route("/postkonum", methods=['POST'])
def postKonum():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes;charset=utf8')

    cursor = conn.cursor()
    data = request.get_json()  # Gönderilen JSON verisini alır

    city,locality = get_location_details(data['latitude'],data['longitude'])

    cursor.execute("SELECT * FROM Nesli WHERE Latin = ?", (data['isim'],))
    veri = cursor.fetchall()

    for row in veri:
        fotograf = row.Fotograf
        cursor.execute(
            'INSERT INTO Konum (latitude, longitude, isim, fotograf, city, locality) VALUES (?, ?, ?, ?, ?, ? )',
            (data['latitude'], data['longitude'], data['isim'], fotograf, city, locality))

        conn.commit()  # Veritabanı değişikliklerini kaydetme



    conn.close()  # Veritabanı bağlantısını kapatma

    return jsonify({'message': 'Data saved successfully'})


#-----------------------------------------------getKonum

@app.route("/getkonum", methods=['GET'])
def getKonum():
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Nesli')  # tablo adı ekle
    data = cursor.fetchall()
    response = []

    for row in data:
        encoded_image = base64.b64encode(row.fotograf).decode('utf-8')
        response.append({
            'latitude': row.latitude,
            'longitude': row.longitude,
            'isim': row.isim,
            'fotograf': encoded_image,
            'city': row.city,
            'district': row.district,
            'neighborhood': row.neighborhood,
            'road': row.road
        })

    conn.close()

    return jsonify(response)

#--------------------------------------------getSehir--------------------------------
@app.route("/getkonumSehir/<Sehir>", methods=['GET'])
def getSehir(Sehir):
    conn = pyodbc.connect(f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};Trusted_Connection=yes')
    cursor = conn.cursor()
    print(Sehir)
    cursor.execute("SELECT * FROM Konum WHERE city = ?", (Sehir,))  # tablo adı ekle
    data = cursor.fetchall()
    response = []
    for row in data:
        encoded_image = base64.b64encode(row.fotograf).decode('utf-8')
        response.append({
            'latitude': row.latitude,
            'longitude': row.longitude,
            'isim': row.isim,
            'fotograf': encoded_image,
            'city': row.city,
            'locality':row.locality
        })

    conn.close()
    print(response)
    return jsonify(response)






if __name__ == "__main__":
    app.run()