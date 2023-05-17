import aiohttp
import asyncio

from OtherModule import CONFIG
from .ParseClasses import (
    VkLastPostId, VkGroupInfo, VkPost, VkPosts,
    VkParserGroupDomain, VkParserGroupPosts, VkParserCommentPost, VkParserGroupId,
    GroupUpdated, GroupsUpdated

)


class VkParser:
    def __init__(self):
        self.__start_link = CONFIG.START_LINK
        self.__version = CONFIG.VERSION

    def fun(self):
        pass

    async def get_group_info_by_domain(self, data: VkParserGroupDomain) -> VkGroupInfo:
        """
        :param data: VkParserGroupDomain:
                token : str
                domain : str
        :return: VkGroupInfo
        """
        session = aiohttp.ClientSession()
        try:
            link = f"{self.__start_link}utils.resolveScreenName?" \
                   f"screen_name={data.domain}&access_token={data.token}&{self.__version}"
            req = await session.get(link)
            req = await req.json()
            if 'response' in req:
                if 'type' in req['response'] and req['response']['type'] == 'group':
                    new_data = VkParserGroupId(token=data.token, group_id=req['response']['object_id'])
                    return await self.__task_get_group_info(new_data, session)
                else:
                    error_code = 0
            else:
                error_code = req["error"]["error_code"]
            return VkGroupInfo(error_code=error_code)
        finally:
            await session.close()

    async def check_correct_token(self, token: str, session=None, group_name: str = 'vk') -> bool:
        """
        :param token: str, user token
        :param session: None | aiohttp.ClientSession()
        :param group_name: str, check domain vk group
        :return: bool,  True | False
        """
        if not session:
            session = aiohttp.ClientSession()
        try:
            link = f"{self.__start_link}wall.get?" \
                   f"domain={group_name}&count={1}&access_token={token}&{self.__version}"
            req = await session.get(link)
            if 'error' in await req.json():
                return False
            return True
        finally:
            await session.close()

    async def __task_get_last_post_id(self, data: VkParserGroupId, session) -> VkLastPostId:
        link = f"{self.__start_link}wall.get?owner_id={-data.group_id}&count=2&access_token={data.token}&{self.__version}"
        req, res = await session.get(link), 0
        req = await req.json()
        if 'response' in req:
            for item in req['response']['items']:
                res = max(item['id'], res)
            return VkLastPostId.parse_obj({"group_id": data.group_id, "id": res})
        return VkLastPostId.parse_obj({"error_code": req["error"]["error_code"]})

    async def get_group_last_post_id(self, data: VkParserGroupId) -> VkLastPostId:
        """
        :param data: VkParserGroupId:
                token : str
                group_id : int
        :return: VkLastPostId
        """
        session = aiohttp.ClientSession()
        try:
            return await self.__task_get_last_post_id(data, session)
        finally:
            await session.close()

    async def get_groups_last_posts_id(self, all_data: list[VkParserGroupId], session=None) -> list[VkLastPostId]:
        """
        :param all_data: list[VkParserGroupId]:
                    token : str
                    group_id : int
        :param session: None | aiohttp.ClientSession()
        :return: list[VkLastPostId]
        """
        if not session:
            session = aiohttp.ClientSession()
        try:
            tasks = []
            for data in all_data:
                tasks.append(asyncio.create_task(self.__task_get_last_post_id(data, session)))
            return await asyncio.gather(*tasks)
        finally:
            await session.close()

    async def __task_get_posts(self, data: GroupUpdated, session) -> VkPosts:
        for token in data.tokens:
            link = f"{self.__start_link}wall.get?owner_id={-data.group_id}&count=" \
                   f"{CONFIG.PARSE_COUNT_POSTS}&access_token={token}&{self.__version}"
            req = await session.get(link)
            req = await req.json()
            if 'response' in req:
                posts_data = {"group_id": data.group_id, "posts": []}
                for item in req['response']['items']:
                    if item['id'] > data.last_post_id:
                        posts_data["posts"].append(VkPost.parse_obj(item))
                return VkPosts.parse_obj(posts_data)

    async def get_group_posts(self, data: GroupUpdated, session=None) -> VkPosts:
        """"""
        try:
            if not session:
                session = aiohttp.ClientSession()
            return await self.__task_get_posts(data, session)
        finally:
            await session.close()

    async def get_groups_posts(self, all_data: GroupsUpdated, session=None) -> list[VkPosts]:
        """"""
        if not session:
            session = aiohttp.ClientSession()
        try:
            tasks = []
            for data in all_data.groups:
                tasks.append(asyncio.create_task(self.__task_get_posts(data, session)))
            return await asyncio.gather(*tasks)
        finally:
            await session.close()

    async def __task_get_group_info(self, data: VkParserGroupId, session) -> VkGroupInfo:
        link = f"{self.__start_link}groups.getById?" \
               f"group_id={data.group_id}&access_token={data.token}&{self.__version}"
        req = await session.get(link)
        req = await req.json()
        if 'response' in req:
            return VkGroupInfo.parse_obj(req['response'][0])
        return VkGroupInfo.parse_obj({'error_code': req["error"]["error_code"]})

    async def get_group_info(self, data: VkParserGroupId) -> VkGroupInfo:
        """
        :param data: VkParserGroupId:
                token : str
                group_id : int
        :return: VkGroupInfo
        """
        session = aiohttp.ClientSession()
        try:
            return await self.__task_get_group_info(data, session)
        finally:
            await session.close()

    async def __task_new_comment(self, data: VkParserCommentPost, session):
        link = f"{self.__start_link}wall.createComment?owner_id={-data.group_id}&post_id={data.post_id}&" \
               f"access_token={data.token}&message={data.comment}&{self.__version}"
        req = await session.get(link)
        req = await req.json()
        if 'response' in req:
            return True
        return False

    async def new_comment(self, data: VkParserCommentPost, session=None) -> bool:
        if not session:
            session = aiohttp.ClientSession()
        try:
            return await self.__task_new_comment(data, session)
        finally:
            await session.close()


vk_parser = VkParser()
