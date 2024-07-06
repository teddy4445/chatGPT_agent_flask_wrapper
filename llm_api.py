# library import
import json
from openai import OpenAI


class LLMAPI:
    """
    A class to manage LLM querying
    """

    # CONSTS #
    LLM_NAMES = ["gpt-3.5-turbo", "gpt-4"]
    LLM_CONTEXT = "Given the CSV data: {}"
    # END - CONSTS #

    def __init__(self,
                 key: str):
        self.client = OpenAI(api_key=key)
        self.my_assistant = self.client.beta.assistants.create(
            model="gpt-4",
            instructions="Write context here.",
            name="Dreamboat agent",
            tools=[{"type": "code_interpreter"}]
        )
        self.my_thread = self.client.beta.threads.create()

    def get_embedding(self,
                      text: str,
                      model: str = "text-embedding-ada-002"):
        text = text.replace("\n", " ")
        return self.client.embeddings.create(input=[text], model=model).data[0].embedding

    def query(self,
              context: str,
              text: str,
              temperature: float = 0.2):
        messages = [{"role": "system", "content": context},
                    {"role": "user", "content": text}]
        answers = self.client.chat.completions.create(model=LLMAPI.LLM_NAMES[1],
                                                      messages=messages,
                                                      temperature=temperature)
        return str(answers.choices[0].message.content)

    def data_related_chat(self,
                          csv_text: str,
                          chat_so_far: list,
                          last_text: str,
                          temperature: float = 0,
                          context_message: str = ""):
        if context_message == "":
            context_message = LLMAPI.LLM_CONTEXT
        user_message = self.client.beta.threads.messages.create(
            thread_id=self.my_thread.id,
            role="user",
            content=last_text
        )
        my_run = self.client.beta.threads.runs.create(
            thread_id=self.my_thread.id,
            assistant_id=self.my_assistant.id,
            instructions=context_message.format(csv_text)
        )
        while my_run.status != "completed":
            keep_retriving_run = self.client.beta.threads.runs.retrieve(
                thread_id=self.my_thread.id,
                run_id=my_run.id
            )

            if keep_retriving_run.status == "completed":
                break

        all_messages = self.client.beta.threads.messages.list(
            thread_id=self.my_thread.id
        )
        return all_messages.data[0].content[0].text.value.replace("\n", "<br>")
