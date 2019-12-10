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

    def test_signup(self, client):
        res = client.get(url_for('signup'))
        assert res.status_code == 200
        assert res.json == {'template': 'signup.html'}

    def test_add_project(self, client):
        res = client.get(url_for('add_project'))
        assert res.status_code == 200
        assert res.json == {'template': 'addproject.html'}

    def test_view_project(self, client):
        res = client.get(url_for('view_project', projects_id='1'))
        assert res.status_code == 200
        assert res.json == {'template': 'viewproject.html'}

    def test_edit_projects(self, client):
        res = client.get(url_for('edit_projects', projects_id='1'))
        assert res.status_code == 200
        assert res.json == {'template': 'editproject.html'}

    def test_edit_image(self, client):
        res = client.get(url_for('edit_image', projects_id='1'))
        assert res.status_code == 200
        assert res.json == {'template': 'editimage.html'}

    def test_about(self, client):
        res = client.get(url_for('about'))
        assert res.status_code == 200
        assert res.json == {'template': 'about.html'}

    def test_contact(self, client):
        res = client.get(url_for('contact'))
        assert res.status_code == 200
        assert res.json == {'template': 'contact.html'}
