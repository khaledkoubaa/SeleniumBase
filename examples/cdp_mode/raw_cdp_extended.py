"""The long way of using CDP Mode without WebDriver"""
import asyncio
from seleniumbase import sb_cdp
from seleniumbase import cdp_driver

url = "https://seleniumbase.io/demo_page"
loop = asyncio.new_event_loop()
driver = cdp_driver.start_sync()
page = loop.run_until_complete(driver.get(url))
sb = sb_cdp.CDPMethods(loop, page, driver)

sb.press_keys("input", "Text")
sb.highlight("button")
sb.type("textarea", "Here are some words")
sb.click("button")
sb.set_value("input#mySlider", "100")
sb.click_visible_elements("input.checkBoxClassB")
sb.select_option_by_text("#mySelect", "Set to 75%")
sb.gui_hover_and_click("#myDropdown", "#dropOption2")
sb.gui_click_element("#checkBox1")
sb.gui_drag_and_drop("img#logo", "div#drop2")
sb.nested_click("iframe#myFrame3", ".fBox")
sb.sleep(2)
sb.driver.stop()
