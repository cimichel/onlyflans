from django.test import TestCase

"""
OnlyFlans Test Suite 🍮
pytest tests for models, views, and API endpoints.

Run with: pytest flans/tests.py -v
"""
import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from .models import Flan, FlanCreator, FlanRating, Subscriber


# ============================================================
# FIXTURES
# ============================================================

@pytest.fixture
def user(db):
    return User.objects.create_user(
        username='flanfan', password='flanpassword123'
    )


@pytest.fixture
def another_user(db):
    return User.objects.create_user(
        username='flanfan2', password='flanpassword456'
    )


@pytest.fixture
def creator(db):
    return FlanCreator.objects.create(
        name="Gordon Hamsey",
        creator_type=FlanCreator.CreatorType.CHEF,
        bio="I've been making flans for 40 years and I'll do it again.",
        is_featured=True,
        total_earnings=Decimal('9999.99'),
        satisfaction_rate=100,
    )


@pytest.fixture
def free_flan(db, user, creator):
    return Flan.objects.create(
        name="Basic Vanilla",
        description="A humble flan for humble folk.",
        flan_type=Flan.FlanType.VANILLA,
        is_premium=False,
        creator=user,
        featured_creator=creator,
    )


@pytest.fixture
def premium_flan(db, user):
    return Flan.objects.create(
        name="Gold Chocolate Dream",
        description="Premium flan for premium people.",
        flan_type=Flan.FlanType.CHOCOLATE,
        is_premium=True,
        price=Decimal('9.99'),
        creator=user,
    )


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def auth_client(client, user):
    client.login(username='flanfan', password='flanpassword123')
    return client


# ============================================================
# MODEL TESTS
# ============================================================

class TestFlanModel:

    def test_free_flan_price_forced_to_zero(self, free_flan):
        """Saving a non-premium flan should always set price to 0."""
        free_flan.price = Decimal('99.99')
        free_flan.save()
        free_flan.refresh_from_db()
        assert free_flan.price == Decimal('0.00')

    def test_premium_flan_keeps_price(self, premium_flan):
        """Premium flans should keep their price."""
        assert premium_flan.price == Decimal('9.99')

    def test_display_price_free(self, free_flan):
        assert free_flan.get_display_price() == "FREE"

    def test_display_price_premium(self, premium_flan):
        assert premium_flan.get_display_price() == "$9.99"

    def test_short_description_truncates(self, user):
        long_desc = "A" * 200
        flan = Flan.objects.create(
            name="Long Flan",
            description=long_desc,
            flan_type=Flan.FlanType.VANILLA,
            creator=user,
        )
        assert len(flan.short_description) == 103  # 100 + '...'
        assert flan.short_description.endswith('...')

    def test_short_description_no_truncation(self, free_flan):
        free_flan.description = "Short description"
        free_flan.save()
        assert free_flan.short_description == "Short description"

    def test_str_premium_flag(self, premium_flan):
        assert "🌟" in str(premium_flan)

    def test_str_no_premium_flag(self, free_flan):
        assert "🌟" not in str(free_flan)


class TestFlanCreatorModel:

    def test_total_flans_is_calculated(self, creator, free_flan):
        """total_flans should reflect actual DB count, not stored field."""
        assert creator.total_flans == 1

    def test_total_flans_zero(self, creator):
        creator.flans.all().delete()
        assert creator.total_flans == 0

    def test_is_popular_high_earnings(self, creator):
        creator.total_earnings = Decimal('5000.00')
        creator.satisfaction_rate = 50
        creator.save()
        assert creator.is_popular is True

    def test_is_popular_high_satisfaction(self, creator):
        creator.total_earnings = Decimal('0.00')
        creator.satisfaction_rate = 95
        creator.save()
        assert creator.is_popular is True

    def test_is_popular_false(self, db):
        unpopular = FlanCreator.objects.create(
            name="Sad Baker",
            creator_type=FlanCreator.CreatorType.AMATEUR,
            bio="I try.",
            total_earnings=Decimal('0.00'),
            satisfaction_rate=50,
        )
        assert unpopular.is_popular is False

    def test_earnings_display(self, creator):
        assert "$" in creator.earnings_display

    def test_get_flans_count_display_zero(self, db):
        creator = FlanCreator.objects.create(
            name="Newbie",
            creator_type=FlanCreator.CreatorType.AMATEUR,
            bio="Just started."
        )
        assert creator.get_flans_count_display() == "Just starting out"

    def test_get_flans_count_display_one(self, creator, free_flan):
        assert "1 amazing flan" in creator.get_flans_count_display()


class TestFlanRatingModel:

    def test_one_rating_per_user_per_flan(self, db, user, free_flan):
        """unique_together should prevent duplicate ratings."""
        from django.db import IntegrityError
        FlanRating.objects.create(flan=free_flan, user=user, score=5)
        with pytest.raises(IntegrityError):
            FlanRating.objects.create(flan=free_flan, user=user, score=3)

    def test_update_or_create_rating(self, db, user, free_flan):
        """update_or_create should update existing rating, not create duplicate."""
        FlanRating.objects.create(flan=free_flan, user=user, score=3)
        rating, created = FlanRating.objects.update_or_create(
            flan=free_flan,
            user=user,
            defaults={'score': 5, 'review': 'Changed my mind!'}
        )
        assert created is False
        assert rating.score == 5

    def test_str_contains_stars(self, db, user, free_flan):
        rating = FlanRating.objects.create(flan=free_flan, user=user, score=4)
        assert "🍮🍮🍮🍮" in str(rating)


