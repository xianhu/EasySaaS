# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


# response model
class RespStat(Resp):
    data_stat: Dict[str, Any] = Field({})


@router.get("/stat/file", response_model=RespStat)
def _get_file_stat(start_day: date = Query(..., description="start day of stat"),
                   end_day: date = Query(..., description="end day of stat"),
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """
    get file stat of current_user
    """
    user_id = current_user.id
    filter0 = File.user_id == user_id

    # filter of date
    filter1 = File.start_time >= start_day
    filter2 = File.start_time <= end_day
    filter3 = File.is_trash == False
    filter_list = [filter0, filter1, filter2, filter3]

    # total files and duration of all days
    total_files = session.query(File).filter(filter0, filter3).count()
    total_duration = session.query(func.sum(File.duration)).filter(filter0, filter3).scalar() or 0

    # files and duration of each day
    field_group = func.date(File.start_time)
    field_list = [field_group, func.count(File.id), func.sum(File.duration)]
    group_result = session.query(*field_list).filter(*filter_list).group_by(field_group).all()

    # return stat
    return RespStat(data_stat={
        "total_files": total_files,
        "total_duration": total_duration,
        "group_result": group_result,
    })
