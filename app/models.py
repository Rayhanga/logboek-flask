from datetime import datetime

from app import db

class Akun(db.Model):
    __tablename__ = 'akun'

    ref = db.Column(db.String(3), nullable=False, primary_key=True)
    nama = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return "<Akun {} - {}>".format(self.ref, self.nama)

class Jurnal(db.Model):
    __tablename__ = 'jurnal'

    id = db.Column(db.Integer, primary_key=True)
    uraian = db.Column(db.String(50), nullable=False)
    tanggal = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    details = db.relationship('Jurnal_Detail', backref='jurnal', lazy='dynamic')

    def __repr__(self):
        return "<Jurnal {} - {}>".format(self.uraian, self.tanggal)


class Jurnal_Detail(db.Model):
    __tablename__ = 'jurnal_detail'

    id = db.Column(db.Integer, primary_key=True)
    jurnal_id = db.Column(db.Integer, db.ForeignKey('jurnal.id'), nullable=False)
    akun_ref = db.Column(db.Integer, db.ForeignKey('akun.ref'), nullable=False)
    nominal = db.Column(db.Float, nullable=False)
    dk = db.Column(db.String(1), nullable=False)

    def __repr__(self):
        return "<Jurnal_Detail {} - {} - {} - {}>".format(self.jurnal_id, self.akun_ref, self.nominal, self.dk)