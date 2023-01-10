import requests
import json
from PIL import Image, ImageDraw, ImageFont

CLIENT_ID = "PlkJdbPLeu_O8swfi415pNXDDy3xz3qHkucjGKsYeXU"

country_codes = json.load(open("country_codes.json", "r"))

queries = ["mountains"]

for query in queries:
    print(f"Getting {query} images...")
    response = requests.get(f"https://api.unsplash.com/search/photos/?client_id={CLIENT_ID}&orientation=landscape&query={query}")

    if response.status_code == 200:
        photos = response.json()["results"]

        for photo in photos:
            response = requests.get(f"https://api.unsplash.com/photos/{photo['id']}?client_id={CLIENT_ID}")
            if response.status_code == 200:
                photo = response.json()
                id_ = photo['id']

                response = requests.get(photo["urls"]["raw"] + "&ar=16:9&fit=crop&w=3840", allow_redirects=True)

                if response.status_code == 200:
                    open(f"image-{id_}.jpg", "wb").write(response.content)
                    
                    with Image.open(f"image-{id_}.jpg") as im:
                        draw = ImageDraw.Draw(im)

                        location_text = photo["location"]["name"] if photo["location"]["name"] else ""
                        font = ImageFont.truetype("fonts/FiraSans-Regular.ttf", 100)

                        draw.text((20, 10), location_text, font = font, align ="left")

                        for country, code in country_codes.items():
                            country = country.lower()
                            if country in location_text.lower():
                                flag_img = Image.open(f"flags/{code.lower()}.png").convert("RGBA")
                                im.paste(flag_img, (im.size[0]-flag_img.size[0]-20, 20), flag_img)


                        im.save(f"image-{id_}.jpg", "JPEG")
                        #im.save(f"/usr/share/wallpapers/custom-wallpapers/djean/image-{id_}.jpg", "JPEG")
