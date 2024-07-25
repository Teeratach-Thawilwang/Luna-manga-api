import copy
from io import BytesIO

from django.conf import settings
from PIL import Image, ImageSequence


class ConversionService:
    def openFromUploadFile(self, uploadFile):
        uploadFileCopy = BytesIO(uploadFile.read())
        uploadFile.seek(0)
        image = Image.open(uploadFileCopy)
        return image

    def convertImageFromUploadFile(self, uploadFile, collection):
        extension = "." + uploadFile.name.split(".")[-1]
        originalFileName = uploadFile.name.replace(extension, "")
        temPath = settings.TEMPORARY_DIR
        filesName = []

        image = self.openFromUploadFile(uploadFile)

        for conversion, size in collection["conversion"].items():
            size = self.getSizeConversion(image, size)
            resizedImage, frames = self.resizeImage(image, size)

            fileName = f"{originalFileName}_{conversion}{extension}"
            filesName.append(fileName)
            self.saveImage(resizedImage, temPath + fileName, quality=100, frames=frames)

        fileName = uploadFile.name
        filesName.append(fileName)
        self.saveImage(image, temPath + fileName, quality=100)

        return filesName

    def transfromConversionByCollection(self, image, collection):
        newCllection = copy.deepcopy(collection)
        for conversion, size in newCllection["conversion"].items():
            size = self.getSizeConversion(image, size)
            newCllection["conversion"][conversion] = {
                "width": size[0],
                "height": size[1],
            }

        newCllection["conversion"]["original"] = {
            "width": image.size[0],
            "height": image.size[1],
        }
        return newCllection["conversion"]

    def getSizeConversion(self, image, size):
        height = size["height"]
        if height == "auto":
            height = int((image.size[1] / image.size[0]) * size["width"])

        width = size["width"]
        if width == "auto":
            width = int((image.size[0] / image.size[1]) * size["height"])

        return (width, height)

    def saveImage(self, image: Image.Image, fileName: str, quality: int = 100, frames: list[Image.Image] = None):
        isAnimated = getattr(image, "is_animated", False)
        if image.format == "GIF" and isAnimated:
            if frames:
                params = {
                    "fp": fileName,
                    "save_all": True,
                    "append_images": frames[1:],
                    "disposal": getattr(image, "disposal_method", 2),
                    **image.info,
                }
                frames[0].save(**params)
            else:
                params = {
                    "fp": fileName,
                    "save_all": True,
                    "append_images": [frame.copy() for frame in ImageSequence.Iterator(image)][1:],
                    "disposal": getattr(image, "disposal_method", 2),
                    **image.info,
                }
                image.save(**params)
        else:
            image.save(fileName, quality=quality)

    def resizeImage(self, image: Image.Image, size: tuple[int]):
        isAnimated = getattr(image, "is_animated", False)
        if image.format == "GIF" and isAnimated:
            frames = [frame.copy().resize(size, Image.LANCZOS) for frame in ImageSequence.Iterator(image)]
            newImage = frames[0]
            newImage.info = image.info
            newImage.format = "GIF"
            newImage.is_animated = True
            return newImage, frames
        else:
            resizedImage = image.resize(size, Image.LANCZOS)
            return resizedImage, None
