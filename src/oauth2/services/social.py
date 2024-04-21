from abc import ABC, abstractmethod


class SocialInfo(ABC):
    def __init__(self, source: str):
        self.source = source

    def _get_user_names(self, fullname="", first_name="", last_name=""):
        fullname = fullname or ""
        first_name = first_name or ""
        last_name = last_name or ""
        if fullname and not (first_name or last_name):
            try:
                first_name, last_name = fullname.split(" ", 1)
            except ValueError:
                first_name = first_name or fullname or ""
                last_name = last_name or ""
        fullname = fullname or " ".join((first_name, last_name))
        return fullname.strip(), first_name.strip(), last_name.strip()

    @abstractmethod
    def get_social_data(self, userinfo: dict) -> tuple[str, dict]:
        pass

    @staticmethod
    def factory(source: str) -> "SocialInfo":
        mapping = {"google": GoogleInfo, "github": GithubInfo, "linkedin": LinkedinInfo}

        cls = mapping.get(source, SocialInfo)
        return cls(source)


class GoogleInfo(SocialInfo):
    def get_social_data(self, userinfo: dict) -> tuple[str, dict]:
        email = userinfo.get("email")
        avatar = userinfo.get("avatar")
        username = email.split("@", 1).pop(0)
        fullname, first_name, last_name = self._get_user_names(
            fullname=userinfo.get("name"),
            first_name=userinfo.get("given_name"),
            last_name=userinfo.get("family_name"),
        )

        data = dict(
            email=email,
            avatar=avatar,
            username=username,
            first_name=first_name,
            last_name=last_name,
            fullname=fullname,
        )

        return email, data


class GithubInfo(SocialInfo):
    def get_social_data(self, userinfo: dict) -> tuple[str, dict]:
        username = userinfo.get("login")
        avatar = userinfo.get("avatar_url")
        email = userinfo.get("email") or f"{username}@github.com"
        fullname, first_name, last_name = self._get_user_names(userinfo.get("name", username))

        data = dict(
            email=email,
            avatar=avatar,
            username=username,
            first_name=first_name,
            last_name=last_name,
            fullname=fullname,
        )
        return email, data


class LinkedinInfo(SocialInfo):
    def get_social_data(self, userinfo: dict) -> tuple[str, dict]:
        email = userinfo.get("email")
        avatar = userinfo.get("picture", "")
        username = email.split("@", 1).pop(0)
        fullname, first_name, last_name = self._get_user_names(
            fullname=userinfo.get("name"),
            first_name=userinfo.get("given_name"),
            last_name=userinfo.get("family_name"),
        )

        data = dict(
            email=email,
            avatar=avatar,
            username=username,
            first_name=first_name,
            last_name=last_name,
            fullname=fullname,
        )

        return email, data
