from django.test import TestCase
from django.urls import reverse # converts name of url into the actual path
from django.db import IntegrityError
from django.core.exceptions import ValidationError
from .models import Video


class TestHomePageMessage(TestCase):

    def test_app_title_message_on_home_page(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertContains(response, 'Football Videos')

class TestAddVideo(TestCase):
    
    def test_add_video(self):

        valid_video = {
            'name': 'Vikings lose to Broncos Recap',
            'url': 'https://www.youtube.com/watch?v=DCIlwPIISS8',
            'notes': 'Vikings lose, Recap'
        }

        url = reverse('add_video')
        response = self.client.post(url, valid_video, follow=True)

        self.assertTemplateUsed('video_collection/video_list.html')

        # does the video list show the new video?
        self.assertContains(response, 'Vikings lose to Broncos Recap')
        self.assertContains(response, 'Vikings lose, Recap')
        self.assertContains(response, 'https://www.youtube.com/watch?v=DCIlwPIISS8')

        video_count = Video.objects.count()
        self.assertEquals(1, video_count)

        video = Video.objects.first()
        self.assertEquals('Vikings lose to Broncos Recap', video.name)
        self.assertEquals('https://www.youtube.com/watch?v=DCIlwPIISS8', video.url)
        self.assertEquals('Vikings lose, Recap', video.notes)
        self.assertEquals('DCIlwPIISS8', video.video_id)
        
    def test_add_video_invalid_url_not_added(self):

        invalid_video_urls = [
            'https://www.youtube.com/watch',
            'https://www.youtube.com/watch?',
            'https://www.youtube.com/watch?v=123',
            'https://www.youtube.com/watch?v=',
            'https://www.github.com',
            'https://www.minneapolis.edu',
            'https://www.minneapolis.edu?v=32156das'
        ]

        for invalid_video_url in invalid_video_urls:

            new_video = {
                'name': 'example',
                'url': invalid_video_url,
                'notes': 'example notes',
            }

        url = reverse('add_video')
        response = self.client.post(url, new_video)

        self.assertTemplateUsed('video_collection/add.html')

        messages = response.context['messages']
        message_texts = [ message.message for message in messages]
        
        self.assertIn('Invalid YouTube URL', message_texts)
        self.assertIn('Please check the data entered.', message_texts)

        video_count = Video.objects.count()
        self.assertEquals(0, video_count)


class TestVideoList(TestCase):
    
    def test_all_video_displayed_in_correct_order(self):
        v1 = Video.objects.create(name='aaa', notes='hello one', url='https://www.youtube.com/watch?v=111')
        v2 = Video.objects.create(name='PPP', notes='hello two', url='https://www.youtube.com/watch?v=222')
        v3 = Video.objects.create(name='ccc', notes='hello three', url='https://www.youtube.com/watch?v=333')
        v4 = Video.objects.create(name='JJJ', notes='hello four', url='https://www.youtube.com/watch?v=444')

        expected_video_order = [v1, v3, v4, v2]
        url = reverse('video_list')
        response = self.client.post(url)

        videos_in_template = list(response.context['videos'])
        self.assertEquals(videos_in_template, expected_video_order)

    def test_no_video_message(self):
        url = reverse('video_list')
        response = self.client.post(url)
        self.assertContains(response, 'No videos')
        self.assertEqual(0, len(response.context['videos']))

    def test_video_number_message_one_video(self):
        v1 = Video.objects.create(name='aaa', notes='hello one', url='https://www.youtube.com/watch?v=111')
        url = reverse('video_list')
        response = self.client.post(url)

        self.assertContains(response, '1 Video')
        self.assertNotContains(response, '1 Videos')

    def test_video_number_message_two_video(self):
        v1 = Video.objects.create(name='aaa', notes='hello one', url='https://www.youtube.com/watch?v=111')
        v2 = Video.objects.create(name='bbb', notes='hello one more', url='https://www.youtube.com/watch?v=1111')
        
        url = reverse('video_list')
        response = self.client.post(url)

        self.assertContains(response, '2 Videos')


class TestVideoSearch(TestCase):
    pass


class TestVidelModel(TestCase):
    
    def test_invalid_url_raises_validation_error(self):
        invalid_video_urls = [
                'https://www.youtube.com/watch',
                'https://www.youtube.com/watch?',
                'https://www.youtube.com/where?v=123',
                'https://www.youtube.com/watch?v=',
                'https://www.github.com',
                'https://www.minneapolis.edu',
                'https://www.minneapolis.edu?v=32156das'
        ]
        
        for invalid_video_url in invalid_video_urls:
            with self.assertRaises(ValidationError):
                Video.objects.create(name='abc', url=invalid_video_url, notes='google website')
                
        self.assertEqual(0, Video.objects.count())


    def test_duplicate_video_raises_integrity_error(self):
        v1 = Video.objects.create(name='aaa', notes='hello one', url='https://www.youtube.com/watch?v=111')
        with self.assertRaises(IntegrityError):
            Video.objects.create(name='aaa', notes='hello one', url='https://www.youtube.com/watch?v=111')



