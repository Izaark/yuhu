from model_bakery.recipe import Recipe
from django.utils import timezone


task_recipe = Recipe(
    "tasks.Task",
    title="logs en datadog",
    email="user_yuhu@yuhu.com.mx",
    description="Create logs for app monitoring",
    is_active=True,

)

task_recipe_with_due_date = task_recipe.extend(
    due_date=timezone.now() - timezone.timedelta(days=1),
)