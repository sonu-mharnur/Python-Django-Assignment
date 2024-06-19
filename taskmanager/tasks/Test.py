# tasks/tests.py

from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import Task

class TaskAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.task1 = Task.objects.create(title='Task 1', description='Description for Task 1')
        self.task2 = Task.objects.create(title='Task 2', description='Description for Task 2')

    def test_list_tasks(self):
        response = self.client.get(reverse('task-list-create'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'Description for New Task'}
        response = self.client.post(reverse('task-list-create'), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)

    def test_retrieve_task(self):
        response = self.client.get(reverse('task-retrieve-update-destroy', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'Task 1')

    def test_update_task(self):
        data = {'title': 'Updated Task'}
        response = self.client.put(reverse('task-retrieve-update-destroy', kwargs={'pk': self.task1.id}), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertEqual(self.task1.title, 'Updated Task')

    def test_delete_task(self):
        response = self.client.delete(reverse('task-retrieve-update-destroy', kwargs={'pk': self.task1.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)

