class ImageMimeTypeEnum:
    JPEG = "image/jpeg"
    PNG = "image/png"
    GIF = "image/gif"
    SVG = "image/svg+xml"
    ICO = "image/x-icon"
    WEBP = "image/webp"

    def get(self, mimetype):
        mimetype = mimetype.upper()
        mimetypes = self.all()
        if mimetype not in mimetypes:
            return None

        return mimetypes[mimetype]

    def all(self):
        return {
            "JPEG": self.JPEG,
            "PNG": self.PNG,
            "GIF": self.GIF,
            "SVG": self.SVG,
            "ICO": self.ICO,
            "WEBP": self.WEBP,
        }

    @staticmethod
    def list(by="value"):
        if by == "key":
            return list(ImageMimeTypeEnum().all().keys())
        return list(ImageMimeTypeEnum().all().values())
