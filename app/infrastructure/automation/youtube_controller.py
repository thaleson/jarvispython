import threading

from playwright.sync_api import sync_playwright

from app.core.logger import logger


class YoutubeController:
    @staticmethod
    def _play_video(
        query: str,
    ) -> None:
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(
                headless=False,
                args=[
                    "--autoplay-policy=no-user-gesture-required",
                ],
            )

            page = browser.new_page()

            page.goto(
                "https://www.youtube.com",
                wait_until="domcontentloaded",
            )

            page.fill(
                "input[name='search_query']",
                query,
            )

            page.keyboard.press("Enter")

            page.wait_for_selector(
                "ytd-video-renderer a#thumbnail",
                timeout=20000,
            )

            first_video = page.locator("ytd-video-renderer a#thumbnail").first

            first_video.click()

            page.wait_for_selector(
                "#movie_player video",
                timeout=20000,
            )

            page.wait_for_timeout(2000)

            main_video = page.locator("#movie_player video").first

            main_video.evaluate("video => video.play()")

            logger.info("YouTube video started. Keeping browser open.")

            page.wait_for_timeout(
                300000,
            )

            browser.close()

    @classmethod
    def search_and_play(
        cls,
        query: str,
    ) -> None:
        logger.info(f"Searching and playing on YouTube: {query}")

        thread = threading.Thread(
            target=cls._play_video,
            args=(query,),
            daemon=False,
        )

        thread.start()
