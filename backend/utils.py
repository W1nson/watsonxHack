
# streamming on to console: 
def stream_to_console(agent, inputs, stream_mode="messages"):
    for chunk, metadata in agent.stream(inputs, stream_mode=stream_mode):
        if chunk.content:
            print(chunk.content, end="", flush=True)