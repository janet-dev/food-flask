from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    food_name = db.Column(db.String(100), nullable=False)
    reviewer_name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String(255))

    def to_dict(self):
        return {
            "id": self.id,
            "food_name": self.food_name,
            "reviewer_name": self.reviewer_name,
            "rating": self.rating,
            "comment": self.comment
        }

@app.route("/api/reviews", methods=["POST"])
def create_review():
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    if not data.get("food_name") or not data.get("reviewer_name") or not data.get("rating"):
        return jsonify({"error": "Missing required fields"}), 400
    review = Review(
        food_name=data["food_name"],
        reviewer_name=data["reviewer_name"],
        rating=data["rating"],
        comment=data.get("comment", "")
    )
    db.session.add(review)
    db.session.commit()
    return jsonify(review.to_dict()), 201

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    reviews = Review.query.all()
    return jsonify([r.to_dict() for r in reviews]), 200

@app.route("/api/reviews/<int:review_id>", methods=["GET"])
def get_review(review_id):
    review = db.session.get(Review, review_id)
    if review:
        return jsonify(review.to_dict())
    return jsonify({"error": "Review not found"}), 404

@app.route("/api/reviews/<int:review_id>", methods=["PUT"])
def update_review(review_id):
    review = db.session.get(Review, review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    data = request.json
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    review.food_name = data.get("food_name", review.food_name)
    review.reviewer_name = data.get("reviewer_name", review.reviewer_name)
    review.rating = data.get("rating", review.rating)
    review.comment = data.get("comment", review.comment)
    db.session.commit()
    return jsonify(review.to_dict()), 200

@app.route("/api/reviews/<int:review_id>", methods=["DELETE"])
def delete_review(review_id):
    review = db.session.get(Review, review_id)
    if not review:
        return jsonify({"error": "Review not found"}), 404
    db.session.delete(review)
    db.session.commit()
    return jsonify({"message": "Review deleted"}), 200

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
