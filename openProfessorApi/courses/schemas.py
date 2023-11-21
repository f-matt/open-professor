from main import ma
from courses.models import Course

class CourseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Course
