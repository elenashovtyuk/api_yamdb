from django.core.exceptions import ValidationError
from django.utils import timezone


# создаем валидатор для поля year модели Title
def validate_year(year):
    # укажем переменную current_year и присвоим ей значение текущего года
    # используя
    current_year = timezone.now().year
    # проверяем, будет ли соответствовать входящее значение поля year условиям
    # если в поле год указан год больше значения текущего года,
    # то будет сгенерировано исключение ValidationError c выводом
    # соответствующего сообщения
    if year > current_year:
        raise ValidationError(
            f'Произведение создано позже текущего года ({current_year})!')
