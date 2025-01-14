
from chats.chat_utils import verify_gemini_api_key
from unittest.mock import patch, MagicMock
import requests

def test_gemini_api_key():
    result, msg = verify_gemini_api_key("")
    assert not result
    assert msg == "No Attribute value provided"

    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {}
        result, message = verify_gemini_api_key("valid_api_key")
        assert result
        assert message == "Valid API Key"
    
    with patch("requests.get", side_effect=requests.exceptions.ConnectTimeout):
        result, msg = verify_gemini_api_key("valid_api_key")
        assert not result
        assert msg == "Connection error occurred"
    
    with patch("requests.get", side_effect=requests.exceptions.Timeout):
        result, msg = verify_gemini_api_key("valid_api_key")
        assert not result
        assert msg == "The request timed out"

    with patch("requests.get", side_effects=requests.exceptions.HTTPError) as mock_get:
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {'error': {'message': 'Not Found'}}
        result, message = verify_gemini_api_key("valid_api_key")
        assert not result
        assert message == "Error: Not Found"

    with patch("requests.get") as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 403  
        mock_response.json.return_value = {"error": {"message": "Invalid API Key"}}
        mock_get.return_value = mock_response
        result, message = verify_gemini_api_key("valid_api_key")
        assert not result
        assert message == "Error: Invalid API Key" 

import pytest
from unittest import mock
import os
import streamlit as st
from chats.chat_utils import verify_module_config_smartdataframe

@pytest.fixture
def mock_dependencies(mocker):
    mocker.patch("os.environ.get", return_value="fake_api_key")  

def test_verify_module_config_smartdataframe_missing_api_key(mocker):
    gen_api = None
    result, message = verify_module_config_smartdataframe(gen_api)
    assert result is False
    assert message == "Environment variable 'GEMINI_API_KEY' is missing"

    mocker.patch("os.environ.get", return_value=None)  
    result, message = verify_module_config_smartdataframe("valid_api_key")
    assert result is False
    assert message == "AttributeError: 'NoneType' object has no attribute 'chat'"

    mocker.patch("chats.chat.gen_api", side_effect=ModuleNotFoundError)  
    result, message = verify_module_config_smartdataframe("valid_api_key")
    assert result is False
    assert message == "AttributeError: 'NoneType' object has no attribute 'chat'"

    mocker.patch("chats.chat.gen_api", side_effect=Exception("Something went wrong")) 
    result, message = verify_module_config_smartdataframe("valid_api_key")
    assert result is False
    assert message == "AttributeError: 'NoneType' object has no attribute 'chat'"
