# Copyright 2017 Yanis Guenane <yanis@guenane.org>
# Author: Yanis Guenane <yanis@guenane.org>
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import slumber

API_URL = 'http://127.0.0.1:5000'


class API(object):

    def __init__(self):
        self.api = slumber.API(API_URL, append_slash=False)

    def list_books(self):
        """List the book resources. """

        return self.api.books.get()

    def create_book(self, author, summary, title):
        """Create a book resource. """

        return self.api.books.post({'author': author, 'summary': summary, 'title': title})

    def update_book(self, id, author=None, summary=None, title=None):
        """Update a book resource. """

        book = {}

        if author:
            book['author'] = author
        if summary:
            book['summary'] = summary
        if title:
            book['title'] = title

        return self.api.books(id).put(book)

    def delete_book(self, id):
        """Delete specified book resource. """

        return self.api.books(id).delete()
