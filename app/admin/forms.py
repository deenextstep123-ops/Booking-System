class ServiceSettingsForm:

    def __init__(self, data):
        self.name = data["name"].strip()
        self.duration_minutes = data["duration_minutes"].strip()

        self.errors = []


    def validate_name(self):

        if not self.name:
            self.errors.append("Service name is required")
            return False

        if len(self.name) > 100:
            self.errors.append("Service name cannot be longer than 100 characters")
            return False

        return True


    def validate_duration(self):

        try:
            self.duration_minutes = int(self.duration_minutes)

        except ValueError:
            self.errors.append("Duration must be a whole number")
            return False

        if self.duration_minutes <= 0:
            self.errors.append("Duration must be greater than 0")
            return False

        if self.duration_minutes % 15 != 0:
            self.errors.append("Duration must be in 15 minute increments")
            return False

        return True


    def validate(self):

        self.errors.clear()

        self.validate_name()
        self.validate_duration()

        if not self.errors:
            return True

        return False