from model_bakery.recipe import Recipe

task_recipe = Recipe(
    "tasks.Task",
    title="logs en datadog",
    email="user_yuhu@yuhu.com.mx",
    description="Create logs for app monitoring",
)