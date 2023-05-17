import pydantic

import VkApiModule


class VkPhotoSizes(pydantic.BaseModel):
    height: int
    width: int
    url: str


class VkPhoto(pydantic.BaseModel):
    id: int
    post_id: int | None
    sizes: list[VkPhotoSizes]

    def get_max_photo_size(self) -> VkPhotoSizes:
        return sorted(self.sizes, key=lambda size: size.height and size.width)[-1]


class VkVideo(pydantic.BaseModel):
    id: int
    owner_id: int
    title: str
    description: str
    duration: int
    date: int

    def get_video_url(self) -> str:
        return f"https://vk.com/video{self.owner_id}_{self.id}"


class VkAttachment(pydantic.BaseModel):
    type: str
    photo: VkPhoto | None
    video: VkVideo | None
    audio: dict | None
    doc: dict | None




class VkPost(pydantic.BaseModel):
    type: str
    id: int
    date: int
    text: str | None
    comments: dict | None
    attachments: list[VkAttachment] | None
    views: dict | None
    copy_history: list | None

    def get_copy_history(self):
        return get_copy_history(self)


def get_copy_history(self: VkPost) -> VkPost | None:
    if self.copy_history:
        return VkPost.parse_obj(self.copy_history[0])
    return None


class VkPosts(pydantic.BaseModel):
    group_id: int
    posts: list[VkPost] | None
    error_code: int | None


class VkLastPostId(pydantic.BaseModel):
    group_id: int | None
    id: int | None
    error_code: int | None


class VkGroupInfo(pydantic.BaseModel):
    id: int | None
    name: str | None
    screen_name: str | None
    photo_200: str | None
    error_code: int | None


class VkParserGroupId(pydantic.BaseModel):
    token: str
    group_id: int


class VkParserGroupDomain(pydantic.BaseModel):
    token: str
    domain: str


class VkParserGroupPosts(pydantic.BaseModel):
    token: str
    group_id: int
    last_post_id: int
    count_post_parse: int


class VkParserCommentPost(pydantic.BaseModel):
    token: str
    group_id: int
    post_id: int
    comment: str


class GroupUpdated(pydantic.BaseModel):
    group_id: int
    last_post_id: int
    tokens: list[str]


class GroupsUpdated(pydantic.BaseModel):
    groups: list[GroupUpdated]

    def get_group_by_id(self, group_id: int) -> list[GroupUpdated]:
        filtered = filter(
            lambda group: group.group_id == group_id,
            self.groups
        )
        return list(filtered)

    def add_group(self, group_data):
        if len(group_data) == 3:
            group = self.get_group_by_id(group_data[0])
            if group:
                group[0].tokens.append(group_data[2])
            else:
                self.groups.append(GroupUpdated(
                    group_id=group_data[0], last_post_id=group_data[1], tokens=[group_data[2]]
                ))
