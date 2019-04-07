import datetime

from django import forms
from datetime import datetime, timedelta, timezone
from .models import File, Social_network
from django.db.models import Sum
from django.forms import formset_factory
from django.conf import settings
import tweepy


class ContactForm(forms.Form):
    Name = forms.CharField(max_length=50)
    Email = forms.EmailField()
    Message = forms.CharField(widget=forms.Textarea)


class ModularCapsuleForm(forms.Form):
    UNIT_CHOICES=((0,'minutes'),(1,'days'),(2,'months'),(3,'years'))
    title = forms.CharField(max_length=250)
    emails = forms.CharField(max_length=2500, required=False)
    twitter = forms.BooleanField(required=False)
    facebook = forms.BooleanField(required=False)
    private = forms.BooleanField(required=False)
    deadman_switch = forms.BooleanField(required=False)
    deadman_counter=forms.IntegerField(required=False)
    deadman_time_unit=forms.ChoiceField(required=False,choices=UNIT_CHOICES)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.upfiles = kwargs.pop('upfiles', None)
        super(ModularCapsuleForm, self).__init__(*args, **kwargs)

    def clean_twitter(self):
        data = self.cleaned_data['twitter']
        twitteracc = Social_network.objects.filter(social_type='T', user_id=self.user.id).first()
        if data:
            if twitteracc is not None:
                try:
                    consumer_secret = settings.TWITTER_CREDENTIALS['consumer_secret']
                    consumer_key = settings.TWITTER_CREDENTIALS['consumer_key']
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(twitteracc.token, twitteracc.secret)
                    api = tweepy.API(auth)
                    api.me()
                except:
                    print('Twitter error, revoking credentials')
                    twitteracc.delete()
                    raise forms.ValidationError('You have no valid Twitter account')
            else:
                raise forms.ValidationError('You have no valid Twitter account')
        return data


class ModuleForm(forms.Form):
    description = forms.CharField(max_length=250)
    release_date = forms.DateTimeField()
    file = forms.FileField(required=False)

    def clean_release_date(self):
        data = self.cleaned_data['release_date']
        if data <= datetime.now(timezone.utc):
            raise forms.ValidationError('The release date must be in the future')
        return data


ModulesFormSet = formset_factory(ModuleForm, extra=1)


class NewFreeCapsuleForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    release_date = forms.DateTimeField()
    emails = forms.CharField(max_length=2500, required=False)
    twitter = forms.BooleanField(required=False)
    facebook = forms.BooleanField(required=False)
    files = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.upfiles = kwargs.pop('upfiles', None)
        super(NewFreeCapsuleForm, self).__init__(*args, **kwargs)

    def clean_release_date(self):
        data = self.cleaned_data['release_date']
        if data <= datetime.now(timezone.utc):
            raise forms.ValidationError('The release date must be in the future')
        yearafter = datetime.now(timezone.utc) + timedelta(days=365)
        if data > yearafter:
            raise forms.ValidationError('The release date must be within 1 year from now')
        return data

    def clean_twitter(self):
        data = self.cleaned_data['twitter']
        twitteracc = Social_network.objects.filter(social_type='T', user_id=self.user.id).first()
        if data:
            if twitteracc is not None:
                try:
                    consumer_secret = settings.TWITTER_CREDENTIALS['consumer_secret']
                    consumer_key = settings.TWITTER_CREDENTIALS['consumer_key']
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(twitteracc.token, twitteracc.secret)
                    api = tweepy.API(auth)
                    api.me()
                except:
                    print('Twitter error, revoking credentials')
                    twitteracc.delete()
                    raise forms.ValidationError('You have no valid Twitter account')
            else:
                raise forms.ValidationError('You have no valid Twitter account')
        return data

    def clean_files(self):
        data = self.upfiles
        files = File.objects.filter(module__capsule__capsule_type='F', module__capsule__creator_id=self.user.id).\
            aggregate(totalsum=Sum('size'))
        totalsum = 0.0
        if files['totalsum'] is not None:
            totalsum = float(files['totalsum'])
        if data is not None and data != []:
            for file in data:
                totalsum += (file.size / 1000000)
            if totalsum > 20.0:
                raise forms.ValidationError('You cannot store more than 20 MB using free capsules')
        return data


class EditFreeCapsuleForm(forms.Form):
    title = forms.CharField(max_length=250)
    description = forms.CharField(max_length=250)
    release_date = forms.DateTimeField()
    emails = forms.CharField(max_length=2500, required=False)
    twitter = forms.BooleanField(required=False)
    facebook = forms.BooleanField(required=False)
    files = forms.FileField(required=False)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.upfiles = kwargs.pop('upfiles', None)
        super(EditFreeCapsuleForm, self).__init__(*args, **kwargs)

    def clean_release_date(self):
        data = self.cleaned_data['release_date']
        if data <= datetime.now(timezone.utc):
            raise forms.ValidationError('The release date must be in the future')
        yearafter = datetime.now(timezone.utc) + timedelta(days=365)
        if data > yearafter:
            raise forms.ValidationError('The release date must be within 1 year from now')
        return data

    def clean_twitter(self):
        data = self.cleaned_data['twitter']
        twitteracc = Social_network.objects.filter(social_type='T', user_id=self.user.id).first()
        if data:
            if twitteracc is not None:
                try:
                    consumer_secret = settings.TWITTER_CREDENTIALS['consumer_secret']
                    consumer_key = settings.TWITTER_CREDENTIALS['consumer_key']
                    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
                    auth.set_access_token(twitteracc.token, twitteracc.secret)
                    api = tweepy.API(auth)
                    api.me()
                except:
                    print('Twitter error, revoking credentials')
                    twitteracc.delete()
                    raise forms.ValidationError('You have no valid Twitter account')
            else:
                raise forms.ValidationError('You have no valid Twitter account')
        return data

    def clean_files(self):
        data = self.upfiles
        files = File.objects.filter(module__capsule__capsule_type='F', module__capsule__creator_id=self.user.id).\
            aggregate(totalsum=Sum('size'))
        totalsum = 0.0
        if files['totalsum'] is not None:
            totalsum = float(files['totalsum'])
        if data is not None and data != []:
            for file in data:
                totalsum += (file.size / 1000000)
            if totalsum > 20.0:
                raise forms.ValidationError('You cannot store more than 20 MB using free capsules')
        return data
