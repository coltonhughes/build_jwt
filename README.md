# Module Documentation
This module is quite simple.
It takes data in the form of inputs to generate a JWT token and is returned to you.

## Example
```
- name: Generate JWT Token
  build_jwt:
    secret: mysecret1234!#@
    issuer: issuer1234!
    expiration: 13433
    algorithm: HS256
```
This is a very simple module that I put very little effort in perfecting.  If issues arise feel free to open them or fork and modify at your own discretion.