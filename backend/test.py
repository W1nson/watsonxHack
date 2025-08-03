from llm import ollama_model, watsonx_model






def test_llm(name, input): 
    if name == "ollama":
        result = ollama_model.stream(input)
        for chunk in result:
            print(chunk.content, end="", flush=True)
    elif name == "watsonx":
        result = watsonx_model.stream(input)
        for chunk in result:
            print(chunk.content, end="", flush=True)
    else:
        raise ValueError("Invalid LLM name")
        


if __name__ == "__main__":
    test_llm("watsonx", "Who are you?")
