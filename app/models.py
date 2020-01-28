from datetime import datetime

from app import db

class Akun(db.Model):
    __tablename__ = 'akun'

    ref = db.Column(db.String(3), nullable=False, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)

    details = db.relationship('Jurnal_Detail', backref='jurnal', lazy='dynamic')

    def __repr__(self):
        return "<Akun {} - {}>".format(self.ref, self.nama)

class Jurnal(db.Model):
    __tablename__ = 'jurnal'

    id = db.Column(db.Integer, primary_key=True)
    uraian = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    # details = db.relationship('Jurnal_Detail', backref='jurnal', lazy='dynamic')

    def __repr__(self):
        return "<Jurnal {} - {}>".format(self.uraian, self.tanggal)


class Jurnal_Detail(db.Model):
    __tablename__ = 'jurnal_detail'

    id = db.Column(db.Integer, primary_key=True)
    jurnal_id = db.Column(db.Integer, db.ForeignKey('jurnal.id'), nullable=False)
    akun_ref = db.Column(db.Integer, db.ForeignKey('akun.ref'), nullable=False)
    nominal = db.Column(db.Float, nullable=False)
    dk = db.Column(db.String(1), nullable=False)

    dp = db.relationship('Jurnal_Detail_Penjualan', backref='jurnal_detail', lazy='dynamic')

    def __repr__(self):
        return "<Jurnal_Detail {} - {} - {} - {}>".format(self.jurnal_id, self.akun_ref, self.nominal, self.dk)

class Barang(db.Model):
    __tablename__ = 'barang'

    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)
    harga_pokok = db.Column(db.Integer, nullable=False)
    harga_jual = db.Column(db.Integer, nullable=False)
    stok = db.Column(db.Integer, nullable=False)

    dp = db.relationship('Jurnal_Detail_Penjualan', backref='barang', lazy='dynamic')

    def __repr__(self):
        return "<Jurnal_Detail {} - {} - {} - {} - {}>".format(self.id, self.nama, self.harga_pokok, self.harga_jual, self.stok)


class Jurnal_Detail_Penjualan(db.Model):
    __tablename__ = 'jurnal_detail_penjualan'

    jurnal_details_id = db.Column(db.Integer, db.ForeignKey('jurnal_detail.id'), primary_key=True)
    barang_id = db.Column(db.Integer, db.ForeignKey('barang.id'), nullable=False)
    nominal = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return "<Jurnal_Detail_Penjualan {} - {} - {}>".format(self.jurnal_details_id, self.barang_id, self.nominal)