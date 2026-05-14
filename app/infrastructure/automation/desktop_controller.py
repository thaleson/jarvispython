import time

import pyautogui

from app.core.logger import logger


class DesktopController:
    @staticmethod
    def click(
        x: int,
        y: int,
    ) -> None:
        logger.info(f"Clicking at ({x}, {y})")

        pyautogui.moveTo(
            x,
            y,
            duration=1,
        )

        pyautogui.click()

    @staticmethod
    def click_first_youtube_result() -> None:
        DesktopController.wait(5)

        DesktopController.click(
            2096,
            726,
        )

    @staticmethod
    def wait(seconds: int) -> None:
        logger.info(f"Waiting {seconds} seconds")

        time.sleep(seconds)
