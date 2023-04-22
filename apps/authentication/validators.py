"""
Copyright (c) 2023 - EvalGenie, LLC
"""

from django.core.exceptions import ValidationError
import re

class MixedCaseAndSpecialCharactersValidator:
    pattern = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).*$')

    def validate(self, password, user=None):
        if not self.pattern.match(password):
            raise ValidationError(
                "Password must contain at least one uppercase letter, "
                "one lowercase letter, one digit, and one special character.",
                code="password_complexity",
            )

    def get_help_text(self):
        return (
            "Your password must contain at least one uppercase letter, "
            "one lowercase letter, one digit, and one special character."
        )
