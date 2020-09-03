#!/usr/bin/python3
# -*- coding: utf-8 -*-


# Copyright 2020 Colton Hughes <colton.hughes@firemon.com>

# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


ANSIBLE_METADATA = {'status': ['stableinterface'],
                    'supported_by': 'community',
                    'version': '1.0'
                    }

DOCUMENTATION = '''
---
module: build_jwt
short_description: Module to build a JWT token
version_added: "2.9"
description:
  - "This module generates a basic JWT token specifically formatted for Zoom Api"
options:
  secret:
    description:
      - Secret to sign the JWT payload
    required: true
  issuer:
    description:
      - Issuer to be included in the payload
    required: true
  algorithm:
    description:
      - Algorithm to use. (Currently only supports HS256)
    required: true
  expiration:
    description:
      - Expiration duration in seconds
    required: true
'''

EXAMPLES = '''
# Generate a basic JWT token
- name: Generate JWT Token
  build_jwt:
    secret: mysecret1234!#@
    issuer: issuer1234!
    expiration: 13433
    algorithm: HS256
'''

RETURN = '''
token:
  description: The JWT token
  type: str
  returned: changed
expires_in:
  description: Expiration defined in play
  type: str
  returned: always
'''
import traceback

try:
  import jwt
  HAS_LIB = True
except:
  HAS_LIB = False
  LIB_IMP_ERR = traceback.format_exc()


from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.basic import missing_required_lib


def run_module():
  module_args = dict(
    secret=dict(type='str', required=True, no_log=True),
    issuer=dict(type='str', required=True),
    expiration=dict(type='str', required=True),
    algorithm=dict(type='str', choices=['HS256'], required=True)
  )

  module = AnsibleModule(
    argument_spec=module_args,
    supports_check_mode=False
  )

  if not HAS_LIB:
    module.fail_json(msg=missing_required_lib("jwt"), exception=LIB_IMP_ERR)

  secret = module.params['secret']
  issuer = module.params['issuer']
  expiration = module.params['expiration']
  algorithm = module.params['algorithm']

  result = dict(
    changed=False,
    token='',
    expires_in=expiration
  )

  if algorithm.lower() == 'hs256':
    try:
      encoded_jwt = jwt.encode(
        {
          "iss": issuer,
          "exp": expiration
        },
        secret,
        algorithm=algorithm)
      
      result['token'] = encoded_jwt.decode("utf-8")
      result['changed'] = True
      module.exit_json(**result)
    except Exception as error:
      
      module.fail_json(msg=error, **result)

def main():
  run_module()
    
if __name__ == '__main__':
  main()