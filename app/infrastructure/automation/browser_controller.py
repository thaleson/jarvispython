import webbrowser


class BrowserController:

    @staticmethod
    def open_youtube():

        webbrowser.open("https://www.youtube.com")

    @staticmethod
    def open_url(url: str):

        webbrowser.open(url)
