import subprocess

input_data = "test_data"
result = subprocess.run(
    ["node", "loader.js", '1' , '2'],
    capture_output=True,
    text=True
)
print(result.stdout.strip())
