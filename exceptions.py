class EndGameError(IndexError):
    """Класс, опрередляющий ошибку, выходящую в конец игры."""

    def __str__(self):
        """Метод, описывающий ошибку."""
        return 'Яблоко больше некуда поставить. Вы выиграли!'
