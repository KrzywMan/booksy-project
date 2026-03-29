import json
from datetime import datetime
from django.core.management.base import BaseCommand
from booksy.models import Hardware  # Upewnij się, że nazwa aplikacji jest poprawna

class Command(BaseCommand):
    help = 'Imports and cleans hardware data from JSON'

    def handle(self, *args, **options):
        raw_data = [
            { "id": 1, "name": "Apple iPhone 13 Pro Max", "brand": "Apple", "purchaseDate": "2021-11-23", "status": "Available" },
            { "id": 2, "name": "Apple MacBook Pro 13", "brand": "Apple", "purchaseDate": "2021-12-20", "status": "In Use" },
            { "id": 3, "name": "Razer Basilisk V2", "brand": "Razer", "purchaseDate": "2021-06-05", "status": "Repair" },
            { "id": 4, "name": "SAMSUNG Galaxy S21", "brand": "Samsung", "purchaseDate": "2021-11-23", "status": "Available" },
            { "id": 5, "name": "Dell XPS 15 9510", "brand": "Dell", "purchaseDate": "2022-03-15", "status": "Available", "notes": "Battery swelling, do not issue without service." },
            { "id": 6, "name": "Logitech MX Master 3", "brand": "Logitech", "purchaseDate": "2027-10-10", "status": "Available" },
            { "id": 7, "name": "Sony WH-1000XM4", "brand": "Sony", "purchaseDate": "2022-01-12", "status": "In Use", "assignedTo": "j.doe@booksy.com" },
            { "id": 4, "name": "Duplicate ID Test Laptop", "brand": "Lenovo", "purchaseDate": "2023-01-01", "status": "Repair" },
            { "id": 9, "name": "iPad Pro 12.9", "brand": "Appel", "purchaseDate": "22-05-2023", "status": "Available" },
            { "id": 10, "name": "Unknown Device", "brand": "", "purchaseDate": None, "status": "Unknown" },
            { "id": 11, "name": "MacBook Air M2", "brand": "Apple", "purchaseDate": "2023-08-01", "status": "Available", "history": "Returned by user with liquid damage. Keyboard sticky." }
        ]

        self.stdout.write(self.style.SUCCESS('Rozpoczynam import danych...'))

        for item in raw_data:
            # Invalid names changing
            brand = item.get('brand', '').strip()
            if brand.lower() == 'appel':
                brand = 'Apple'
            
            # Date format usage
            p_date = item.get('purchaseDate')
            clean_date = None
            
            if p_date:
                for fmt in ('%Y-%m-%d', '%d-%m-%Y'):
                    try:
                        clean_date = datetime.strptime(p_date, fmt).date()
                        break
                    except ValueError:
                        continue
            
            # Status validation
            status = item.get('status', 'Available')
            if status not in ['Available', 'In Use', 'Repair']:
                status = 'Repair' # Bezpieczny fallback dla "Unknown"

            Hardware.objects.create(
                name=item.get('name'),
                brand=brand,
                purchase_date=clean_date,
                status=status,
                assigned_to=item.get('assignedTo'),
                notes=item.get('notes', ''),
                history=item.get('history', '')
            )

        self.stdout.write(self.style.SUCCESS(f'Pomyślnie zaimportowano {len(raw_data)} przedmiotów.'))