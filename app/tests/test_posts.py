from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_post_and_like():
    # garantir user
    u = client.post("/users", json={"username":"post_user_x","email":"post_user_x@test.com","posts":0}).json()
    user_id = u["id"]
    # criar post
    p = client.post("/posts", json={"user_id": user_id, "content":"Hello world"}).json()
    post_id = p["id"]
    assert p["likes"] == 0
    assert p["user_id"] == user_id
    # like
    liked = client.post(f"/posts/{post_id}/like").json()
    assert liked["likes"] == 1

def test_feed_pagination():
    r = client.get("/feed?page=1&size=3")
    assert r.status_code == 200
    body = r.json()
    assert body["page"] == 1
    assert body["size"] == 3
    assert "total" in body
    assert len(body["items"]) <= 3

def test_users_with_posts_pagination():
    r = client.get("/users-with-posts?page=1&size=2")
    assert r.status_code == 200
    body = r.json()
    assert body["page"] == 1
    assert body["size"] == 2
    assert "total" in body
    assert len(body["users"]) <= 2
