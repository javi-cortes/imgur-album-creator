from imgurpython import ImgurClient
from dotenv import load_dotenv
import os


class ImgurClientWrapper:
    def __init__(self, credentials=None) -> None:
        load_dotenv()
        self.client_id = os.getenv("IMGUR_CLIENT_ID")
        self.client_secret = os.getenv("IMGUR_CLIENT_SECRET")

        if not all((self.client_id, self.client_secret)):
            raise "You need to set up your CLIENT_ID and CLIENT_SECRET on your .env file"

        print(self.client_id, self.client_secret)
        self.client = ImgurClient(self.client_id, self.client_secret)

        if not credentials:
            credentials = self.auth_flow()

        print(f"Setting user authentication: Access + Refresh tokens")
        self.client.set_user_auth(credentials["access_token"], credentials["refresh_token"])

    def auth_flow(self):
        print(f"Starting Authentication flow")

        # Authorization flow, pin example (see docs for other auth types)
        authorization_url = self.client.get_auth_url("pin")
        print(f"Go to {authorization_url} and write the pin code\npincode:")
        pincode = input()

        print(f"Getting credentials with the provided pin code")
        credentials = self.client.authorize(pincode, "pin")

        print(f"Authentication flow ended successfully")

        return credentials

    def create_album(self):
        album_response = self.client.create_album(
            {
                "title": "API calls",
            }
        )
        return album_response["id"]

    def upload_image_to_imgur(self, image_url) -> str:
        print(f"UPLOADING {image_url} to imgur")
        try:
            upload_response = self.client.upload_from_url(image_url, anon=False)
        except Exception as e:
            print(e)
            return ""
        print(f"UPLOADED {image_url} to imgur: {upload_response['id']}")
        return upload_response['id']

    def add_image_to_album(self, album_id, image_imgur_ids):
        album_response = self.client.album_add_images(album_id, image_imgur_ids)

        print(f"{image_imgur_ids} added to album {album_id}")


if __name__ == "__main__":
    imgurclient = ImgurClientWrapper()
    # creds on imgurclient if authflow is ok
    # now you can use your own album or just create one
    # album_id imgurclient.create_album()

