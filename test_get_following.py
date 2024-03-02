import json

import stweet as st
from stweet.http_request.requests import RequestsWebClient, RequestsWebClientProxyConfig
from stweet.twitter_api.default_twitter_web_client_provider import TwitterAuthWebClientInterceptor

class API:
    def __init__(self, proxies = None):
        if proxies is None:
            self.proxies = dict()
        else:
            self.proxies = proxies

    def get_user(self, username: str) -> dict:
        user_task = st.GetUsersTask([username])
        collector = st.CollectorRawOutput()

        proxy_cfg = None
        if len(self.proxies) > 0:
            proxy_cfg = RequestsWebClientProxyConfig(self.proxies["http"], self.proxies["https"])

        client = RequestsWebClient(
            proxy = proxy_cfg,
            verify = False,
            interceptors=[TwitterAuthWebClientInterceptor()]
        )

        st.GetUsersRunner(
            get_user_task = user_task, 
            raw_data_outputs=[collector],
            web_client = client
        ).run()

        rawlist = collector.get_raw_list()
        if len(rawlist) == 0:
            raise Exception("List[RawData] returned by Twitter GetUsersTask is empty.")

        json_str= rawlist[0].raw_value
        data = json.loads(json_str)["legacy"]
        if not "profile_banner_url" in data:
            data["profile_banner_url"] = ""

        return data

# twitter = API()
# user = twitter.get_user("ooojstn")
# print(user)

client = RequestsWebClient(
    verify = False,
    interceptors=[TwitterAuthWebClientInterceptor()]
)
from stweet.twitter_api.default_twitter_web_client_provider import DefaultTwitterWebClientProvider
from stweet.twitter_api.twitter_api_requests import TwitterApiRequests
# client = DefaultTwitterWebClientProvider.get_web_client()
req = TwitterApiRequests().get_following_request_by_user_id("21761627")
print(req)
resp = client.run_request(req)
print(resp)

