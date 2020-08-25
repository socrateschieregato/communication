from enum import Enum, unique


class EnumDatabaseChoicesMixin(Enum):
    @classmethod
    def get_database_choices(cls):
        return tuple((item.value, item.value) for item in cls)

    @classmethod
    def get_database_max_length(cls):
        return max(len(item.value) for item in cls)


@unique
class CommunicationEnum(EnumDatabaseChoicesMixin):
    EMAIL = 'email'
    SMS = 'sms'
    PUSH = 'push'
    WHATSAPP = 'whatsapp'


@unique
class ScheduleStatusEnum(EnumDatabaseChoicesMixin):
    SENT = 'sent'
    SCHEDULED = 'scheduled'
    CANCELLED = 'cancelled'
