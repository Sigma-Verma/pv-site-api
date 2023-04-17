""" Test for main app """

from pv_site_api.pydantic_models import Inverters


def test_get_inverters_fake(client, fake):
    response = client.get("/inverters")
    assert response.status_code == 200

    inverters = Inverters(**response.json())
    assert len(inverters.inverters) > 0


def test_get_inverters(client, httpx_mock, clients):
    httpx_mock.add_response(url="https://enode-api.production.enode.io/inverters", json=["id1"])

    httpx_mock.add_response(
        url="https://enode-api.production.enode.io/inverters/id1",
        json={
            "id": "string",
            "vendor": "EMA",
            "chargingLocationId": "8d90101b-3f2f-462a-bbb4-1ed320d33bbe",
            "lastSeen": "2020-04-07T17:04:26Z",
            "isReachable": True,
            "productionState": {
                "productionRate": 0,
                "isProducing": True,
                "totalLifetimeProduction": 100152.56,
                "lastUpdated": "2020-04-07T17:04:26Z",
            },
            "information": {
                "id": "string",
                "brand": "EMA",
                "model": "Sunny Boy",
                "siteName": "Sunny Plant",
                "installationDate": "2020-04-07T17:04:26Z",
            },
            "location": {"longitude": 10.7197486, "latitude": 59.9173985},
        },
    )

    response = client.get("/inverters")
    assert response.status_code == 200

    inverters = Inverters(**response.json())
    assert len(inverters.inverters) > 0
