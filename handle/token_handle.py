# coding=utf-8
import argparse
import os.path
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../")
from common import GetSessionId, TokenList, TokenCreate, BaseResponse
from settings import SETTINGS
from utils import url_join, request_post, request_get, get_logger


class TokenHandle(object):
    """
    首先判断之前是否创建过token，如果有的话直接更新到settings.json，如果没有再生成token，最后创建该token
    """
    def __init__(self):
        self._logging = get_logger(os.path.basename(__file__))
        self._get_session_id_url = url_join("/login")
        self._access_token_url = url_join("/access-tokens")
        self._get_generate_token_url = url_join("/access-tokens/generate")
        self.token = SETTINGS.TOKEN
        self._session_id = self._get_session_id()
        self._headers = {
            "Cookie": "sessionId=" + self._session_id
        }

    def _get_session_id(self):
        """
        获取session_id
        """
        params = {
            "userName": SETTINGS.USERNAME,
            "userPassword": SETTINGS.PASSWORD
        }
        session_id_instance = request_post(self._get_session_id_url, {}, params, {}, GetSessionId)
        return session_id_instance.data.sessionId

    def _get_token_list(self):
        """
        获取指定结束时间的token list
        """
        params = {
            "pageNo": "1",
            "pageSize": "50"
        }
        token_list_instance = request_get(self._access_token_url, self._headers, params, {}, TokenList)
        token_list = token_list_instance.data.totalList
        return list(filter(lambda x: str(x.expireTime) == SETTINGS.TOKEN_EXPIRE_TIME, token_list))

    def _generate_token(self):
        """
        生成token
        """
        params = {
            "userId": "1",
            "expireTime": SETTINGS.TOKEN_EXPIRE_TIME
        }
        base_instance = request_post(self._get_generate_token_url, self._headers, params, {}, BaseResponse)
        return base_instance.data
    
    def create_token(self):
        """
        创建token
        """
        token_list = self._get_token_list()
        if len(token_list) > 0:
            self.token = token_list[0].token
            self._logging.info("Token {} is already exists.".format(self.token))
        else:
            self.token = self._generate_token()
            params = {
                "userId": "1",
                "expireTime": SETTINGS.TOKEN_EXPIRE_TIME,
                "token": self.token
            }
            request_post(self._access_token_url, self._headers, params, {}, TokenCreate)
            self._logging.info("Generate token {} success.".format(self.token))
        SETTINGS.rewrite_token(self.token)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Dolphin Scheduler token operation.")
    parser.add_argument("-c", "--create", action="store_true", help="create DS token")
    args = parser.parse_args()

    if args.create:
        handle = TokenHandle()
        handle.create_token()
    else:
        parser.print_help()

