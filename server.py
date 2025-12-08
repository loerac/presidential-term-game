from textual_serve.server import Server

server = Server("python -m app", title="President Term Quiz")
server.serve()
