from typing import List, Optional
from pydantic import Field

from backend.model.edit.search_log_em import SearchLogEm
from backend.model.view.search_log_detail_vm import SearchLogDetailVm


class SearchLogVm(SearchLogEm):
    details: Optional[List[SearchLogDetailVm]]

