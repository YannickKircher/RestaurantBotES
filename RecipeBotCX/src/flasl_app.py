from flask import Flask, jsonify, request

app = Flask(__name__)

# Create a sample data store
books = [
    {"id": 1, "title": "Book 1", "author": "Author 1"},
    {"id": 2, "title": "Book 2", "author": "Author 2"}
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify(books[0])

# Run the app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)