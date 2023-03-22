from django.db import models

class GameStatistics(models.Model):
    name = models.CharField(max_length=100)
    agent = models.CharField(max_length=100, blank=True, null=True)
    killer = models.BooleanField(default=False)
    num_turns = models.IntegerField(blank=True, null=True)
    banished = models.BooleanField(default=False)
    actions = models.JSONField(blank=True, null=True)
    votes = models.JSONField(blank=True, null=True)
    killed = models.BooleanField(default=False)
    escaped = models.BooleanField(default=False)
    num_killed = models.IntegerField(blank=True, null=True)
    num_basished = models.IntegerField(blank=True, null=True)
    num_escaped = models.IntegerField(blank=True, null=True)
    witness_during_vote = models.JSONField(blank=True, null=True)
    vote_rate_for_self = models.FloatField(blank=True, null=True)
    vote_rate_for_killer = models.FloatField(blank=True, null=True)
    witness_vote_rate_for_killer = models.FloatField(blank=True, null=True)
    non_witness_vote_rate_for_killer = models.CharField(max_length=100, blank=True, null=True)
    duplicate_search_rate = models.CharField(max_length=100, blank=True, null=True)
    story = models.CharField(max_length=65535, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'hoodwinked'