broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_routes = {
  'tasks.local': 'local',
  'tasks.api': 'api',
  'tasks.godzilla': 'local'
}
task_annotations = {
  'tasks.local': {'rate_limit': '2/h'},
  'tasks.api': {'rate_limit': '5/m'},
  'tasks.godzilla': {'rate_limit': '2/h'},
}

timezone = 'America/New_York'
