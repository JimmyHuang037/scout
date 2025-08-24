from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/api/admin')

from . import students
from . import teachers
from . import responses
from . import student_detail
from . import student_fetch
from . import student_ops_view
from . import student_update
from . import student_view
from . import students_ops
from . import teacher_create
from . import teacher_detail
from . import teacher_update

__all__ = ['admin_bp']