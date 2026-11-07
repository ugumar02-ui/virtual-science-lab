from content import PRACTICALS
from fastapi.testclient import TestClient
from server.main import app

client = TestClient(app)
failures = 0
for p in PRACTICALS:
    r = client.post(f"/practicals/{p['id']}/run", json={"controls": {}, "seed": 1})
    ok = r.status_code == 200 and r.json()["result"].get("kind") in ("quantitative", "qualitative")
    print("OK  " if ok else "FAIL", p["id"], "" if ok else r.text[:150])
    failures += not ok
print("failures:", failures)
