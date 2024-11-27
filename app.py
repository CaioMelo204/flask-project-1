from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mssql.information_schema import views

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video(name={self.name})"

db.create_all()

video_put_args = reqparse.RequestParser()
video_put_args.add_argument("name", type=str, help="Name of video", required=True)
video_put_args.add_argument("description", type=str, help="Description of video")
video_put_args.add_argument("likes", type=int, help="likes of video", required=True)
video_put_args.add_argument("views", type=int, help="views of video", required=True)

resource_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'description': fields.String,
    'likes': fields.Integer,
    'views': fields.Integer
}

class Video(Resource):
    @marshal_with(resource_fields)
    def get(self, video_id):
        result = VideoModel.query.filter_by(id=video_id).first()
        return result

    @marshal_with(resource_fields)
    def put(self, video_id):
        args = video_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, message="Video already exists")
        video = VideoModel(id=video_id, name=args['name'], views=args['views'], likes=args['likes'])
        db.session.add(video)
        db.session.commit()
        return video, 201

api.add_resource(Video, '/video/<int:video_id>')

if __name__ == '__main__':
    app.run(debug=True)
