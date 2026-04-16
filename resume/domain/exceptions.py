from core.exceptions import ConflictError, NotFoundError, OwnershipError


class ResumeNotFound(NotFoundError):
    def __init__(self, resume_id: object) -> None:
        super().__init__(f"Resume not found: {resume_id}")


class WorkExperienceNotFound(NotFoundError):
    def __init__(self, experience_id: object) -> None:
        super().__init__(f"Work experience not found: {experience_id}")


class EducationNotFound(NotFoundError):
    def __init__(self, education_id: object) -> None:
        super().__init__(f"Education entry not found: {education_id}")


class ProjectNotFound(NotFoundError):
    def __init__(self, project_id: object) -> None:
        super().__init__(f"Project not found: {project_id}")


class NoActiveResume(NotFoundError):
    def __init__(self, user_id: object) -> None:
        super().__init__(f"No active resume found for user: {user_id}")


class ResumeOwnershipError(OwnershipError):
    def __init__(self, resume_id: object) -> None:
        super().__init__(f"Resume {resume_id} does not belong to this user")
