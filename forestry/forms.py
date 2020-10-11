from django import forms

from .models import Comment, CommentReply


class CommentForm(forms.ModelForm):
    """Form definition for Comment."""

    class Meta:
        """Meta definition for Commentform."""

        model = Comment
        fields = ('full_name', "email", "message")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs.update({'class': 'form-control'})
        self.fields['email'].widget.attrs.update({'class': 'form-control'})
        self.fields['message'].widget.attrs.update(
            {'class': 'form-control', 'row': '3'})


class UserCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(
            {'class': 'form-control', 'row': '3'})


class CommentReplyForm(forms.ModelForm):
    """Form definition for CommentReply."""

    class Meta:
        """Meta definition for CommentReplyform."""

        model = CommentReply
        fields = ('message',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update({'class': 'form-control'})
