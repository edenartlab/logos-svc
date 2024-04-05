from logos.llm import LLM
from pydantic import BaseModel


class OutputSchema(BaseModel):
    """
    Output schema for LLM
    """

    description: str
    numimages: int


llm = LLM(model="gpt-4-1106-preview", system_message="You are an AI assistant")

prompt = "Describe this image. In description, tell me what the image is about. In numimages, tell me how many images are attached."

result = llm(
    prompt,
    image="https://edenartlab-prod-data.s3.us-east-1.amazonaws.com/27d5f97d76bb6550cec0f82296587bbc1ac1d66d34cfa824f3056046abe8c0e1.jpg",
    output_schema=OutputSchema,
    params={"max_tokens": 1000},
)

print(result)
