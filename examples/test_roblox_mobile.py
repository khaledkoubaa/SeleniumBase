"""Mobile device test for Chromium-based browsers
Example: "pytest test_roblox_mobile.py --mobile"
"""
from seleniumbase import BaseCase

if __name__ == "__main__":
    from pytest import main
    main([__file__, "--mobile", "-s"])


class RobloxTests(BaseCase):
    def test_roblox_mobile_site(self):
        if not self.mobile_emulator:
            self.open_if_not_url("about:blank")
            print("\n  This test is only for mobile-device web browsers!")
            print('  (Use "--mobile" to run this test in Mobile Mode!)')
            self.skip('Use "--mobile" to run this test in Mobile Mode!')
        self.open("https://www.roblox.com/")
        self.assert_element("#download-the-app-container")
        self.assert_text("Roblox for Android", "p.roblox-for-platform")
        self.assert_text("Continue in App", "a.primary-link")
        self.highlight("p.roblox-for-platform", loops=8)
        self.highlight("a.primary-link", loops=8)
