import unittest
import asyncio
from src.api import load_quotes, common_elements, fetch_quote, quote_tags, quote
from unittest.mock import patch, mock_open
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop
from aiohttp import web


class TestAPI(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open())
    @patch("src.api.json.load", return_value={})
    def test_load_quotes(self, json_mock, open_mock):
        load_quotes()
        open_mock.assert_called()

    def test_common_elements(self):
        l1 = [1, 2, 3]
        l2 = [3, 4, 5]
        l3 = [5, 6, 7]
        res = common_elements(l1, l2)
        self.assertEqual(res, {3})

        res = common_elements(l2, l3)
        self.assertEqual(res, {5})

        res = common_elements(l1, l3)
        self.assertEqual(res, set())
        
    @patch("src.api.load_quotes", return_value=[{"tags":['test']}])
    def test_fetch_quote(self, load_quote_mock):
        res1 = fetch_quote()
        res2 = fetch_quote(tags=["test"])
        self.assertEqual(res1, res2)


class TestApp(AioHTTPTestCase, unittest.TestCase):

    async def get_application(self):
        app = web.Application()
        app.router.add_get("", quote)
        app.router.add_get("/", quote)
        app.router.add_get("/tags", quote_tags)
        return app

    @unittest_run_loop
    @patch("src.api.fetch_quote", return_value={"status": "success",
                                                "tags": ["Ron"]})
    async def test_quote(self, fetch_quote_mock):
        resp = await self.client.request("GET", "/")
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertTrue("success" in text)

    @unittest_run_loop
    @patch("src.api.fetch_quote", return_value={"status": "success",
                                                "tags": ["Ron"]})
    async def test_quote_tags(self, fetch_quote_mock):
        resp = await self.client.request("GET", "/tags?tags=Ron")
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertTrue("success" in text)
        self.assertTrue("Ron" in text)

        resp = await self.client.request("GET", "/tags?tags=Veronica")
        self.assertEqual(resp.status, 200)
        text = await resp.text()
        self.assertTrue("success" in text)

if __name__ == "__main__":
    unittest.main()
