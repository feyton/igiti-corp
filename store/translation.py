from modeltranslation.translator import TranslationOptions, translator

from .models import SeedPretreatment, SeedProduct, TypesOfSeed


class TypeOfSeedTranslation(TranslationOptions):
    fields = ("overview", "storage_type")


class SeedPreatreatementTranslation(TranslationOptions):
    fields = ("title", "process")


class SeedProductTranslation(TranslationOptions):
    fields = ("short_note",)


translator.register(SeedPretreatment, SeedPreatreatementTranslation)
translator.register(TypesOfSeed, TypeOfSeedTranslation)
translator.register(SeedProduct, SeedProductTranslation)
