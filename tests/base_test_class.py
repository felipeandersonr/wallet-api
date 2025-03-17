from requests import Response
from starlette.testclient import TestClient


class BaseTest:
    @staticmethod
    def request_client_post(client: TestClient, 
                            router_url: str, 
                            authorization_token: str | None = None, 
                            json_data: dict | None = None) -> Response:
        
        headers = {}

        if authorization_token:
            headers = {"Authorization": f"Bearer {authorization_token}"}

        response = client.post(
            url=router_url, 
            json=json_data,
            headers=headers
        )

        return response
    

    @staticmethod
    def request_client_form_post(client: TestClient,
                                 router_url: str,
                                 authorization_token: str | None = None,
                                 form_data: dict | None = None) -> Response:
        
        headers = {}

        if authorization_token:
            headers["Authorization"] = f"Bearer {authorization_token}"
            
        response = client.post(
            url=router_url,
            data=form_data,
            headers=headers
        )
        
        return response
    

    @staticmethod
    def request_client_get(client: TestClient, router_url: str, authorization_token: str | None = None) -> Response:
        headers = {}

        if authorization_token:
            headers = {"Authorization": f"Bearer {authorization_token}"}

        response = client.get(
            url=router_url, 
            headers=headers
        )

        return response


    @staticmethod
    def request_client_delete(client: TestClient, router_url: str, authorization_token: str | None = None) -> Response:
        headers = {}

        if authorization_token:
            headers = {"Authorization": f"Bearer {authorization_token}"}
        
        response = client.delete(
            url=router_url,
            headers=headers
        )
        
        return response
