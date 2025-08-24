from flask import Blueprint

teacher_bp = Blueprint('teacher', __name__, url_prefix='/api/teacher')

from . import exam_class
from . import exam_results
from . import performance
from . import profile
from . import score_create
from . import score_update
from . import scores
from . import students
