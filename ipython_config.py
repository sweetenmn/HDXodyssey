#python_config.py

c = get_config()

# Allow all IP addresses to use the service and run it on port 8888.
c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8888

# Don't load the browser on startup.
c.NotebookApp.open_browser = False
