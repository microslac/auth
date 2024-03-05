from social_core.backends.github import GithubOAuth2

from oauth2.socials.strategy import SocialStrategy, UserData


class GithubStrategy(SocialStrategy):
    name = "github"
    backend_cls = GithubOAuth2

    def authorization_url(self) -> tuple[str, str | int]:
        backend = self.get_backend()
        authorization_url = backend.auth_url()
        return authorization_url, ""

    def user_details(self) -> tuple[str, UserData]:
        backend = self.get_backend()
        email, user_data = backend.get_user_response()
        return email, user_data
