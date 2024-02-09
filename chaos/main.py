import requests

request = requests.post("http://127.0.0.1:3000/process_data", json={
  "data": ["Hello", 1, 5, "World", "!"]
}).json()
print(request)
assert request == {
  "string_len": 11,
  "int_sum": 6
}