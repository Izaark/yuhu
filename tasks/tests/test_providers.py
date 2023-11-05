import pytest
from tasks.tests.baker_recipes import task_recipe
from tasks.providers import get_tasks, get_task_by_id, delete_task_by_task


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


