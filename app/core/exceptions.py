from fastapi import HTTPException, status

EmailIsBusyException = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Данная почта занята"
)

EmailWithNoUser = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Не существует пользователя с данной почтой",
)

IncorrectPassword = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Ошибка в электронной почте или пароле",
)

UserIsNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Пользователя не существует",
)

AnswerIsNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Ответ не найден"
)

ProjectIsNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND, detail="Проект не найден"
)

EmployerIsNotFound = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Профиль работодателя не найден",
)

CandidateIsNotExist = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Candidate profile not found",
)

AnswerIsAlreadyExist = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Вы уже отправили ответ на этот проект.",
)

CandidateIsAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Профиль уже создан"
)

EmployereIsAlreadyExist = HTTPException(
    status_code=status.HTTP_409_CONFLICT, detail="Профиль уже создан"
)


NotAllowedToAddReview = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not allowed to review this answer",
)

UnknownRole = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Unknown role"
)

InvalidRole = HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid profile role"
)

TokenExpired = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Token has expired",
)

InvalidToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token",
)

NotAuthenticated = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Not authenticated",
)

InvalidOrExpiredRefreshToken = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Refresh token invalid or expired",
)

InvalidTokenMissingSub = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid token: missing sub",
)

UserRoleNotAdmin = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User role is not admin",
)

UserRoleNotEmployer = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User role is not employer",
)

UserRoleNotCandidate = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User role is not candidate",
)
