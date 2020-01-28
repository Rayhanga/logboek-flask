from flask import jsonify, make_response, request, abort, redirect, url_for
import datetime

from app import app, auth, db
from app.models import Akun, Jurnal, Jurnal_Detail, Jurnal_Detail_Penjualan, Barang

@app.route('/api/v1.0/akun/', methods=['GET', 'POST'])
@auth.login_required
def akun_list():
    if request.method == 'GET':
        query = Akun.query.all()
        res_list = []

        for akun in query:
            query_detail = Jurnal_Detail.query.filter_by(akun_ref=akun.ref).all()
            jurnal_details = []
            saldo = 0

            for data in query_detail:
                jurnal = Jurnal.query.filter_by(id=data.jurnal_id).first_or_404()
                # print(jurnal)
                if(data.dk == 'D'):
                    saldo = saldo + data.nominal
                else:
                    saldo = saldo - data.nominal
                    
                jurnal_details.append({
                    'tanggal': jurnal.tanggal.strftime("%Y-%m-%dT%H:%M:%S"),
                    'uraian': jurnal.uraian,
                    'nominal': data.nominal,
                    'dk': data.dk
                })

            res_list.append({
                'ref': akun.ref,
                'nama': akun.nama,
                'details': jurnal_details,
                'saldo': saldo
            })

        return jsonify({
            "akun_list": res_list
        })

    if request.method == 'POST':
        if not request.is_json:
            return abort(400)

        req_data = request.get_json()
        
        if not isinstance(req_data, dict):
            return abort(400)

        akun_baru = Akun(
            ref=req_data['ref'],
            nama=req_data['nama']
        )

        ##### Check if data already exist ####
        if Akun.query.filter_by(ref=req_data['ref']).first() or Akun.query.filter_by(nama=req_data['nama']).first():
            return abort(409)

        db.session.add(akun_baru)
        db.session.commit()

        return redirect(url_for('akun_list'))
        
    return abort(405)

@app.route('/api/v1.0/jurnal/', methods=['GET', 'POST'])
@auth.login_required
def jurnal_list():    
    if request.method == 'GET':
        query = Jurnal.query.all()
        res_list = []

        for jurnal in query:
            query_detail = Jurnal_Detail.query.filter_by(jurnal_id=jurnal.id).all()
            jurnal_details = []

            for data in query_detail:
                query_akun = Akun.query.filter_by(ref=data.akun_ref).first()
                query_dp = Jurnal_Detail_Penjualan.query.filter_by(jurnal_details_id=data.id).first()

                dp = None

                if(query_dp):
                    dp = {
                        'barang_id': query_dp.barang_id,
                        'nominal': query_dp.nominal
                    }

                jurnal_details.append({
                    'id': data.id,
                    'akun': query_akun.nama,
                    'nominal': data.nominal,
                    'dk': data.dk,
                    'dp': dp
                })

            res_list.append({
                'id': jurnal.id,
                'uraian': jurnal.uraian,
                'tanggal': jurnal.tanggal.strftime("%d/%m/%Y %H:%M:%S"),
                'details': jurnal_details
            })
        return jsonify({
            'jurnal_list': res_list
        })

    if request.method == 'POST':
        ### Restrict to JSON only ###
        if not request.is_json:
            return abort(400)

        req_data = request.get_json()
        
        data_details = req_data['details']

        if not isinstance(req_data, dict) and not isinstance(data_details, list):
            return abort(400)

        jurnal_baru = Jurnal(
            uraian=req_data['uraian'],
            tanggal=datetime.datetime.strptime(req_data['tanggal'], "%d/%m/%Y %H:%M:%S") 
        )

        db.session.add(jurnal_baru)
        db.session.commit()
        
        for data in data_details:
            detail_baru = Jurnal_Detail(
                jurnal_id=jurnal_baru.id,
                akun_ref=data['akun_ref'],
                nominal=float(data['nominal']),
                dk=data['dk'].upper()
            )

            db.session.add(detail_baru)
            db.session.commit()

            try:
                dp = data['dp']
                dp_baru = Jurnal_Detail_Penjualan(
                    jurnal_details_id=detail_baru.id,
                    barang_id=dp['barang_id'],
                    nominal=dp['nominal']
                )
                db.session.add(dp_baru)
                db.session.commit()
            except KeyError:
                pass

            # print(detail_baru)

        ##### Check if data already exist ####
        # if Jurnal.query.filter_by(uraian=req_data['uraian']).first():
        #     return abort(409)

        return redirect(url_for('jurnal_list'))

    return abort(405)

