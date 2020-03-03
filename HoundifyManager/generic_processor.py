from abc import ABC, abstractmethod
import requests
import httpx
import hashlib
import base64
import hmac
import time
import uuid


HOUNDIFY_BASE_TEXT_API = "https://api.houndify.com/v1/text"
COMPONENTS_FOLDER_NAME = "components"


class HoundifyProcessor(ABC):
    def __init__(self, client_id, client_key, session_id):
        self.request_headers = self._build_request_headers(client_id=client_id,
                                                           client_key=client_key,
                                                           session_id=session_id)

    @staticmethod
    def _build_request_headers(client_id, client_key, session_id):
        """
        Arguments:
            client_id (string): Obtained when you register a client.
            client_key (string): Obtained when you register a client.
            session_id (string): Unique session for context user.
        Returns:

        """

        timestamp = str(int(time.time()))

        hound_request_auth = session_id + ";" + str(uuid.uuid4())

        h = hmac.new(bytearray(base64.urlsafe_b64decode(client_key)),
                     (hound_request_auth + timestamp).encode("utf-8"),
                     hashlib.sha256)

        signature = base64.urlsafe_b64encode(h.digest()).decode("utf-8")

        hound_client_auth = client_id + ";" + timestamp + ";" + signature

        headers = {
            "Hound-Request-Authentication": hound_request_auth,
            "Hound-Client-Authentication": hound_client_auth
        }

        return headers

    @abstractmethod
    def process_request(self, text, language_code="en"):
        """
        Returns bot output for user input.

        Using the same `session_id` between requests allows continuation
        of the conversation.

        Arguments:
            session_id (string): Unique session for context user.
            text (string): User input.
            language_code (string): Context language.
        Returns:
            Houndify JSON response. (dict)
        """
        pass


class HoundifyAsyncProcessor(HoundifyProcessor):
    def __init__(self, client_id, client_key, session_id):
        super(HoundifyAsyncProcessor, self).__init__(client_id, client_key,
                                                     session_id)

        self.session = httpx.Client(headers=self.request_headers)

    def process_request(self, text, language_code="en"):
        """
        Returns bot output for user input.

        Using the same `session_id` between requests allows continuation
        of the conversation.

        Arguments:
            session_id (string): Unique session for context user.
            text (string): User input.
            language_code (string): Context language.
        Returns:
            Houndify JSON response. (dict)
        """

        request_params = {"query": text}

        response = self.session.post(HOUNDIFY_BASE_TEXT_API, params=request_params)

        response.raise_for_status()

        return response.json()


class HoundifySyncProcessor(HoundifyProcessor):
    def __init__(self, client_id, client_key, session_id):
        super(HoundifySyncProcessor, self).__init__(client_id, client_key,
                                                    session_id)

        self.session = requests.session()
        self.session.headers = self.request_headers

    def process_request(self, text, language_code="en"):
        """
        Returns bot output for user input.

        Using the same `session_id` between requests allows continuation
        of the conversation.

        Arguments:
            session_id (string): Unique session for context user.
            text (string): User input.
            language_code (string): Context language.
        Returns:
            Houndify JSON response. (dict)
        """

        request_params = {"query": text}

        response = self.session.post(HOUNDIFY_BASE_TEXT_API, params=request_params)

        response.raise_for_status()

        return response.json()
