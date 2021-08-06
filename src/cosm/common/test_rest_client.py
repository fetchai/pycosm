from cosm.common.rest_client import RestClient
from unittest import TestCase
from unittest.mock import Mock, patch
from requests import Session, Response
from urllib.parse import urlencode


class QueryTests(TestCase):
    @patch("requests.session", spec=Session)
    @patch("cosm.common.rest_client.MessageToDict")
    def test_get_pass(self, messageToDict_mock, session_mock):
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 200
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json
        session_mock.return_value.get.return_value = resp
        client.get(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)

        expected_url = f"{rest_address}{request_url_path}&{urlencode(request_json)}"
        session_mock.return_value.get.assert_called_once_with(url=expected_url)

    @patch("requests.session", spec=Session)
    @patch("cosm.common.rest_client.MessageToDict")
    def test_get_error(self, messageToDict_mock, session_mock):
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 400
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json
        session_mock.return_value.get.return_value = resp

        with self.assertRaises(Exception) as context:
            client.get(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)
        self.assertTrue("Error when sending a GET request" in str(context.exception))

    @patch("requests.session", spec=Session)
    @patch("cosm.common.rest_client.MessageToDict")
    def test_post_pass(self, messageToDict_mock, session_mock):
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 200
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json

        session_mock.return_value.post.return_value = resp
        client.post(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)

        _, kwargs = session_mock.return_value.post.call_args
        headers = kwargs["headers"]
        assert (
            headers.items()
            >= {
                "Content-type": "application/json",
                "Accept": "application/json",
            }.items()
        )
        assert kwargs["url"] == f"{rest_address}{request_url_path}"
        assert kwargs["json"] == request_json

    @patch("requests.session", spec=Session)
    @patch("cosm.common.rest_client.MessageToDict")
    def test_post_error(self, messageToDict_mock, session_mock):
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        request_url_path = "/my/weird/url/path"
        resp = Mock(spec=Response)
        resp.status_code = 400
        resp.content = "dfdffdss".encode(encoding="utf8")

        request = "some weird request value"
        request_json = {"a": 1, "b": "something"}
        messageToDict_mock.return_value = request_json

        session_mock.return_value.post.return_value = resp

        with self.assertRaises(Exception) as context:
            client.post(request_url_path, request)

        messageToDict_mock.assert_called_once_with(request)
        self.assertTrue("Error when sending a POST request" in str(context.exception))

    @patch("requests.session", spec=Session)
    def test_session_close_on_object_deletion(self, session_mock):
        rest_address = "some url"
        client = RestClient(rest_address)

        session_mock.assert_called_once_with()
        assert client.rest_address == rest_address

        del client
        session_mock.return_value.close.assert_called_once_with()