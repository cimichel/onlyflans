"""
Management command to seed OnlyFlans with glorious flan data.

Usage:
    python manage.py seed_flans
    python manage.py seed_flans --clear   # limpa tudo antes de seeder
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from decimal import Decimal
from flans.models import Flan, FlanCreator, Subscriber


CREATORS = [
    {
        "name": "Gordon Hamsey",
        "creator_type": "chef",
        "bio": "I've destroyed 47 Michelin-starred kitchens in pursuit of the perfect flan. My caramel has made grown men weep. DONKEY! WHERE IS YOUR BAIN-MARIE?",
        "is_featured": True,
        "total_earnings": Decimal("84320.50"),
        "satisfaction_rate": 99,
        "instagram_followers": "2.3M",
        "profile_image": "https://i.pravatar.cc/300?img=11",
    },
    {
        "name": "Vovó Aparecida",
        "creator_type": "grandma",
        "bio": "Faço pudim desde 1974 e não preciso de receita, minha filha. Minha mão tem memória. Já ensinei 3 gerações e vou ensinar você também, mas você TEM que usar leite condensado Moça.",
        "is_featured": True,
        "total_earnings": Decimal("12450.00"),
        "satisfaction_rate": 100,
        "instagram_followers": "847K",
        "profile_image": "https://i.pravatar.cc/300?img=47",
    },
    {
        "name": "FlanQueen69",
        "creator_type": "influencer",
        "bio": "Flan content creator 🍮✨ Collab? DM me. Not your average dessert girlie. My vanilla flan has 4.2M views on TikTok and I don't even know why.",
        "is_featured": True,
        "total_earnings": Decimal("231000.00"),
        "satisfaction_rate": 94,
        "instagram_followers": "4.2M",
        "profile_image": "https://i.pravatar.cc/300?img=25",
    },
    {
        "name": "Chad Flansworth",
        "creator_type": "amateur",
        "bio": "Started making flan during COVID lockdown. My first attempt gave my whole family food poisoning. Things have improved significantly since then. Probably.",
        "is_featured": False,
        "total_earnings": Decimal("342.00"),
        "satisfaction_rate": 71,
        "instagram_followers": "847",
        "profile_image": "https://i.pravatar.cc/300?img=15",
    },
    {
        "name": "Chef Pierre Flançois",
        "creator_type": "chef",
        "bio": "Trained at Le Cordon Bleu Paris. Spent 8 years perfecting the French flan. Now I live in Brisbane and make flan for Australians who put tomato sauce on everything. C'est la vie.",
        "is_featured": False,
        "total_earnings": Decimal("28750.00"),
        "satisfaction_rate": 96,
        "instagram_followers": "156K",
        "profile_image": "https://i.pravatar.cc/300?img=68",
    },
    {
        "name": "Vovó Benedita",
        "creator_type": "grandma",
        "bio": "80 anos, 80 pudins. Já fiz pudim no fogão a lenha, no microondas, na airfryer e uma vez no porta-malas do carro a caminho de Aparecida. Todos ficaram perfeitos.",
        "is_featured": False,
        "total_earnings": Decimal("5200.00"),
        "satisfaction_rate": 100,
        "instagram_followers": "23K",
        "profile_image": "https://i.pravatar.cc/300?img=45",
    },
]

FLANS = [
    # === VANILLA ===
    {
        "name": "Pudim Clássico da Vovó",
        "description": "A receita original. Leite condensado, leite, ovos, baunilha e uma pitada de amor incondicional que você nunca vai conseguir replicar. A Vovó Aparecida faz esse pudim há 50 anos e toda vez que você tenta copiar, não fica igual. Aceite.",
        "flan_type": "vanilla",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500",
        "creator_name": "Vovó Aparecida",
    },
    {
        "name": "Vanilla Bean Supreme",
        "description": "Flan de baunilha com favas de baunilha de Madagascar. Não é a fava falsa em pó. É a fava real que custa R$47 cada uma. Gordon Hamsey não aceita substitutos e você também não deveria.",
        "flan_type": "vanilla",
        "is_premium": True,
        "price": Decimal("8.99"),
        "image_url": "https://images.unsplash.com/photo-1464305795204-6f5bbfc7fb81?w=500",
        "creator_name": "Gordon Hamsey",
    },
    {
        "name": "Flan Português do Porto",
        "description": "12 gemas, leite condensado, leite evaporado e um cálice de vinho do Porto. Receita trazida de Portugal em 1987 pela avó da avó. Altamente viciante. Não nos responsabilizamos pela dependência emocional gerada.",
        "flan_type": "vanilla",
        "is_premium": True,
        "price": Decimal("7.49"),
        "image_url": "https://images.unsplash.com/photo-1519915028121-7d3463d5b1c3?w=500",
        "creator_name": "Chef Pierre Flançois",
    },
    {
        "name": "Pudim de Micro-ondas (Funciona, Juro)",
        "description": "Chad prometeu que funciona. Chad errou algumas vezes mas agora está 70% seguro que funciona. Tempo: 8 minutos. Resultado: surpreendentemente aceitável.",
        "flan_type": "vanilla",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500",
        "creator_name": "Chad Flansworth",
    },
    {
        "name": "Leche Flan Filipino",
        "description": "12 gemas, leite condensado e leite evaporado. Assado em banho-maria com papel alumínio. A versão filipina é mais densa, mais rica e mais perigosa para o colesterol do que qualquer coisa que você já comeu. Extremamente premium.",
        "flan_type": "vanilla",
        "is_premium": True,
        "price": Decimal("9.99"),
        "image_url": "https://images.unsplash.com/photo-1486427944299-d1955d23e34d?w=500",
        "creator_name": "FlanQueen69",
    },

    # === CHOCOLATE ===
    {
        "name": "Pudim de Brigadeiro",
        "description": "Quando você não conseguia escolher entre pudim e brigadeiro, então alguém genial decidiu que não era necessário. Calda de chocolate, textura de pudim, sabor de brigadeiro. Um escândalo culinário absolutamente aprovado.",
        "flan_type": "chocolate",
        "is_premium": True,
        "price": Decimal("6.99"),
        "image_url": "https://images.unsplash.com/photo-1606313564200-e75d5e30476c?w=500",
        "creator_name": "Vovó Aparecida",
    },
    {
        "name": "Dark Chocolate Obsession",
        "description": "Chocolate 70% cacau. Não o chocolate ao leite das crianças. Chocolate de adulto, para pessoas que fazem escolhas sérias na vida. Gordon Hamsey aprova. Sua cardiologista não aprova. Você decide.",
        "flan_type": "chocolate",
        "is_premium": True,
        "price": Decimal("11.99"),
        "image_url": "https://images.unsplash.com/photo-1578985545062-69928b1d9587?w=500",
        "creator_name": "Gordon Hamsey",
    },
    {
        "name": "Pudim de Chocolate com Morango",
        "description": "Chocolate + morango = combinação que existe há séculos por uma razão. Pedaços de morango fresco embutidos no pudim de chocolate. FlanQueen69 fez esse para o Valentine's Day e o namorado chorou. De emoção. Provavelmente.",
        "flan_type": "chocolate",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1565958011703-44f9829ba187?w=500",
        "creator_name": "FlanQueen69",
    },

    # === COCONUT ===
    {
        "name": "Pudim de Coco Queimado",
        "description": "Coco queimado dá um sabor defumado e incrível ao pudim tradicional. Chef Pierre descobriu isso por acidente quando esqueceu o coco no forno. O acidente virou receita. A receita virou hit. O hit virou sua identidade.",
        "flan_type": "coconut",
        "is_premium": True,
        "price": Decimal("8.49"),
        "image_url": "https://images.unsplash.com/photo-1559181567-c3190bbbdc94?w=500",
        "creator_name": "Chef Pierre Flançois",
    },
    {
        "name": "Flan de Coco com Abacaxi",
        "description": "Tropical. Refrescante. Polêmico. Metade das pessoas ama a combinação coco+abacaxi. A outra metade acha um crime culinário. Vovó Benedita não tem tempo para opiniões negativas e faz esse pudim desde 1989.",
        "flan_type": "coconut",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1490323914169-4b24bbb46f09?w=500",
        "creator_name": "Vovó Benedita",
    },
    {
        "name": "Coconut Paradise 🌴",
        "description": "Leite de coco, coco ralado fresco, coco em flocos, coco queimado por cima. Se você tem medo de coco, saia. Se você ama coco, este é o seu templo. FlanQueen69 foi a Bali criar essa receita. Você vai notar.",
        "flan_type": "coconut",
        "is_premium": True,
        "price": Decimal("9.49"),
        "image_url": "https://images.unsplash.com/photo-1562440499-64c9a111f713?w=500",
        "creator_name": "FlanQueen69",
    },

    # === COFFEE ===
    {
        "name": "Espresso Flan às 11pm",
        "description": "Gordon Hamsey criou esse às 11 da noite depois de um serviço de 14 horas. Não é recomendado para quem tem ansiedade, insônia ou reunião às 8h. Para os demais: absolutamente imprescindível.",
        "flan_type": "coffee",
        "is_premium": True,
        "price": Decimal("8.99"),
        "image_url": "https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=500",
        "creator_name": "Gordon Hamsey",
    },
    {
        "name": "Pudim de Café com Leite Condensado",
        "description": "Café forte + leite condensado + uma filosofia de vida que diz que o café deve estar em tudo, inclusive sobremesas. Vovó Benedita toma isso com café da manhã. Não julgue.",
        "flan_type": "coffee",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1461023058943-07fcbe16d735?w=500",
        "creator_name": "Vovó Benedita",
    },

    # === SPECIAL ===
    {
        "name": "Pudim de Paçoca 🥜",
        "description": "Amendoim caramelizado, paçoca esfarelada por cima, calda de caramelo com amendoim. Não é para quem é alérgico a amendoim. Para todos os outros: bem-vindo ao Brasil.",
        "flan_type": "special",
        "is_premium": True,
        "price": Decimal("7.99"),
        "image_url": "https://images.unsplash.com/photo-1563729784474-d77dbb933a9e?w=500",
        "creator_name": "Vovó Aparecida",
    },
    {
        "name": "Flan de Frutas Vermelhas",
        "description": "Morango, framboesa, mirtilo e amora sobre pudim clássico. Parece chique. Na verdade é o jeito de FlanQueen69 fingir que come fruta. Esteticamente perfeito para Instagram. Emocionalmente reconfortante.",
        "flan_type": "special",
        "is_premium": True,
        "price": Decimal("10.99"),
        "image_url": "https://images.unsplash.com/photo-1488477181946-6428a0291777?w=500",
        "creator_name": "FlanQueen69",
    },
    {
        "name": "Pudim de Chá Verde Matcha",
        "description": "Matcha japonês de cerimônia dá cor verde linda e sabor único ao pudim. Chad tentou fazer com chá verde de saquinho. Não ficou igual. Chef Pierre foi ao Japão buscar o matcha correto. Isso é dedicação ou insanidade? Sim.",
        "flan_type": "special",
        "is_premium": True,
        "price": Decimal("12.99"),
        "image_url": "https://images.unsplash.com/photo-1515823064-d6e0c04616a7?w=500",
        "creator_name": "Chef Pierre Flançois",
    },
    {
        "name": "O Flan do Chad (Revisão 47)",
        "description": "Esta é a 47ª versão do flan do Chad. As 46 primeiras não eram ruins, eram apenas... experiências. Esta aqui está genuinamente boa. Chad está orgulhoso. Por favor não diga que preferia a versão 23.",
        "flan_type": "special",
        "is_premium": False,
        "price": Decimal("0.00"),
        "image_url": "https://images.unsplash.com/photo-1551024506-0bccd828d307?w=500",
        "creator_name": "Chad Flansworth",
    },
]

SUBSCRIBERS = [
    {"email": "flanfanatica@gmail.com", "name": "Ana Flan"},
    {"email": "pudimparaiso@hotmail.com", "name": "Carlos Eduardo"},
    {"email": "souviverdeflan@gmail.com", "name": "Beatriz"},
    {"email": "flan.devotee@outlook.com", "name": "Roberto"},
    {"email": "caramelfever@gmail.com", "name": "Mariana"},
]


class Command(BaseCommand):
    help = "Seeds the database with glorious flan data 🍮"

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Clear existing data before seeding',
        )

    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write("🗑️  Clearing existing data...")
            Flan.objects.all().delete()
            FlanCreator.objects.all().delete()
            Subscriber.objects.all().delete()
            self.stdout.write(self.style.WARNING("Cleared!"))

        # Create admin user if needed
        admin, created = User.objects.get_or_create(
            username='admin',
            defaults={'email': 'admin@onlyflans.com',
                      'is_staff': True, 'is_superuser': True}
        )
        if created:
            admin.set_password('flanpassword123')
            admin.save()
            self.stdout.write(self.style.SUCCESS(
                "👤 Admin user created (admin / flanpassword123)"))

        # Seed creators
        self.stdout.write("\n🍳 Creating creators...")
        creator_map = {}
        for data in CREATORS:
            creator, created = FlanCreator.objects.get_or_create(
                name=data['name'],
                defaults={k: v for k, v in data.items() if k != 'name'}
            )
            creator_map[creator.name] = creator
            icon = "✨" if created else "⏭️ "
            self.stdout.write(f"  {icon} {creator.name}")

        # Seed flans
        self.stdout.write("\n🍮 Creating flans...")
        for data in FLANS:
            creator_name = data.pop('creator_name')
            creator = creator_map.get(creator_name)

            flan, created = Flan.objects.get_or_create(
                name=data['name'],
                defaults={
                    **data,
                    'creator': admin,
                    'featured_creator': creator,
                }
            )
            icon = "✨" if created else "⏭️ "
            premium = "💎" if flan.is_premium else "🆓"
            self.stdout.write(f"  {icon} {premium} {flan.name}")

            # Restore for next iteration
            data['creator_name'] = creator_name

        # Seed subscribers
        self.stdout.write("\n📧 Creating subscribers...")
        for data in SUBSCRIBERS:
            sub, created = Subscriber.objects.get_or_create(
                email=data['email'],
                defaults=data
            )
            icon = "✨" if created else "⏭️ "
            self.stdout.write(f"  {icon} {sub.email}")

        # Summary
        self.stdout.write("\n" + "="*50)
        self.stdout.write(self.style.SUCCESS(
            f"✅ Done! {Flan.objects.count()} flans, "
            f"{FlanCreator.objects.count()} creators, "
            f"{Subscriber.objects.count()} subscribers"
        ))
        self.stdout.write("🚀 Run: python manage.py runserver")
        self.stdout.write(
            "🔑 Admin: http://localhost:8000/admin (admin / flanpassword123)")
