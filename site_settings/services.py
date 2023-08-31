import json
from typing import Sequence, Mapping, Union, Optional

from django.db.models import QuerySet

from .models import CarouselImage
from .serializers import CarouselImageSerializer


def get_carousel_images(serialize: Optional[bool] = True) -> Union[QuerySet[CarouselImage], CarouselImageSerializer]:
    carousel_images = CarouselImage.objects.all().order_by("id")
    if serialize:
        return CarouselImageSerializer(carousel_images, many=True)
    return carousel_images


def save_carousel_images(form_data: Mapping, files: Mapping) -> None:
    images = []

    for image in json.loads(form_data["images"]):
        img = files.get("image: " + image["image"], False)

        if not img:
            img = image['image'].replace("/media/", "")

        image.pop("image")
        images.append(CarouselImage(**image, image=img))

    CarouselImage.objects.all().delete()
    CarouselImage.objects.bulk_create(images)


def get_languages():
    try:
        with open("../site_settings/languages.json") as languages_json:
                return json.load(languages_json)
    except:
        return {}


def save_languages(languages: Sequence) -> None:
    with open("../site_settings/languages.json", "w") as languages_json:
        languages_json.write(json.dumps(languages))


def get_tg_ids():
    tg_ids = []

    with open("../site_settings/tg_ids.txt") as tg_ids_file:
        for tg_id in tg_ids_file:
            tg_ids.append(tg_id.strip())

    return tg_ids


def save_tg_ids(tg_ids_txt):
    with open("../site_settings/tg_ids.txt", "w") as tg_ids_file:
        tg_ids_file.write(tg_ids_txt)
