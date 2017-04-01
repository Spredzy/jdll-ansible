#!/usr/bin/python

from ansible.module_utils.basic import *
from jdll import API

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

    myapi = API()
    result = {
        'changed': True
    }

    if module.params['state'] == 'absent':
        if 'id' not in module.params:
            module.fail_json(msg='id parameter is mandatory')
        myapi.delete_book(module.params['id'])

    else:
        if module.params['id'] is not None:
            update = {}
            for key in ['author', 'title', 'summary']:
                if key in module.params:
                    update[key] = module.params[key]
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

            myapi.create_book(**book)
            result.update(book)

        else:
            result.update({'books': myapi.list_books()})

    module.exit_json(**result)


if __name__ == '__main__':
    main()
