from django.test import TestCase

from django.urls import reverse

from .models import Feed

import json

class RssIndexViewTests(TestCase):
    def test_no_feed(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["feed"], None)

    def test_user_feed(self):
        response = self.client.get(reverse("index") + "?url=https://www.djangoproject.com/rss/weblog/")

        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["feed"], None)

class RssFeedModelTests(TestCase):
    def setUp(self):
        Feed.objects.create(url="http://feeds.news24.com/articles/news24/TopStories/rss")
    def test_model_has_url(self):
        news24_feed = Feed.objects.get(url="http://feeds.news24.com/articles/news24/TopStories/rss")
        self.assertEqual(news24_feed.url,"http://feeds.news24.com/articles/news24/TopStories/rss")

class RssRestFeedsViewTests(TestCase):
    def test_create_feed(self):
        url = "http://feeds.news24.com/articles/news24/TopStories/rss"
        json_data = json.dump({"url": url})

        response = self.client.post(
            reverse('rss-feeds'),
            json_data,
            content_type="application/json"
        )

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 201)
        self.assertQuerysetEqual(feeds,["<Feed '{}'>".format(url)])


    def test_get_feeds(self):
        url = "http://feeds.news24.com/articles/news24/TopStories/rss"

        Feed.objects.create(
            url=url
        )

        response = self.client.get(reverse('rest-feeds'))
        feed = response.json()[0]

        self.assertEqual(response.status_code, 200)
        self.assertEqual(feed["url"], url)

    def test_update_feed(self):
        url = "http://feeds.news24.com/articles/news24/TopStories/rss"
        new_url = "http://feeds.news24.com/articles/news24/Africa/rss"

        Feed.objects.create(
            url=url
        )

        json_data = json.dumps({
            "url": new_url
        })

        response = self.client.put(
            "/rss/feeds/1/",
            json_data,
            content_type="application/json"
        )

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            feeds,
            ["<Feed '{}'>".format(new_url)]
        )

    def test_delete_feed(self):
        Feed.objects.create(
            url="http://feeds.news24.com/articles/news24/TopStories/rss"
        )

        response = self.client.delete("/rss/feeds/1/")

        feeds = Feed.objects.all()

        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(
            feeds,
            []
        )
