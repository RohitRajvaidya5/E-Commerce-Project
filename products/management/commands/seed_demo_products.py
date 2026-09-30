from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Product


DEMO_PRODUCTS = [
    {
        "name": "Classic White T-Shirt",
        "description": "A comfortable everyday cotton T-shirt in a clean white finish.",
        "price": 29.99,
        "stock": 40,
        "category": "Apparel",
        "color": "#f5f5f5",
    },
    {
        "name": "Urban Bluetooth Headphones",
        "description": "Wireless over-ear headphones with deep bass and all-day comfort.",
        "price": 89.99,
        "stock": 18,
        "category": "Electronics",
        "color": "#3b82f6",
    },
    {
        "name": "Leather Wallet",
        "description": "Premium leather wallet with multiple card slots and a slim profile.",
        "price": 49.5,
        "stock": 25,
        "category": "Accessories",
        "color": "#a16207",
    },
    {
        "name": "Running Sneakers",
        "description": "Lightweight performance sneakers built for comfort and movement.",
        "price": 119.0,
        "stock": 12,
        "category": "Footwear",
        "color": "#10b981",
    },
    {
        "name": "Smart Watch",
        "description": "Track fitness, notifications, and time with this everyday smartwatch.",
        "price": 149.99,
        "stock": 15,
        "category": "Electronics",
        "color": "#8b5cf6",
    },
    {
        "name": "Travel Backpack",
        "description": "Durable and spacious backpack designed for commuting and travel.",
        "price": 64.99,
        "stock": 30,
        "category": "Accessories",
        "color": "#f97316",
    },
]


def build_demo_svg(title, color):
    return f"""
    <svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
      <defs>
        <linearGradient id="bg" x1="0" x2="1">
          <stop offset="0%" stop-color="#ffffff" />
          <stop offset="100%" stop-color="{color}" />
        </linearGradient>
      </defs>
      <rect width="800" height="600" fill="url(#bg)" />
      <rect x="90" y="90" width="620" height="420" rx="28" fill="rgba(255,255,255,0.35)" stroke="rgba(0,0,0,0.2)" />
      <circle cx="240" cy="220" r="110" fill="rgba(255,255,255,0.6)" />
      <rect x="330" y="180" width="220" height="28" rx="14" fill="rgba(17,24,39,0.8)" />
      <rect x="330" y="230" width="180" height="20" rx="10" fill="rgba(17,24,39,0.7)" />
      <rect x="330" y="270" width="140" height="20" rx="10" fill="rgba(17,24,39,0.5)" />
      <text x="400" y="470" text-anchor="middle" font-size="42" font-family="Arial, sans-serif" fill="#111827" font-weight="700">{title}</text>
    </svg>
    """.strip()


class Command(BaseCommand):
    help = "Seed demo product data and local image assets for development"

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete all existing products before seeding demo data.",
        )

    def handle(self, *args, **options):
        if options["clear"]:
            deleted_count, _ = Product.objects.all().delete()
            self.stdout.write(self.style.WARNING(f"Deleted {deleted_count} existing products."))

        created_count = 0

        for product_data in DEMO_PRODUCTS:
            product, created = Product.objects.update_or_create(
                name=product_data["name"],
                defaults={
                    "description": product_data["description"],
                    "price": product_data["price"],
                    "stock": product_data["stock"],
                    "category": product_data["category"],
                },
            )

            if created:
                created_count += 1

            if not product.image:
                filename = f"{slugify(product.name)}.svg"
                svg_content = build_demo_svg(product.name, product_data["color"])
                product.image.save(filename, ContentFile(svg_content.encode("utf-8")), save=True)
                self.stdout.write(self.style.SUCCESS(f"Added image for: {product.name}"))

            self.stdout.write(
                self.style.SUCCESS(
                    f"{'Created' if created else 'Updated'}: {product.name}"
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Demo data complete. {created_count} new products were created."
            )
        )
