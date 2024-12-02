import argostranslate.package
import argostranslate.translate

import goslate
from googletrans import Translator

class QueryTranslator:
    def __init__(self, from_code, to_code):
        self.from_code = from_code
        self.to_code = to_code

        argostranslate.package.update_package_index()

        for package in argostranslate.package.get_available_packages():
            if package.from_code == from_code and package.to_code == to_code:
                argostranslate.package.install_from_path(package.download())
                package.download()

        # self.translator = Translator()

    def translate(self, s):
        return argostranslate.translate.translate(s, self.from_code, self.to_code)
        # return self.translator.translate(s, src="en", dest="ru").text
        # return self.translator.translate(s, target_language)

if __name__ == "__main__":
    qt = QueryTranslator("en", "ru")
    print(qt.translate("Hello, World!"))
