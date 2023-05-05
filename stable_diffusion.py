import aiohttp
import aiofiles
import asyncio
from io import BytesIO
from PIL import Image
import logging


model_endpoint = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-2-1"
hf_token = ""
logging.basicConfig(level=logging.DEBUG)

async def gen_api_image(prompt:str):
  payload = {
    "inputs": prompt,
    "parameters": {
      "width": 800,
      "height": 480,
      "guidance_scale": 5
    }
  }
  headers = {
    "Authorization": f"Bearer {hf_token}",
    "Content-Type": "application/json",
    "Accept": "image/png"
  }
  async with aiohttp.ClientSession() as session:
    async with session.post(model_endpoint, headers=headers, json=payload) as response:
      logging.info("Response received.")
      logging.info(f"Status: {response.status}")
      logging.info(f"Headers: {response.headers}")
      if response.status == 200:
        async with aiofiles.open("test_image.png", mode='wb') as f:
          await f.write(await response.read())

# async def gen_local_image(prompt:str):


# Main Function

# Query the Hugging Face Stability AI API
logging.info("Submitting request")
asyncio.run(gen_api_image("Mothra in the style of a woodcut."))
