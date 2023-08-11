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
    filter0 = and_(File.user_id == user_id, File.is_trash == False)

    # field of date
    field_date = func.date(File.start_time)

    # files, duration and days of all days
    total_files = session.query(File).filter(filter0).count()
    total_duration = session.query(func.sum(File.duration)).filter(filter0).scalar() or 0
    total_days = session.query(func.count(distinct(field_date))).filter(filter0).scalar() or 0

    # filter of date range
    filter1 = File.start_time >= start_day
    filter2 = File.start_time <= end_day
    filter_list = [filter0, filter1, filter2]

    # files and duration of each day
    field_list = [field_date, func.count(File.id), func.sum(File.duration)]
    group_result = session.query(*field_list).filter(*filter_list).group_by(field_date).all()

    # return file stat
    return RespStat(data_stat={
        "total_days": total_days,
        "total_files": total_files,
        "total_duration": total_duration,
        "group_result": group_result,
    })
