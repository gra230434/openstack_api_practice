from openstack import connection
conn = connection.Connection(
    auth_url="http://172.17.11.105:5000/v3",
    project_name="demo",
    username="demo",
    password="demo1024")

for container in conn.object_store.containers():
   print(container.name)