import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from tasks.tests.baker_recipes import task_recipe


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def get_token(api_client):
    response = api_client.post(
        '/api/v1/users', {'username': 'yuhu_test', 'password': 'yuhupass'}, format='json'
    )
    return response.data['token']


@pytest.mark.django_db
def test_task_list_api_view(api_client, get_token):
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_token)
    task_recipe.make(_quantity=4)
    response = api_client.get('/api/v1/tasks')

    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()["results"]) == 4


@pytest.mark.django_db
def test_task_list_detail_api_view(api_client, get_token):
    task = task_recipe.make()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_token)
    response = api_client.get(f"/api/v1/tasks/{task.id}")
    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert json_data["id"] == task.id
    assert json_data["title"] == task.title
    assert json_data["email"] == task.email
    assert json_data["description"] == task.description
    assert json_data["is_active"] == task.is_active


@pytest.mark.django_db
def test_task_partial_update_api_view(api_client, get_token):
    task = task_recipe.make(title="celery tasks", description='celery description')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_token)

    assert task.title == 'celery tasks'
    assert task.description == 'celery description'

    update_data = {
        'title': 'title updated',
        'description': 'description updated'
    }

    response = api_client.patch(f"/api/v1/tasks/{task.id}", update_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    task.refresh_from_db()
    assert task.title == 'title updated'
    assert task.description == 'description updated'


@pytest.mark.django_db
def test_task_update_api_view(api_client, get_token):
    task = task_recipe.make(title="celery tasks", description='celery description')
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_token)

    assert task.title == 'celery tasks'
    assert task.description == 'celery description'

    update_data = {
        "title": "title celery uddated",
        "email": "updated@gmail.com",
        "description": "celery description updated",
        "due_date": "2023-04-11 11:00:00"
    }

    response = api_client.put(f"/api/v1/tasks/{task.id}", update_data, format='json')
    assert response.status_code == status.HTTP_200_OK

    task.refresh_from_db()
    assert task.title == 'title celery uddated'
    assert task.email == 'updated@gmail.com'
    assert task.description == 'celery description updated'


@pytest.mark.django_db
def test_task_delete_api_view(api_client, get_token):
    task = task_recipe.make()
    api_client.credentials(HTTP_AUTHORIZATION='Token ' + get_token)
    response = api_client.delete(f"/api/v1/tasks/{task.id}")

    assert response.status_code == status.HTTP_204_NO_CONTENT
