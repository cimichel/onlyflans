from django.core.management.base import BaseCommand
from flans.models import FlanCreator

class Command(BaseCommand):
    help = 'Add hilarious fake flan creators to the database'
    
    def handle(self, *args, **options):
        creators = [
            {
                'name': 'Gordon Ramsay',
                'creator_type': 'chef',
                'bio': '"THIS FLAN IS RAW!...ly amazing when you actually follow my recipe, you donkey!" Known for his temper and perfectly caramelized sugar. His vanilla flan is so good it will make you cry (mostly from happiness, sometimes from fear).',
                'profile_image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRHaVSaSDzehBonWYJXh-kdNv4GEfTzTPElJ404YLS20xVy5KKLYK3y0rWD0s2RmNBwynLYl3QU3WQ3pUpKQIUsTsq8SQ-Rdgfm2VD4tw',
                'is_featured': True,
                'total_flans': 12,
                'total_earnings': 8472.50,
                'satisfaction_rate': 98,
                'instagram_followers': '2.4M'
            },
            {
                'name': 'Abuela Maria',
                'creator_type': 'grandma', 
                'bio': '90 years young and still making the best flan in Guadalajara. Secret ingredient: love (and a pinch of brandy). Her recipes have been passed down through 4 generations. "Mijito, you need more caramel!"',
                'profile_image': 'https://static0.colliderimages.com/wordpress/wp-content/uploads/2022/02/Rita-Moreno-West-Side-Story.jpg?w=1200&h=675&fit=crop',
                'is_featured': True,
                'total_flans': 8,
                'total_earnings': 3245.80,
                'satisfaction_rate': 100,
                'instagram_followers': '450K'
            },
            {
                'name': 'Nana Rosa',
                'creator_type': 'grandma',
                'bio': 'Known as "The Flan Whisperer". Can tell if a flan is perfect just by listening to it jiggle. Her coconut flan has caused three marriage proposals. "A little more vanilla, cariño!"',
                'profile_image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7cJMe-Gwtr60fJPy1ZTtlj4ZkQkS2v_Aygg&s',
                'is_featured': True,
                'total_flans': 15,
                'total_earnings': 5123.45,
                'satisfaction_rate': 99,
                'instagram_followers': '380K'
            },
            {
                'name': 'Palmirinha',
                'creator_type': 'chef',
                'bio': 'The pudim queen in Brazil. "The only thing you should be afraid of in the kitchen is running out of eggs!"',
                'profile_image': 'https://encrypted-tbn2.gstatic.com/images?q=tbn:ANd9GcS8eJRIIUuEKNj-GrntChX5ij29opmjwAYk6wi9bIQh4yVSYWWYNkcEZbPpZ4Pf6uVFfk5UL9jHlOE382Eqe-J6ooelajjX1xhhPGDF6Yg',
                'is_featured': False,
                'total_flans': 6,
                'total_earnings': 1876.90,
                'satisfaction_rate': 87,
                'instagram_followers': '120K'
            },
            {
                'name': 'Ana Maria Braga',
                'creator_type': 'influencer',
                'bio': ' TV presenter with a mascot parrot. "It\'s a good thing... that you subscribed to my flans!"',
                'profile_image': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ5vEPMPnHSGx_J1gKl8KZOM_rDC9NjXj2-7kp3LgxZObscG_j2ZghP8fIf0AwKc_jxBwzmB2PPeK5aN0BYtq7N_ssJKmzSUWCcyG0FGg',
                'is_featured': False,
                'total_flans': 9,
                'total_earnings': 2987.30,
                'satisfaction_rate': 94,
                'instagram_followers': '890K'
            },
            {
                'name': 'Tía Carmen',
                'creator_type': 'grandma',
                'bio': 'The sassiest flan maker this side of the Rio Grande. Will roast your flan skills while teaching you how to make perfection. "Ay, mi amor, your caramel is too pale! Are you afraid of color?"',
                'profile_image': 'https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=400&auto=format&fit=crop&q=80',
                'is_featured': True,
                'total_flans': 11,
                'total_earnings': 4321.65,
                'satisfaction_rate': 97,
                'instagram_followers': '560K'
            },
            {
                'name': 'Chef Eric Jacquin',
                'creator_type': 'chef',
                'bio': 'Italian chef who believes everything is better with flan. Known for his "flan alfredo" and "tiramisu flan". "Mama mia! That\'s a spicy flan!"',
                'profile_image': 'https://encrypted-tbn3.gstatic.com/images?q=tbn:ANd9GcRCWbJ4HzAtNq650CpHcfLtG0oNdiLccLkgeJAEUGIAIibiRVI9PSdFttZu21umWAoAH3TzPJAybcd7voH0GpWKyaFQEA0MnbYp1wuinW0',
                'is_featured': False,
                'total_flans': 7,
                'total_earnings': 2154.75,
                'satisfaction_rate': 91,
                'instagram_followers': '230K'
            },
            {
                'name': 'Abuelita Consuelo',
                'creator_type': 'grandma',
                'bio': 'Makes flan so good it should be illegal. Known for sneaking a little tequila into her recipes. "A little kick never hurt anybody, mija!"',
                'profile_image': 'https://img.texasmonthly.com/2020/11/texas-firsts-baking-conchas-grandmother.jpg?auto=compress&crop=faces&fit=fit&fm=pjpg&ixlib=php-3.3.1&q=45',
                'is_featured': False,
                'total_flans': 14,
                'total_earnings': 3876.20,
                'satisfaction_rate': 96,
                'instagram_followers': '670K'
            }
        ]
        
        creators_created = 0
        for creator_data in creators:
            creator, created = FlanCreator.objects.get_or_create(
                name=creator_data['name'],
                defaults=creator_data
            )
            if created:
                creators_created += 1
                self.stdout.write(f"✅ Added: {creator_data['name']}")
            else:
                self.stdout.write(f"⚠️ Already exists: {creator_data['name']}")
        
        self.stdout.write(self.style.SUCCESS(f'\n🎉 Successfully created {creators_created} hilarious creators!'))
        total_creators = FlanCreator.objects.count()
        self.stdout.write(f'📊 Total creators in database: {total_creators}')