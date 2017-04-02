#!/usr/bin/python

from ansible.module_utils.basic import *
from jdll import API

ANSIBLE_METADATA = {'status': ['preview'],
                    'supported_by': 'community',
                    'version': '1.0'}

DOCUMENTATION = '''
---
module: book
author: "Yanis Guenane (@Spredzy)"
version_added: "2.3"
short_description: Gerer des resources books de notre API de test.
description:
    - Ce module interagit avec le endpoint /books de notre API de test.
options:
    state:
        required: false
        default: "present"
        choices: [ present, absent ]
        description:
            - Si la resource book doit etre presente ou absente.
    id:
        required: false
        description:
            - L'identifieur de la resource book.
    author:
        required: false
        description:
            - Le nom de l'auteur de book.
    title:
        required: false
        description:
            - Titre du book.
    summary:
        required: true
        description:
            - Resume du book.
'''

EXAMPLES = '''
# Create a new book
- book:
    title: A title
    author: An author
    summary: A  summary

# Update a specific book
- book:
    id: XXXX
    title: Un titre alternatif

# Delete a book
- book:
    id: XXX
    state: absent
'''

RETURN = '''
title:
    description: The title of the book
    returned:
        - changed
        - success
    type: string
    sample: A title
summary:
    description: The summary of the book
    returned:
        - changed
        - success
    type: string
    sample: A summary
id:
    description: ID of the book
    returned:
        - changed
        - success
    type: string
    sample: XXXXX
'''

def main():
    module = AnsibleModule(
        argument_spec=dict(
            state=dict(default='present', choices=['present', 'absent'], type='str'),
            id=dict(type='str'),
            author=dict(type='str'),
            summary=dict(type='str'),
            title=dict(type='str'),
        ),
    )

    # TODO: List of improvement that could be done with
    #       this module as a starting point.
    #
    #  * Implement noop mode with --check
    #  * Set accordingly the 'changed' status based on
    #    the actual action set
    #  * Check return number and return message accordinly
    #

    myapi = API()
    result = {
        'changed': True
    }

    If module.params['state'] == 'absent':
        if 'id' not in module.params:
            module.fail_json(msg='id parameter is mandatory')
        # Call to the bindingL: DELETE
        myapi.delete_book(module.params['id'])

    else:
        if module.params['id'] is not None:
            update = {}
            for key in ['author', 'title', 'summary']:
                if key in module.params:
                    update[key] = module.params[key]
            # Call to the binding: PUT
            myapi.update_book(module.params['id'], **update)
            result.update(update)

        elif module.params['author'] is not None or module.params['title'] is not None or module.params['summary'] is not None:
            if module.params['author'] is None or module.params['title'] is None or module.params['summary'] is None:
                module.fail_json(msg='author, title and summary are mandatory parameters')

            book = {
                'author': module.params['author'],
                'summary': module.params['summary'],
                'title': module.params['title']
            }

            # Call to the binding: POST
            myapi.create_book(**book)
            result.update(book)

        else:
            # Call to the binding : GET
            books =  {'books': myapi.list_books()
            result.update(books)

    module.exit_json(**result)


if __name__ == '__main__':
    main()
