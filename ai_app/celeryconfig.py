
broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/0'

task_routes = {
  'tasks.local': 'local',
  'tasks.api': 'api'
}
task_annotations = {
  'tasks.local': {'rate_limit': '10/h'},
  'tasks.api': {'rate_limit': '10/m'}
}