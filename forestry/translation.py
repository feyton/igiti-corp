from modeltranslation.translator import TranslationOptions, translator

from .models import Author, BlogPost, Category


class PostTranslationOptions(TranslationOptions):
    fields = ("title", "description", "text", "summary")


class AuthorTranslation(TranslationOptions):
    fields = ("bio",)


class CategoryTranslation(TranslationOptions):
    fields = ("description",)


translator.register(BlogPost, PostTranslationOptions)
translator.register(Author, AuthorTranslation)
translator.register(Category, CategoryTranslation)
