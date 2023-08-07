# _*_ coding: utf-8 _*_

"""
user api
"""

from ..base import *
from ..utils import get_current_user

# define router
router = APIRouter()


class RespStat(Resp):
    data_stat: Dict[str, Any] = Field({})


@router.get("/stat", response_model=RespStat)
def _get_user_stat(start_day: date = Query(..., description="start day of stat"),
                   end_day: date = Query(..., description="end day of stat"),
                   current_user: User = Depends(get_current_user),
                   session: Session = Depends(get_session)):
    """
    get stat of current_user
    """
    user_id = current_user.id
    filter0 = File.user_id == user_id

    # filter of date
    filter1 = File.start_time >= start_day
    filter2 = File.start_time <= end_day

    # total files and duration
    total_files = session.query(File).filter(filter0, filter1, filter2).count()
    total_duration = session.query(func.sum(File.duration)).filter(filter0, filter1, filter2).scalar() or 0

    # files and duration of each day
    _group = func.date(File.start_time)
    _columns = [_group, func.count(File.id), func.sum(File.duration)]
    group_result = session.query(*_columns).filter(filter0, filter1, filter2).group_by(_group).all()

    # return stat
    return RespStat(data_stat={
        "total_files": total_files,
        "total_duration": total_duration,
        "group_result": group_result,
    })
