def test_logout_success(client, common_user_authenticated):
    # response = client.delete(
    #     f"/logout/{common_user_authenticated.user_id}", 
        
    # )

    pass


def test_logout_with_does_not_existent_user(client):
    pass


def test_logout_with_no_permission_user(client):
    # um usuario tenta deslogar outro
    pass
