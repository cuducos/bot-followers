from django.db.models import CharField


class LowerCaseCharField(CharField):
    def pre_save(self, instance, add):
        value = getattr(instance, self.attname)
        setattr(instance, self.attname, value.lower())
        return super(LowerCaseCharField, self).pre_save(instance, add)

    def to_python(self, value):
        value = super(LowerCaseCharField, self).to_python(value)
        return value.lower()
