"""Using CDP.fetch.RequestPaused to filter content in real-time."""
import asyncio
import colorama
import mycdp
import sys
from seleniumbase import decorators
from seleniumbase import cdp_driver

c1 = colorama.Fore.RED + colorama.Back.LIGHTYELLOW_EX
c2 = colorama.Fore.BLUE + colorama.Back.LIGHTCYAN_EX
cr = colorama.Style.RESET_ALL
if "linux" in sys.platform:
    c1 = c2 = cr = ""


class RequestPausedTest():
    async def request_paused_handler(self, event, tab):
        r = event.request
        is_image = ".png" in r.url or ".jpg" in r.url or ".gif" in r.url
        if not is_image:  # Let the data through
            tab.feed_cdp(
                mycdp.fetch.continue_request(request_id=event.request_id)
            )
        else:  # Block the data (images)
            TIMED_OUT = mycdp.network.ErrorReason.TIMED_OUT
            s = f"{c1}BLOCKING{cr} | {c2}{r.method}{cr} | {r.url}"
            print(f" >>> ------------\n{s}")
            tab.feed_cdp(
                mycdp.fetch.fail_request(event.request_id, TIMED_OUT)
            )

    async def start_test(self):
        driver = await cdp_driver.start_async()
        tab = await driver.get("about:blank")
        tab.add_handler(mycdp.fetch.RequestPaused, self.request_paused_handler)
        url = "https://gettyimages.com/photos/firefly-2003-nathan"
        await driver.get(url)
        await asyncio.sleep(5)
        driver.stop()


@decorators.print_runtime("RequestPausedTest")
def main():
    test = RequestPausedTest()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(test.start_test())


if __name__ == "__main__":
    main()
