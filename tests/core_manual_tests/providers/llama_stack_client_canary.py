import asyncio

import agentops
import os
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient
from llama_stack_client.types import UserMessage
from llama_stack_client.lib.inference.event_logger import EventLogger

load_dotenv()

agentops.init(default_tags=["llama-stack-client-provider-test"])

host = "0.0.0.0" # LLAMA_STACK_HOST
port = 5001 # LLAMA_STACK_PORT

full_host = f"http://{host}:{port}"

client = LlamaStackClient(
    base_url=f"{full_host}",
)

response = client.inference.chat_completion(
    messages=[
        UserMessage(
            content="hello world, write me a 3 word poem about the moon",
            role="user",
        ),
    ],
    model_id="meta-llama/Llama-3.2-3B-Instruct",
    stream=False
)

async def stream_test():
  response = client.inference.chat_completion(
      messages=[
          UserMessage(
              content="hello world, write me a 3 word poem about the moon",
              role="user",
          ),
      ],
      model_id="meta-llama/Llama-3.2-3B-Instruct",
      stream=True
  )

  async for log in EventLogger().log(response):
      log.print()


async def main():
    await stream_test()

agentops.end_session(end_state="Success")