class TestSubscriberModel:

    def test_display_name_uses_name(self, db):
        sub = Subscriber.objects.create(
            email="cintia@example.com", name="Cintia")
        assert sub.display_name == "Cintia"

    def test_display_name_falls_back_to_email(self, db):
        sub = Subscriber.objects.create(email="cintia@example.com")
        assert sub.display_name == "cintia"


# ============================================================
# VIEW TESTS
# ============================================================

class TestFlanListView:

    def test_flan_list_returns_200(self, client, db):
        response = client.get(reverse('flan-list'))
        assert response.status_code == 200

    def test_flan_list_filter_by_type(self, client, free_flan, premium_flan):
        response = client.get(reverse('flan-list') + '?type=vanilla')
        assert response.status_code == 200
        flans = list(response.context['flans'])
        assert all(f.flan_type == 'vanilla' for f in flans)

    def test_flan_list_pagination(self, client, user):
        # Create 15 flans (more than FLANS_PER_PAGE=9)
        for i in range(15):
            Flan.objects.create(
                name=f"Flan {i}",
                description="A flan.",
                flan_type=Flan.FlanType.VANILLA,
                creator=user,
            )
        response = client.get(reverse('flan-list'))
        assert response.status_code == 200
        assert response.context['page_obj'].has_next()


class TestFlanDetailView:

    def test_flan_detail_returns_200(self, client, free_flan):
        response = client.get(reverse('flan-detail', args=[free_flan.id]))
        assert response.status_code == 200

    def test_flan_detail_404_on_missing(self, client, db):
        response = client.get(reverse('flan-detail', args=[99999]))
        assert response.status_code == 404

    def test_flan_detail_shows_rating_stats(self, client, user, free_flan, another_user):
        FlanRating.objects.create(flan=free_flan, user=user, score=4)
        FlanRating.objects.create(flan=free_flan, user=another_user, score=2)
        response = client.get(reverse('flan-detail', args=[free_flan.id]))
        assert response.context['avg_score'] == 3.0
        assert response.context['total_ratings'] == 2


class TestRateFlanView:

    def test_rating_requires_login(self, client, free_flan):
        response = client.post(
            reverse('flan-rate', args=[free_flan.id]),
            {'score': 5}
        )
        assert response.status_code == 302
        assert '/login/' in response.url

    def test_rating_submission(self, auth_client, free_flan):
        response = auth_client.post(
            reverse('flan-rate', args=[free_flan.id]),
            {'score': 5, 'review': 'Magnificent flan!'}
        )
        assert response.status_code == 302
        assert FlanRating.objects.filter(flan=free_flan).count() == 1

    def test_invalid_score_rejected(self, auth_client, free_flan):
        response = auth_client.post(
            reverse('flan-rate', args=[free_flan.id]),
            {'score': 99}
        )
        assert FlanRating.objects.filter(flan=free_flan).count() == 0


class TestSubscribeView:

    def test_subscribe_creates_subscriber(self, client, db):
        response = client.post(
            reverse('subscribe'),
            {'email': 'flanfan@example.com', 'name': 'Flan Fan'}
        )
        assert response.status_code == 302
        assert Subscriber.objects.filter(email='flanfan@example.com').exists()

    def test_subscribe_missing_email(self, client, db):
        response = client.post(reverse('subscribe'), {'name': 'No Email'})
        assert response.status_code == 302
        assert Subscriber.objects.count() == 0


# ============================================================
# API TESTS
# ============================================================

class TestFlanAPI:

    def test_api_flan_list(self, client, free_flan, premium_flan):
        response = client.get('/api/flans/')
        assert response.status_code == 200
        assert response.json()['count'] == 2

    def test_api_flan_list_filter_premium(self, client, free_flan, premium_flan):
        response = client.get('/api/flans/?premium=true')
        assert response.status_code == 200
        assert response.json()['count'] == 1

    def test_api_flan_detail(self, client, free_flan):
        response = client.get(f'/api/flans/{free_flan.id}/')
        assert response.status_code == 200
        data = response.json()
        assert data['name'] == free_flan.name
        assert 'ratings' in data

    def test_api_flan_detail_404(self, client, db):
        response = client.get('/api/flans/99999/')
        assert response.status_code == 404

    def test_api_stats(self, client, free_flan, premium_flan):
        response = client.get('/api/stats/')
        assert response.status_code == 200
        data = response.json()
        assert data['total_flans'] == 2
        assert data['premium_flans'] == 1
        assert data['free_flans'] == 1

    def test_api_subscribe(self, client, db):
        response = client.post(
            '/api/subscribe/',
            {'email': 'api@example.com'},
            content_type='application/json'
        )
        assert response.status_code == 201

    def test_api_rating_requires_auth(self, client, free_flan):
        response = client.post(
            f'/api/flans/{free_flan.id}/ratings/',
            {'score': 5},
            content_type='application/json'
        )
        assert response.status_code == 403

    def test_api_rating_submission(self, auth_client, free_flan):
        response = auth_client.post(
            f'/api/flans/{free_flan.id}/ratings/',
            {'score': 5, 'review': 'API test review'},
            content_type='application/json'
        )
        assert response.status_code == 201
        assert FlanRating.objects.filter(flan=free_flan).count() == 1

    def test_api_rating_update(self, auth_client, user, free_flan):
        FlanRating.objects.create(flan=free_flan, user=user, score=3)
        response = auth_client.post(
            f'/api/flans/{free_flan.id}/ratings/',
            {'score': 5, 'review': 'Changed my mind'},
            content_type='application/json'
        )
        assert response.status_code == 200  # 200 = updated, not 201 created
        assert FlanRating.objects.get(flan=free_flan, user=user).score == 5
