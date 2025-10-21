from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from flans.models import Flan


class Command(BaseCommand):
    help = 'Add 20+ sample flans to the database'

    def handle(self, *args, **options):
        # Get or create a user to be the creator
        user, created = User.objects.get_or_create(
            username='flancreator',
            defaults={
                'email': 'creator@onlyflans.com',
                'first_name': 'Flan',
                'last_name': 'Master'
            }
        )

        sample_flans = [
            {
                'name': 'Classic Vanilla Dream',
                'description': 'Creamy traditional Mexican flan with golden caramel sauce that melts in your mouth. The perfect balance of sweet and rich.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'vanilla',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Chocolate Caramel Heaven',
                'description': 'Rich dark chocolate flan with salted caramel drizzle. So decadent it should be illegal.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600',
                'flan_type': 'chocolate',
                'is_premium': True,
                'price': 4.99
            },
            {
                'name': 'Coconut Paradise',
                'description': 'Tropical coconut flan with toasted coconut flakes. Close your eyes and taste the beach.',
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600',
                'flan_type': 'coconut',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Coffee Delight',
                'description': 'Espresso-infused flan with coffee glaze. The perfect dessert for coffee lovers.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'coffee',
                'is_premium': True,
                'price': 3.99
            },
            {
                'name': 'Abuelas Secret Recipe',
                'description': 'This recipe has been passed down for generations. So good it might make you cry.',
                'image_url': 'https://images.unsplash.com/photo-1541783245837-1a93e9788abb?w=600',
                'flan_type': 'vanilla',
                'is_premium': True,
                'price': 6.99
            },
            {
                'name': 'Salted Caramel Swirl',
                'description': 'Vanilla flan with beautiful salted caramel swirls. Sweet, salty, and absolutely perfect.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'vanilla',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Mexican Chocolate Flan',
                'description': 'Traditional Mexican chocolate with cinnamon and spice. A flavor explosion in every bite.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600',
                'flan_type': 'chocolate',
                'is_premium': True,
                'price': 5.49
            },
            {
                'name': 'Tropical Coconut Lime',
                'description': 'Coconut flan with zesty lime twist. Refreshing and light with tropical vibes.',
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600',
                'flan_type': 'coconut',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Mocha Madness',
                'description': 'The perfect marriage of coffee and chocolate. For when you cant decide between both.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'coffee',
                'is_premium': True,
                'price': 4.99
            },
            {
                'name': 'Bourbon Vanilla Elegance',
                'description': 'Premium bourbon vanilla beans in a silky smooth flan. Pure luxury.',
                'image_url': 'https://images.unsplash.com/photo-1541783245837-1a93e9788abb?w=600',
                'flan_type': 'vanilla',
                'is_premium': True,
                'price': 7.99
            },
            {
                'name': 'White Chocolate Raspberry',
                'description': 'Creamy white chocolate flan with raspberry coulis. Elegant and delicious.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600',
                'flan_type': 'chocolate',
                'is_premium': True,
                'price': 5.99
            },
            {
                'name': 'Pina Colada Flan',
                'description': 'Coconut and pineapple flan that tastes like vacation in a dessert.',
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600',
                'flan_type': 'coconut',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Irish Coffee Flan',
                'description': 'Coffee flan with a hint of Irish cream. Adults only, for obvious reasons.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'coffee',
                'is_premium': True,
                'price': 6.49
            },
            {
                'name': 'Orange Blossom Flan',
                'description': 'Delicate orange blossom water infused flan. Light, floral, and unforgettable.',
                'image_url': 'https://images.unsplash.com/photo-1541783245837-1a93e9788abb?w=600',
                'flan_type': 'special',
                'is_premium': True,
                'price': 5.99
            },
            {
                'name': 'Dulce de Leche Supreme',
                'description': 'Flan swimming in homemade dulce de leche. Not for the faint of heart.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'special',
                'is_premium': True,
                'price': 6.99
            },
            {
                'name': 'Matcha Green Tea Flan',
                'description': 'Japanese matcha green tea gives this flan a unique and sophisticated flavor.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600',
                'flan_type': 'special',
                'is_premium': True,
                'price': 5.49
            },
            {
                'name': 'Lemon Basil Infusion',
                'description': 'Unexpected but amazing combination of lemon and fresh basil. Refreshing and unique.',
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600',
                'flan_type': 'special',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Spiced Pumpkin Flan',
                'description': 'All the cozy flavors of pumpkin spice in flan form. Perfect for autumn.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'special',
                'is_premium': True,
                'price': 4.99
            },
            {
                'name': 'Black Sesame Flan',
                'description': 'Nutty black sesame gives this flan an exotic and beautiful gray color.',
                'image_url': 'https://images.unsplash.com/photo-1541783245837-1a93e9788abb?w=600',
                'flan_type': 'special',
                'is_premium': True,
                'price': 5.99
            },
            {
                'name': 'Rum Raisin Flan',
                'description': 'Plump rum-soaked raisins throughout a rich vanilla flan. Sophisticated and boozy.',
                'image_url': 'https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=600',
                'flan_type': 'vanilla',
                'is_premium': True,
                'price': 6.49
            },
            {
                'name': 'Honey Lavender Dream',
                'description': 'Local honey and culinary lavender create a floral, delicate dessert experience.',
                'image_url': 'https://images.unsplash.com/photo-1488477181946-6428a0291777?w=600',
                'flan_type': 'special',
                'is_premium': False,
                'price': 0.00
            },
            {
                'name': 'Tiramisu Flan',
                'description': 'The classic Italian dessert reimagined as flan. Coffee, mascarpone, and cocoa magic.',
                'image_url': 'https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=600',
                'flan_type': 'coffee',
                'is_premium': True,
                'price': 6.99
            },
            {
                'name': 'Mexican Wedding Flan',
                'description': 'Extra rich and creamy flan traditionally served at Mexican weddings. Celebration in every bite.',
                'image_url': 'https://images.unsplash.com/photo-1541783245837-1a93e9788abb?w=600',
                'flan_type': 'vanilla',
                'is_premium': True,
                'price': 7.49
            }
        ]

        flans_created = 0
        for flan_data in sample_flans:
            flan, created = Flan.objects.get_or_create(
                name=flan_data['name'],
                defaults={
                    'description': flan_data['description'],
                    'image_url': flan_data['image_url'],
                    'flan_type': flan_data['flan_type'],
                    'is_premium': flan_data['is_premium'],
                    'price': flan_data['price'],
                    'creator': user
                }
            )
            if created:
                flans_created += 1
                self.stdout.write(f"✅ Added: {flan_data['name']}")
            else:
                self.stdout.write(f"⚠️ Already exists: {flan_data['name']}")

        self.stdout.write(self.style.SUCCESS(
            f'\n🎉 Successfully created {flans_created} new flans!'))
        self.stdout.write(f'📊 Total flans in database: {Flan.objects.count()}')
