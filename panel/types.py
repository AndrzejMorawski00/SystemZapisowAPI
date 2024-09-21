from typing import TypedDict, List


class CourseType(TypedDict):
    id: int
    name: str
    shortcut: str


class CourseTag(TypedDict):
    id: int
    name: str
    shortcut: str


class CourseEffect(TypedDict):
    id: int
    name: str


class CourseDict(TypedDict):
    id: int
    name: str
    recommended_for_first_year: bool
    url: str
    type: CourseType
    ects: int
    tags: List[CourseTag]
    effects: List[CourseEffect]


class CourseDataDict(TypedDict):
    semester: int
    courses: List[CourseDict]
