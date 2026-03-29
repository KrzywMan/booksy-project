from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Hardware
from django.urls import reverse

class HardwareRentalTests(TestCase):
    def setUp(self):
        # preparing data
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.admin = User.objects.create_user(username='admin', password='password123', is_staff=True)
        
        # 1. Working device
        self.laptop = Hardware.objects.create(
            name="Test Laptop", brand="Dell", status="Available"
        )
        # 2. Device in repair
        self.broken_phone = Hardware.objects.create(
            name="Broken Phone", brand="Apple", status="Repair"
        )
        # 3. Device already rent
        self.busy_tablet = Hardware.objects.create(
            name="Busy Tablet", brand="Samsung", status="In Use"
        )

    # TEST 1: Cant rent broken device
    def test_cannot_rent_repair_hardware(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(f'/api/rent/{self.broken_phone.id}/')
        
        self.assertEqual(response.status_code, 400)
        self.broken_phone.refresh_from_db()
        self.assertEqual(self.broken_phone.status, "Repair")

    # TEST 2: Cant rent device in use
    def test_cannot_rent_already_in_use(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(f'/api/rent/{self.busy_tablet.id}/')
        
        self.assertEqual(response.status_code, 400)
        self.busy_tablet.refresh_from_db()
        self.assertEqual(self.busy_tablet.status, "In Use")

    # TEST 3: Normal user cant reach admin
    def test_unauthorized_access_to_admin_panel(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get('/admin-panel/')
        
        # Django user_passes_test enters login if no permission
        self.assertEqual(response.status_code, 302)