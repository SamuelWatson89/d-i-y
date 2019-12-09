import pytest
from flask import url_for

class TestApp:

    def test_get_projects(self, client):
        res = client.get(url_for('get_projects'))
        assert res.status_code == 200
        assert res.json == {'template': 'projects.html'}

    def test_login(self, client):
        res = client.get(url_for('login'))
        assert res.status_code == 200
        assert res.json == {'template': 'login.html'}
