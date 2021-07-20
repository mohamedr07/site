from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from ldap3 import Server, Connection
import jwt
from website.settings import SECRET_KEY, LDAP_AUTH_URL, LDAP_AUTH_SEARCH_BASE
import datetime
import json

class LoginView(APIView):
    def post(self, request):

        username = request.data['username']
        password = request.data['password']

        server = Server(LDAP_AUTH_URL)
        c = Connection(server)

        c.open()
        c.bind()

        if c.bind():
            user_search_filter = '(uid={})'.format(username)
            c.search(search_base=LDAP_AUTH_SEARCH_BASE,
                        search_filter= user_search_filter,
                        search_scope='SUBTREE', attributes=['*'])
        print(json.loads(c.response_to_json()))
        if(c.response == []):
            return Response('error username or password is incorrect')
        username = c.response[0]['dn']
        user = {
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=60)
            }
        encoded = jwt.encode(user, SECRET_KEY, algorithm="HS256")
        if c.rebind(user=username, password=password):
            print(encoded)
            c.unbind()
            return Response(encoded, status=status.HTTP_202_ACCEPTED)
        else:
            return Response('connection error try again')
