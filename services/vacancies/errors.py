class VacancyNotFound(Exception):
    def __str__(self):
        return "Vacancy not found"


class ImpossibleRange(Exception):

    def __str__(self):
        return "First argument cannot be higher than second"
