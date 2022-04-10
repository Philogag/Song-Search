from enum import Enum

from backend.model.edit.master_user_em import MasterUserEm
from backend.model.edit.robot_em import RobotEm
from backend.model.edit.role_em import RoleEm


class EnumKeyNameRule(Enum):
    """"""

    underline = "下划线命名"
    camel = "驼峰命名"


class EnumHandlerCategory(Enum):
    """
    事件发起人对应实体
    category: model_name
    """

    master_user = MasterUserEm.__name__
    role = RoleEm.__name__
    system_robot = RobotEm.__name__


class EnumDataPermissionCategory(Enum):
    """
    授权类别
    """

    allow = "允许"
    allow_all = "允许所有"


class EnumRoleCode(Enum):
    """
    角色类别
    code: name
    """

    guest = "游客"
    super_admin = "系统管理员"
    test = "测试"


class EnumRobotCode(Enum):
    """
    机器人类别
    code: name
    """

    init_robot = "系统初始化机器人"
    message_queue_robot = "消息队列机器人"
    cron_robot = "定时任务机器人"


class EnumRouteCategory(Enum):
    data = "后端路由（数据路由）"
    view = "前端路由（页面路由）"


class EnumCompetitionCategory(Enum):
    """比赛项目赛制类型"""

    heats_and_finals = "预、决赛"
    final_only = "决赛"


class EnumSportMeetingStatus(Enum):
    create = "已创建"  # 报名未开始
    sign_up = "报名中"
    sign_up_finish = "报名结束"
    running = "进行中"
    finish = "已结束"


class EnumCompetitionStatus(Enum):
    """比赛项目进度"""

    sing_up = "报名中"
    prepare = "等待开始"
    heats_roll_call = "预赛检录中"
    heats_running = "预赛中"
    heats_finish = "预赛结束"
    final_roll_call = "决赛检录中"
    final_running = "决赛中"
    all_finish = "比赛结束"


class EnumPeopleGender(Enum):
    male = "男"
    female = "女"
    mix = "混合"


class EnumCheckInFillInMethod(Enum):
    """
    检录表填充方法
    项目名称、比赛阶段将置于表头抬头
    """

    group_order = "比赛批次"
    in_group_order = "比赛批次内顺序/道次"
    organization_name = "参赛人所属组织"
    team_group_name = "参赛人所属参赛组"
    team_name = "参赛人所属代表队"
    people_mane = "参赛人姓名"
    people_gender = "参赛人性别"
    people_cloth_number = "参赛人号码布"
