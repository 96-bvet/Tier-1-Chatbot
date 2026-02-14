import os
import pytest
from unittest.mock import patch, MagicMock
from tier1_chatbot.chatbot import (
    check_knowledge_base,
    KNOWLEDGE_BASE,
    get_ai_response,
    search_external_info,
    create_syncro_ticket
)

class TestKnowledgeBase:
    """Test knowledge base functionality."""
    
    def test_check_knowledge_base_password_reset(self):
        """Test password reset query matches knowledge base."""
        matched_key, kb_item = check_knowledge_base("I need a password reset")
        assert matched_key == "password reset"
        assert kb_item is not None
        assert "portal" in kb_item["response"].lower()
    
    def test_check_knowledge_base_email_issue(self):
        """Test email issue query matches knowledge base."""
        matched_key, kb_item = check_knowledge_base("I have an email issue")
        assert matched_key == "email issue"
        assert kb_item is not None
        assert "spam" in kb_item["response"].lower()
    
    def test_check_knowledge_base_printer_issue(self):
        """Test printer issue query matches knowledge base."""
        matched_key, kb_item = check_knowledge_base("printer issue with my device")
        assert matched_key == "printer issue"
        assert kb_item is not None
        assert "restart" in kb_item["response"].lower()
    
    def test_check_knowledge_base_no_match(self):
        """Test query with no knowledge base match."""
        matched_key, kb_item = check_knowledge_base("how do I install software")
        assert matched_key is None
        assert kb_item is None

class TestChatEndpoint:
    """Test chat endpoint functionality."""
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'healthy'
    
    def test_chat_password_reset(self, client):
        """Test chat endpoint with password reset query."""
        response = client.post('/chat', json={
            'message': 'I need help with password reset',
            'context': ''
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data
        assert 'context' in data
        assert 'portal' in data['response'].lower()
    
    def test_chat_email_issue(self, client):
        """Test chat endpoint with email issue query."""
        response = client.post('/chat', json={
            'message': 'having an email issue',
            'context': ''
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data
        assert 'spam' in data['response'].lower() or 'settings' in data['response'].lower()
    
    def test_chat_printer_issue(self, client):
        """Test chat endpoint with printer issue query."""
        response = client.post('/chat', json={
            'message': 'my printer issue is not resolved',
            'context': ''
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data
        assert 'restart' in data['response'].lower() or 'network' in data['response'].lower()
    
    @patch('tier1_chatbot.chatbot.get_ai_response')
    def test_chat_unknown_query_uses_ai(self, mock_ai, client):
        """Test chat endpoint uses AI for unknown queries."""
        mock_ai.return_value = "I can help you with that."
        
        response = client.post('/chat', json={
            'message': 'how do I configure my VPN',
            'context': ''
        })
        assert response.status_code == 200
        data = response.get_json()
        assert 'response' in data
        mock_ai.assert_called_once()

class TestUtilityFunctions:
    """Test utility functions."""
    
    @patch('tier1_chatbot.chatbot.openai.ChatCompletion.create')
    def test_get_ai_response(self, mock_openai):
        """Test AI response generation."""
        mock_openai.return_value = MagicMock(
            choices=[MagicMock(message={'content': 'Test response'})]
        )
        
        response = get_ai_response("test message", api_key="test-key")
        assert response == "Test response"
        mock_openai.assert_called_once()
    
    @patch('tier1_chatbot.chatbot.openai.ChatCompletion.create')
    def test_get_ai_response_exception(self, mock_openai):
        """Test AI response generation with exception."""
        mock_openai.side_effect = Exception("API error")
        
        response = get_ai_response("test message", api_key="test-key")
        assert "AI service error" in response
    
    @patch.dict(os.environ, {}, clear=True)
    @patch('tier1_chatbot.chatbot.openai')
    def test_get_ai_response_no_api_key(self, mock_openai):
        """Test AI response generation without API key."""
        mock_openai.api_key = None
        response = get_ai_response("test message", api_key=None)
        assert "not configured" in response.lower()
    
    @patch('tier1_chatbot.chatbot.requests.get')
    def test_search_external_info_success(self, mock_get):
        """Test external search with successful response."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'organic_results': [{'snippet': 'Test snippet'}]
        }
        mock_get.return_value = mock_response
        
        result = search_external_info("test query", api_key="test-key")
        assert result == "Test snippet"
    
    @patch('tier1_chatbot.chatbot.requests.get')
    def test_search_external_info_no_results(self, mock_get):
        """Test external search with no results."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'organic_results': []}
        mock_get.return_value = mock_response
        
        result = search_external_info("test query", api_key="test-key")
        assert result == "No external info found."
    
    @patch('tier1_chatbot.chatbot.requests.get')
    def test_search_external_info_exception(self, mock_get):
        """Test external search with exception."""
        mock_get.side_effect = Exception("Network error")
        
        result = search_external_info("test query", api_key="test-key")
        assert "Search failed" in result
        assert "Network error" in result
    
    def test_search_external_info_no_api_key(self):
        """Test external search without API key."""
        result = search_external_info("test query", api_key=None)
        assert result == "No search API key configured."
    
    @patch('tier1_chatbot.chatbot.requests.post')
    def test_create_syncro_ticket_success(self, mock_post):
        """Test Syncro ticket creation with success."""
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {'id': '12345'}
        mock_post.return_value = mock_response
        
        result = create_syncro_ticket(
            "Test Subject", 
            "Test Description",
            subdomain="test",
            api_key="test-key"
        )
        assert "12345" in result
        assert "successfully" in result.lower()
    
    @patch('tier1_chatbot.chatbot.requests.post')
    def test_create_syncro_ticket_failure(self, mock_post):
        """Test Syncro ticket creation with failure."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad Request"
        mock_post.return_value = mock_response
        
        result = create_syncro_ticket(
            "Test Subject",
            "Test Description",
            subdomain="test",
            api_key="test-key"
        )
        assert "failed" in result.lower()
    
    @patch('tier1_chatbot.chatbot.requests.post')
    def test_create_syncro_ticket_exception(self, mock_post):
        """Test Syncro ticket creation with exception."""
        mock_post.side_effect = Exception("Connection timeout")
        
        result = create_syncro_ticket(
            "Test Subject",
            "Test Description",
            subdomain="test",
            api_key="test-key"
        )
        assert "Ticket creation failed" in result
        assert "Connection timeout" in result
    
    def test_create_syncro_ticket_no_config(self):
        """Test Syncro ticket creation without configuration."""
        result = create_syncro_ticket(
            "Test Subject",
            "Test Description",
            subdomain=None,
            api_key=None
        )
        assert "not configured" in result.lower()
