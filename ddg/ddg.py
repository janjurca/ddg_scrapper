from duckduckgo_search import DDGS
import argparse
import os
from PIL import Image
import uuid
import json

parser = argparse.ArgumentParser(description='Search for images on DuckDuckGo')
parser.add_argument('keywords', type=str, nargs='+',)
parser.add_argument('--region', type=str, default="wt-wt")
parser.add_argument('--safesearch', type=str, default="off")
parser.add_argument('--size', type=str, default=None)
parser.add_argument('--color', type=str, default="Monochrome")
parser.add_argument('--type_image', type=str, default=None)
parser.add_argument('--layout', type=str, default=None)
parser.add_argument('--license_image', type=str, default=None)
parser.add_argument('--output-dir', type=str, default="output")
args = parser.parse_args()

output_dir = os.path.join(args.output_dir, "_".join(args.keywords))

os.makedirs(output_dir, exist_ok=True)

with DDGS() as ddgs:
    keywords = ' '.join(args.keywords)
    ddgs_images_gen = ddgs.images(
      keywords,
      region=args.region,
      safesearch=args.safesearch,
      size=args.size,
      color=args.color,
      type_image=args.type_image,
      layout=args.layout,
      license_image=args.license_image,
    )
    for r in ddgs_images_gen:
        uuid = uuid.uuid4()
        title = r['title']
        url = r['url']
        Image.open(ddgs.get_image(url)).save(os.path.join(output_dir, f"{uuid}.jpg"))
        with open(os.path.join(output_dir, f"{uuid}.json"), "w") as f:
            json.dump(r, f)
