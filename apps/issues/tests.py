"""Example pytest-django tests for the /vueapi/ DRF surface.

Pattern for new endpoint tests:
  1. Arrange: seed the minimum domain state the endpoint touches (fixtures below).
  2. Act: hit the URL with `client`, JSON in / JSON out.
  3. Assert: response shape + side effects on the DB.

Any test that touches the DB must be marked with @pytest.mark.django_db.
"""
import pytest
from django.contrib.auth import get_user_model

from apps.issues.models.ideas import Ideas, UserIdeaVote


@pytest.fixture
def voter(db):
    return get_user_model().objects.create_user(username='voter', password='pw')


@pytest.fixture
def idea(db):
    # No createdByUser — keeps the test off the reputation/UserInfo path.
    idea = Ideas.newIdea(content='self-host a forum')
    idea.save()
    return idea


@pytest.fixture
def logged_in_client(client, voter):
    client.force_login(voter)
    return client


def test_up_vote_increments_score_and_records_vote(logged_in_client, voter, idea):
    response = logged_in_client.post(
        '/vueapi/idea_vote',
        data={'id': idea.id, 'vote_type': 'up'},
        content_type='application/json',
    )

    assert response.status_code == 200
    assert response.json() == {'result': 'success'}

    idea.refresh_from_db()
    assert idea.point == 1
    assert UserIdeaVote.objects.filter(idea=idea, user=voter, voteType='UP').count() == 1


def test_up_cancel_reverses_previous_up_vote(logged_in_client, voter, idea):
    logged_in_client.post(
        '/vueapi/idea_vote',
        data={'id': idea.id, 'vote_type': 'up'},
        content_type='application/json',
    )

    response = logged_in_client.post(
        '/vueapi/idea_vote',
        data={'id': idea.id, 'vote_type': 'up_cancel'},
        content_type='application/json',
    )

    assert response.status_code == 200
    idea.refresh_from_db()
    assert idea.point == 0
    assert not UserIdeaVote.objects.filter(idea=idea, user=voter, voteType='UP').exists()
