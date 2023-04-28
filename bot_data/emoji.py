import enum


class Emoji(str, enum.Enum):
    PLUS = "➕"
    MINUS = "➖"
    INFO = "ℹ"
    CHECK_MARK = "✅"
    CROSS = X = "🚫"
    TOGGLE = SWITCH = "🔘"
    GREEN_CIRCLE = "🟢"
    DOUBLE_LEFT = "⏪"
    LEFT = "⬅"
    DOWN = "⤵"
    RIGHT = "➡"
    DOUBLE_RIGHT = "⏩"

    def __str__(self):
        return self.value
