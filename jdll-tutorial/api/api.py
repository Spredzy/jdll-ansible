#!/bin/python

import json
import uuid
import os

from flask import Flask
from flask import abort
from flask import jsonify
from flask import request

app = Flask(__name__)

_FILEPATH = '/tmp/toto.txt'


@app.route('/')
def jdll_ansible():
        return 'Bienvenue a l\'atelier API Ansible'


@app.route('/books', methods=['GET'])
def jdll_ansible_get_endpoint():
    """Display the content of the book. """

    if not os.path.exists(_FILEPATH):
        open(_FILEPATH, 'w').write(json.dumps([]))

    books_content = json.loads(open(_FILEPATH).read())
    return jsonify(books_content)


@app.route('/books/<book_id>', methods=['GET'])
def jdll_ansible_get_endpoint_id(book_id):
    """Display the informations of a single book. """

    book = [book for book in json.loads(open(_FILEPATH).read()) if book['id'] == book_id]
    if len(book) == 1:
        return jsonify(book[0])
    else:
        abort(404)


@app.route('/books', methods=['POST'])
def jdll_ansible_post_endpoint():
    """Add content to the book. """

    data = json.loads(request.data)

    if 'title' not in data or 'author' not in data or 'summary' not in data:
        abort(400)

    item = {
        'id': str(uuid.uuid4()),
        'author': data['author'],
        'summary': data['summary'],
        'title': data['title'],
    }

    books_content = json.loads(open(_FILEPATH).read())
    if len([i for i in books_content if (i['title'] == data['title'] and i['summary'] == data['summary'] and i['author'] == data['author'])]) == 0:
        books_content.append(item)
        open(_FILEPATH, 'w').write(json.dumps(books_content))
        return jsonify({'message': 'Book Added'})

    else:
        abort(409)


@app.route('/books/<book_id>', methods=['PUT'])
def jdll_ansible_put_endpoint(book_id):
    """Update content of the book. """

    data = json.loads(request.data)

    books_content = json.loads(open(_FILEPATH).read())
    if book_id not in [i['id'] for i in books_content]:
        abort(404)
    else:
        for i in books_content:
            if i['id'] == book_id:
                if 'title' in data:
                    i['title'] = data['title']

                if 'author' in data:
                    i['author'] = data['author']

                if 'summary' in data:
                    i['summary'] = data['summary']
                break
        open(_FILEPATH, 'w').write(json.dumps(books_content))
        return jsonify({'message': 'Book Updated'})


@app.route('/books/<book_id>', methods=['DELETE'])
def jdll_ansible_delete_endpoint(book_id):
    """Delete content of the file. """

    books_content = json.loads(open(_FILEPATH).read())
    if book_id not in [i['id'] for i in books_content]:
        abort(404)
    else:
        books_content = [i for i in books_content if i['id'] != book_id]
        open(_FILEPATH, 'w').write(json.dumps(books_content))
        return jsonify({'message': 'Book Deleted'}), 204


if __name__ == "__main__":
    app.run()
