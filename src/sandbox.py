from daytona import Daytona, DaytonaConfig
  
# Define the configuration
config = DaytonaConfig(api_key="dtn_b5aabcf6be1fbf64bb7aa7ff6d14bdf526fa0ec4f408b22622cd50605d099efc")

# Initialize the Daytona client
daytona = Daytona(config)

# Create the Sandbox instance
sandbox = daytona.create()
sandbox.git.clone("https://github.com/xuxiankun/claude-agent", branch="main", path="workspace")
# Run the code securely inside the Sandbox

response = sandbox.process.exec('npm install -g @anthropic-ai/claude-code')
if response.exit_code != 0:
  print(f"Error: {response.exit_code} {response.result}")
else:
  print(response.result)
response = sandbox.process.exec('cd workspace && pip install -e .')
if response.exit_code != 0:
  print(f"Error: {response.exit_code} {response.result}")
else:
  print(response.result)
response = sandbox.process.exec('cd workspace && python src/quick_start.py')
if response.exit_code != 0:
  print(f"Error: {response.exit_code} {response.result}")
else:
  print(response.result)
  