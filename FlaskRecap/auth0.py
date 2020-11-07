import json
from jose import jwt
from urllib.request import urlopen

# Configuration
# UPDATE THIS TO REFLECT YOUR AUTH0 ACCOUNT
AUTH0_DOMAIN = 'young-fsnd.au.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'image'


class AuthError(Exception):
    '''
    AuthError Exception
    A standardized way to communicate auth failure modes
    '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# PASTE YOUR OWN TOKEN HERE
# MAKE SURE THIS IS A VALID AUTH0 TOKEN FROM THE LOGIN FLOW
token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlA1ek1qUTQ3RlJOUGNnSTh3VDMtYSJ9.eyJpc3MiOiJodHRwczovL3lvdW5nLWZzbmQuYXUuYXV0aDAuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA0Mzk4NjY4NjI5MzYyMTI5OTg3IiwiYXVkIjpbImltYWdlIiwiaHR0cHM6Ly95b3VuZy1mc25kLmF1LmF1dGgwLmNvbS91c2VyaW5mbyJdLCJpYXQiOjE2MDM1OTU5ODcsImV4cCI6MTYwMzYwMzE4NywiYXpwIjoidzR2ZUo3RHRPdXMyNUJPbk5tMjE5aGdsMHFaa3RiWW0iLCJzY29wZSI6Im9wZW5pZCBwcm9maWxlIGVtYWlsIn0.SvIO5VRMqk4A7_KA801dAL3U_cBaawNqH2uhWM-CrhqMa9PcEqfQFcwXdrgJR3sGNVtNRiLZgc_3FDmwMuoXmpCu64ieyR6XXRwB26LIAnDS4Bi-Lk4vlyWZnIJztYDJ2XSiiTdMfNqiNK_bTN_1FZAf3pioBcATA2397lnNyLDMOI5NcCwbP3mAGhqhVXsZ-EcgJB-E2sY1TisAIgqau1rJTsQwq1KTjCk0j4GiPMxCzHqSisobaLC-hlywjlWHfd0BEk8u5955k74XH8PZgo4eoVWGqUQqbGXYRPxRj89l7SYXxgBcXtd5VWQuauYb6B5SqrWaUV3u-FBA9tPLBg"


# Auth Header
def verify_decode_jwt(token):
    # GET THE PUBLIC KEY FROM AUTH0
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    print(jwks)
    # GET THE DATA IN THE HEADER
    unverified_header = jwt.get_unverified_header(token)
    print(unverified_header)
    # CHOOSE OUR KEY
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    print(rsa_key)
    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
    }, 400)


if __name__ == "__main__":
    verify_decode_jwt(token)
