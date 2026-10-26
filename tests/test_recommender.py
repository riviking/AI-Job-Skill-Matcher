from core.recommender import recommend_courses
from utils.data_loader import load_courses


def test_course_recommendations_are_free_and_match_the_requested_skill():
    skill = "Python"
    recommendations = recommend_courses([skill])[skill]
    courses = load_courses()

    assert recommendations
    for recommendation in recommendations:
        matching = courses[
            (courses.title == recommendation["title"])
            & (courses.skill_name.str.casefold() == skill.casefold())
        ]
        assert not matching.empty
        assert matching.is_free.all()
        assert recommendation["url"].startswith("https://")
