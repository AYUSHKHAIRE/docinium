import time
import logging
import undetected_chromedriver as uc

logger = logging.getLogger(__name__)


class SeleniumLauncher:
    """
    Launch undetected Chrome Selenium driver and resize window accurately.
    """

    def __init__(self, screen_width: int = 1920, screen_height: int = 1080, headless: bool = True):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.headless = headless
        self.driver = None

    def setup_selenium_driver(self):
        """
        Setup undetected Chrome Selenium driver,
        resize the window accurately.

        Output:
            None (sets self.driver)
        """
        start_time = time.time()

        # ------------------------------------------------------------
        # Chrome Options
        # ------------------------------------------------------------
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-infobars")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--start-maximized")

        # if self.headless:
        #     chrome_options.add_argument("--headless=new")

        chrome_options.set_capability(
            "goog:loggingPrefs", {"browser": "ALL"}
        )

        # ------------------------------------------------------------
        # Launch Driver
        # ------------------------------------------------------------
        driver = uc.Chrome(
            options=chrome_options,
            use_subprocess=True
        )

        # ------------------------------------------------------------
        # Accurate Window Resize (outer vs inner)
        # ------------------------------------------------------------
        outer_width = driver.execute_script("return window.outerWidth;")
        inner_width = driver.execute_script("return window.innerWidth;")
        outer_height = driver.execute_script("return window.outerHeight;")
        inner_height = driver.execute_script("return window.innerHeight;")

        width_diff = outer_width - inner_width
        height_diff = outer_height - inner_height

        final_width = self.screen_width + width_diff
        final_height = self.screen_height + height_diff

        driver.set_window_size(final_width, final_height)

        # ------------------------------------------------------------
        # Finalize
        # ------------------------------------------------------------
        self.driver = driver

        end_time = time.time()
        logger.info(
            f"[ SETUP ] Undetected Chrome initialized in "
            f"{end_time - start_time:.4f} seconds | "
            f"Viewport: {self.screen_width}x{self.screen_height}"
        )

launcher = SeleniumLauncher(
    screen_width=1920,
    screen_height=1080,
    headless=True
)

launcher.setup_selenium_driver()
driver = launcher.driver

driver.get("https://www.google.com")
time.sleep(5000)