# This file is a part of Arjuna
# Copyright 2015-2020 Rahul Verma

# Website: www.RahulVerma.net

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#   http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from oauthlib.oauth2 import BackendApplicationClient, MobileApplicationClient
from requests_oauthlib import OAuth2Session

from .session import HttpSession

from bs4 import BeautifulSoup
import urllib.parse

class OAuthSession(HttpSession):
    '''
        Base Class for all types of OAuth Http Sessions.

        Arguments:
            session: `requests_oauthlib` session object
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
    '''

    def __init__(self, *, session, url):
        super().__init__(url=url, _auto_session=False)
        self._set_session(session)
        self.__token = None

    @property
    def token(self):
        '''
            OAuth Token created by this session.
        '''
        return self.__token

    def _set_outh_token(self, token):
        self.__token = token
        self._session.headers.update({'Authorization': 'Bearer ' + self.token})

    def create_new_session(self, url, *, content_type=None):
        '''
            Create a new HttpSession object. OAuth token of this session is attached to the new session.

            Arguments:
                url: Base URL for the new HTTP session.
                content-type: Default request content type for the new session.
        '''
        return HttpSession(url=url, oauth_token=self.token, content_type=content_type)


class OAuthClientGrantSession(OAuthSession):
    '''
        Creates token using OAuth's Resource Owner Client Credentials Grant Type.
        Uses BackendApplicationClient from requests_oauthlib.

        Keyword Arguments:
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            client_id: Client ID
            client_secret: Client Secret
            token_url: Token URL
    '''

    def __init__(self, *, url, client_id, client_secret, token_url):
        client = BackendApplicationClient(client_id=client_id)
        oauth = OAuth2Session(client=client)
        super().__init__(session=oauth, url=url)
        token = oauth.fetch_token(token_url=token_url, 
                                  client_id=client_id,
                                  client_secret=client_secret)
        self._set_outh_token(token)


class OAuthImplicitGrantSession(OAuthSession):
    '''
        Creates token using OAuth's Implicit Code Grant Type.
        Uses MobileApplicationClient from requests_oauthlib.

        Keyword Arguments:
            url: Base URL for this HTTP session. If relative path is used as a route in sender methods like `.get`, then this URL is prefixed to their provided routes.
            client_id: Client ID
            scope: Scope
            redirect_uri: Redirect URI
            auth_url: Authorization URL
            auth_handler: A callback function to handle custom authroization logic. It will be called by providing session object, authorization URL and auth_args.
            **auth_args: Arbitray key-value pairs to be passed as arguments to the auth_handler callback.

        Note:
            Some sample auth_handler signatures:

                .. code-block:: python

                    auth_handler_1(oauth_session, auth_url, **kwargs)
                    auth_handler_2(oauth_session, auth_url, some_arg=None, another_arg="some_def_value")

    '''
    def __init__(self, *, url, client_id, scope, redirect_uri=None, auth_url, auth_handler=None, **auth_args):
        oauth = OAuth2Session(
            client=MobileApplicationClient(client_id=client_id),
            scope=scope,
            redirect_uri=redirect_uri,
        )
        super().__init__(session=oauth, url=url)

        auth_url, state = oauth.authorization_url(auth_url)

        token = None
        if auth_handler is None:
            token = outh.token_from_fragment(callback_url)
        else:
            token = auth_handler(self, auth_url, **auth_args)
        self._set_outh_token(token)
