from django import forms
from .models import EventRegistration


class EventRegistrationForm(forms.ModelForm):
    class Meta:
        model = EventRegistration
        fields = [
            'first_name', 'last_name', 'email', 'organization', 'job_title',
            'country', 'phone_number', 'sessions', 'attend_all_days',
            'goals_expectations', 'need_accommodation', 'need_transportation',
            'roommate_preference', 'arrival_date', 'departure_date',
            'dietary_restrictions', 'medical_conditions',
            'emergency_contact_name', 'emergency_contact_relationship',
            'emergency_contact_phone', 'how_heard_about_event',
            'interested_in_volunteering', 'event', 'user'
        ]
        widgets = {
            'sessions': forms.CheckboxSelectMultiple(choices=[
                ('spa', 'Session A: Spa'),
                ('volleyball', 'Session B: Volleyball Tournament'),
                ('prayer', 'Session C: Prayer, Healing & Deliverance'),
            ]),
            'dietary_restrictions': forms.CheckboxSelectMultiple(choices=[
                ('vegetarian', 'Vegetarian'),
                ('vegan', 'Vegan'),
                ('gluten_free', 'Gluten-Free'),
            ]),
            'how_heard_about_event': forms.CheckboxSelectMultiple(choices=[
                ('website', 'Website'),
                ('social_media', 'Social Media'),
                ('referral', 'Referral'),
                ('others', 'Others'),
            ]),
            'attend_all_days': forms.RadioSelect(choices=[
                (True, 'yes'),
                (False, 'No'),
            ]),
            'need_accommodation': forms.RadioSelect(choices=[
                (True, 'yes'),
                (False, 'no'),
            ]),
            'need_transportation': forms.RadioSelect(choices=[
                (True, 'yes'),
                (False, 'no'),
            ]),
            'interested_in_volunteering': forms.RadioSelect(choices=[
                (True, 'yes'),
                (False, 'no'),
            ]),
            'event': forms.HiddenInput(), 
        }