@app.route('/api/v1.0/barang/', methods=['GET', 'POST'])
@auth.login_required
def barang_list():
    if request.method == 'GET':
        query = Barang.query.all()
        res_list = []

        for barang in query:
            res_list.append({
                'id': barang.id,
                'nama': barang.nama,
                'harga_pokok': barang.harga_pokok,
                'harga_jual': barang.harga_jual,
                'stok': barang.stok
            })

        return jsonify({
            'barang_list': res_list
        })

    if request.method == 'POST':
        if not request.is_json:
            return abort(400)

        req_data = request.get_json()
        
        if not isinstance(req_data, dict):
            return abort(400)

        barang_baru = Barang(
            nama=req_data['nama'],
            harga_pokok=req_data['harga_pokok'],
            harga_jual=req_data['harga_jual'],
            stok=req_data['stok']
        )

        db.session.add(barang_baru)
        db.session.commit()

        return redirect(url_for('barang_list'))

    return abort(405)

@app.route('/api/v1.0/barang/<int:id>/', methods=['GET', 'PUT'])
@auth.login_required
def barang_by_id(id):
    if request.method == 'GET':
        query = Barang.query.filter_by(id=id).first_or_404()

        return jsonify({
            'barang': query
        })

    if request.method == 'PUT':
        if not request.is_json:
            return abort(400)

        req_data = request.get_json()
        
        if not isinstance(req_data, dict):
            return abort(400)

        query = Barang.query.filter_by(id=id).first_or_404()

        query.stok = query.stok + int(req_data['stok'])
        
        query = Barang.query.all()
        res_list = []

        for barang in query:
            res_list.append({
                'id': barang.id,
                'nama': barang.nama,
                'harga_pokok': barang.harga_pokok,
                'harga_jual': barang.harga_jual,
                'stok': barang.stok
            })

        return jsonify({
            'barang_list': res_list
        })

    return abort(405)

@app.route('/api/v1.0/akun/<ref>/', methods=['GET', 'DELETE', 'PUT'])
@auth.login_required
def akun_by_ref(ref):
    if request.method == 'GET':
        query = Akun.query.filter_by(ref=ref).first_or_404()
        query_detail = Jurnal_Detail.query.filter_by(akun_ref=ref).all()

        jurnal_details = []

        for data in query_detail:
            jurnal = Jurnal.query.filter_by(id=data.jurnal_id).first_or_404()
            jurnal_details.append({
                'tanggal': jurnal.tanggal.strftime("%d-%m-%Y %H:%M:%S"),
                'uraian': jurnal.uraian,
                'nominal': data.nominal,
                'dk': data.dk
            })

        akun = {
            'ref': query.ref,
            'nama': query.nama,
            'details': jurnal_details
        }

        

        return jsonify({
            'akun': akun
        })

    if request.method == 'DELETE':
        ### Restrict to JSON only ###
        if not request.is_json:
            return abort(400)

        query = Akun.query.filter_by(ref=ref).first_or_404()

        db.session.delete(query)
        db.session.commit()

        query = Akun.query.all()
        res_list = []
        for akun in query:
            res_list.append({
                'ref': akun.ref,
                'nama': akun.nama
            })
            
        return jsonify({
            "akun_list": res_list
        })

    if request.method == 'PUT':
        ### Restrict to JSON only ###
        if not request.is_json:
            return abort(400)

        query = Akun.query.filter_by(ref=ref).first_or_404()
        
        req_data = request.get_json()

        if Akun.query.filter_by(nama=req_data['nama']).first():
            return abort(409)

        query.nama = req_data['nama']

        db.session.commit()

        query = Akun.query.all()
        res_list = []
        for akun in query:
            res_list.append({
                'ref': akun.ref,
                'nama': akun.nama
            })
            
        return jsonify({
            "akun_list": res_list
        })

    return abort(405)

@app.route('/api/v1.0/jurnal/<int:id>/', methods=['GET', 'DELETE'])
@auth.login_required
def jurnal_by_jurnal_id(id):
    if request.method == 'GET':
        query_detail = Jurnal_Detail.query.filter_by(jurnal_id=id).all()

        jurnal_details = []

        for data in query_detail:
            query_akun = Akun.query.filter_by(ref=data.akun_ref).first()
            jurnal_details.append({
                'id': data.id,
                'akun': query_akun.nama,
                'nominal': data.nominal,
                'dk': data.dk
            })

        return jsonify({
            'jurnal_details': jurnal_details
        })

    if request.method == 'DELETE':
        ### Restrict to JSON only ###
        if not request.is_json:
            return abort(400)

        query = Jurnal.query.filter_by(id=id).first_or_404()

        db.session.delete(query)
        db.session.commit()

        query = Jurnal.query.all()
        res_list = []
        for jurnal in query:
            res_list.append({
                'id': jurnal.id,
                'uraian': jurnal.uraian,
                'tanggal': jurnal.tanggal
            })
            
        return jsonify({
            "jurnal_list": res_list
        }) 

###============================================== TODO  ==============================================###
# Refine authentication method with JWT Token Auth