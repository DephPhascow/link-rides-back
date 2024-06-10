from modeltranslation.translator import register, TranslationOptions
from main.models import TmpModel

@register(TmpModel)
class TmpModelTranslationOptions(TranslationOptions):
    fields = ('name', 'description', )