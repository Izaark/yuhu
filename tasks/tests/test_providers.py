from unittest.mock import patch
import pytest
from tasks.tests.baker_recipes import task_recipe, task_recipe_with_due_date
from tasks.providers import (get_tasks, get_task_by_id, delete_task_by_task,
                             get_due_tasks_by_is_active, set_inactive_tasks, get_title_and_email_from_inactive_tasks)


@pytest.mark.django_db
def test_get_tasks():
    task_recipe.make(_quantity=4)
    tasks = get_tasks()
    assert tasks.count() == 4


@pytest.mark.django_db
def test_get_task_by_id(django_assert_num_queries):
    fake_task = task_recipe.make()
    with django_assert_num_queries(num=1):
        task = get_task_by_id(fake_task.id)
        assert task == fake_task


@pytest.mark.django_db
def test_delete_task_by_id():
    fake_task = task_recipe.make()
    tasks = get_tasks()
    assert tasks.count() == 1
    delete_task_by_task(fake_task)
    tasks = get_tasks()
    assert tasks.count() == 0


@pytest.mark.django_db
def test_get_due_tasks_by_is_active():
    task_recipe_with_due_date.make(is_active=True)

    tasks = get_due_tasks_by_is_active()
    assert tasks.count() == 1
    assert tasks[0].is_active is True


@pytest.mark.django_db
def test_set_inactive_tasks():
    task_recipe_with_due_date.make(is_active=True)
    set_inactive_tasks()

    get_inactive_tasks = get_due_tasks_by_is_active(is_active=False)
    assert get_inactive_tasks[0].is_active is False


@pytest.mark.django_db
@patch('tasks.providers.set_inactive_tasks')
def test_get_title_and_email_from_inactive_tasks(mocked_set_inactive_tasks):
    mocked_set_inactive_tasks.return_value = None
    task_recipe_with_due_date.make(is_active=False)
    tasks = get_title_and_email_from_inactive_tasks()

    assert tasks.count() == 1
    assert tasks[0]["title"] is not None
    assert tasks[0]["email"] is not None

