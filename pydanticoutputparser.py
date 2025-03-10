from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field

load_dotenv()

llm = HuggingFaceEndpoint(
    repo_id = "google/gemma-2-2b-it",
    task="text-generation"
)

model = ChatHuggingFace(llm=llm)

class Person(BaseModel):
    name : str = Field(description="Name of the person")
    age : int = Field(description="Age of the person", gt=18)
    city: str = Field(description="Name of the city the person belongs to")


parser = PydanticOutputParser(pydantic_object=Person)

template = PromptTemplate(
    template = "Generate the name, age and city of a fictional person from {place} \n {format_instruction}",
    input_variables= ["place"],
    partial_variables={"format_instruction": parser.get_format_instructions()}
)

prompt = template.invoke({"place": "India"})

result = model.invoke(prompt)

final_result = parser.parse(result.content)

print(final_result)
