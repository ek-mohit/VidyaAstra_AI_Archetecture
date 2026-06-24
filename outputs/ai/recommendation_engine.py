"""
recommendation_engine.py

Personalized recommendation engine

Uses:

1. Quiz Scores
2. Lecture Completion
3. Flashcard Performance
4. Watch Time
5. Student Activity

Outputs:

- Weak Topics
- Suggested Lectures
- Suggested Quizzes
- Revision Plan
"""

import json
from collections import defaultdict


class RecommendationEngine:

    def __init__(self):
        pass

    def load_student_data(
        self,
        student_file
    ):

        with open(
            student_file,
            "r",
            encoding="utf-8"
        ) as f:

            return json.load(f)

    def identify_weak_topics(
        self,
        student_data
    ):

        weak_topics = []

        quiz_scores = student_data.get(
            "quiz_scores",
            []
        )

        for item in quiz_scores:

            if item["score"] < 60:

                weak_topics.append(
                    item["topic"]
                )

        return weak_topics

    def identify_strong_topics(
        self,
        student_data
    ):

        strong_topics = []

        quiz_scores = student_data.get(
            "quiz_scores",
            []
        )

        for item in quiz_scores:

            if item["score"] >= 80:

                strong_topics.append(
                    item["topic"]
                )

        return strong_topics

    def recommend_lectures(
        self,
        weak_topics,
        lectures
    ):

        recommendations = []

        for lecture in lectures:

            if lecture["topic"] in weak_topics:

                recommendations.append(
                    lecture
                )

        return recommendations

    def recommend_quizzes(
        self,
        weak_topics,
        quizzes
    ):

        result = []

        for quiz in quizzes:

            if quiz["topic"] in weak_topics:

                result.append(
                    quiz
                )

        return result

    def generate_revision_plan(
        self,
        weak_topics
    ):

        plan = []

        day = 1

        for topic in weak_topics:

            plan.append(
                {
                    "day": day,
                    "topic": topic,
                    "task":
                        "Revise Notes + Quiz"
                }
            )

            day += 1

        return plan

    def calculate_overall_progress(
        self,
        student_data
    ):

        completed = (
            student_data.get(
                "completed_lectures",
                0
            )
        )

        total = (
            student_data.get(
                "total_lectures",
                1
            )
        )

        progress = (
            completed / total
        ) * 100

        return round(
            progress,
            2
        )

    def build_recommendation_report(
        self,
        student_data,
        lectures,
        quizzes
    ):

        weak_topics = (
            self.identify_weak_topics(
                student_data
            )
        )

        strong_topics = (
            self.identify_strong_topics(
                student_data
            )
        )

        recommended_lectures = (
            self.recommend_lectures(
                weak_topics,
                lectures
            )
        )

        recommended_quizzes = (
            self.recommend_quizzes(
                weak_topics,
                quizzes
            )
        )

        revision_plan = (
            self.generate_revision_plan(
                weak_topics
            )
        )

        progress = (
            self.calculate_overall_progress(
                student_data
            )
        )

        return {
            "progress": progress,
            "weak_topics": weak_topics,
            "strong_topics": strong_topics,
            "recommended_lectures":
                recommended_lectures,
            "recommended_quizzes":
                recommended_quizzes,
            "revision_plan":
                revision_plan
        }


if __name__ == "__main__":

    engine = RecommendationEngine()

    student_data = {
        "completed_lectures": 8,
        "total_lectures": 12,

        "quiz_scores": [
            {
                "topic": "1NF",
                "score": 40
            },
            {
                "topic": "2NF",
                "score": 55
            },
            {
                "topic": "3NF",
                "score": 90
            }
        ]
    }

    lectures = [
        {
            "id": 1,
            "topic": "1NF"
        },
        {
            "id": 2,
            "topic": "2NF"
        },
        {
            "id": 3,
            "topic": "3NF"
        }
    ]

    quizzes = [
        {
            "id": 101,
            "topic": "1NF"
        },
        {
            "id": 102,
            "topic": "2NF"
        }
    ]

    report = (
        engine.build_recommendation_report(
            student_data,
            lectures,
            quizzes
        )
    )

    print(
        json.dumps(
            report,
            indent=4
        )
    )