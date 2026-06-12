from django.db import models


class RollStatus(models.TextChoices):
    CREATED = "CREATED", "Добавлен"
    REGRINDING = "REGRINDING", "Переточка"
    ON_BEARING = "ON_BEARING", "В подшипниках"
    ON_PILLOW = "ON_PILLOW", "В подушках"
    ASSEMBLED = "ASSEMBLED", "Собран"
    ON_STAND = "ON_STAND", "В клети"
    ON_MILL = "ON_MILL", "На стане"
    ON_COMPLETED = "ON_COMPLETED", "Отработан"
    SCRAPPED = "SCRAPPED", "Списан"


class Roll(models.Model):
    number = models.CharField(max_length=50, unique=True)

    set_number = models.PositiveIntegerField()
    stand_number = models.PositiveIntegerField()
    profile = models.PositiveIntegerField()

    initial_diameter = models.DecimalField(max_digits=8, decimal_places=2)
    current_diameter = models.DecimalField(max_digits=8, decimal_places=2)

    current_status = models.CharField(
        max_length=30,
        choices=RollStatus.choices,
        default=RollStatus.CREATED
    )
    updated_at = models.DateTimeField(auto_now=True)

    # Ответственный
    employee = models.TextField(
        blank=True,
        verbose_name="Ответственный"
    )

    def __str__(self):
        return (
            f"№{self.number} | "
            f"Клеть {self.stand_number} | "
            f"Профиль {self.profile} | "
            f"Ø{self.current_diameter}"
        )


class RollHistory(models.Model):
    # Вал, к которому относится операция
    roll = models.ForeignKey(
        "Roll",
        on_delete=models.CASCADE,
        related_name="history",
        verbose_name="Вал"
    )

    # Дата выполнения операции
    operation_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата операции"
    )

    # Новый статус после операции
    status = models.CharField(
        max_length=30,
        choices=RollStatus.choices,
        verbose_name="Статус"
    )

    # Диаметр до операции
    old_diameter = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Старый диаметр"
    )

    # Диаметр после операции
    new_diameter = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Новый диаметр"
    )

    # Комментарий оператора
    comment = models.TextField(
        blank=True,
        verbose_name="Комментарий"
    )

    # Ответственный
    employee = models.TextField(
        blank=True,
        verbose_name="Ответственный"
    )

    class Meta:
        verbose_name = "История вала"
        verbose_name_plural = "История валов"
        ordering = ["-operation_date"]

    def __str__(self):
        return (
            f"{self.roll.number} | "
            f"{self.get_status_display()} | "
            f"{self.operation_date:%d.%m.%Y %H:%M}"
        )

    def save(self, *args, **kwargs):
        """
        После сохранения записи истории
        обновляем текущее состояние вала.
        """

        super().save(*args, **kwargs)

        roll = self.roll

        # Обновляем статус
        roll.current_status = self.status

        # Обновляем Ответственного за последнюю операцию
        roll.employee = self.employee

        # Если указан новый диаметр,
        # обновляем текущий диаметр вала
        if self.new_diameter is not None:
            roll.current_diameter = self.new_diameter

        # updated_at обновится автоматически
        roll.save()
