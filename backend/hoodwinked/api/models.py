from django.db import models

class GameStatistics(models.Model):
    name = models.CharField(max_length=100)
    agent = models.CharField(max_length=100)
    killer = models.BooleanField(default=False)
    num_turns = models.IntegerField()
    banished = models.BooleanField(default=False)
    actions = models.JSONField()
    votes = models.JSONField()
    killed = models.BooleanField(default=False)
    escaped = models.BooleanField(default=False)
    num_killed = models.IntegerField()
    num_basished = models.IntegerField()
    num_escaped = models.IntegerField()
    witness_during_vote = models.JSONField()
    vote_rate_for_self = models.FloatField()
    vote_rate_for_killer = models.FloatField()
    witness_vote_rate_for_killer = models.FloatField()
    non_witness_vote_rate_for_killer = models.CharField(max_length=100)
    duplicate_search_rate = models.CharField(max_length=100)
    story = models.CharField(max_length=65535)

    def __str__(self):
        return self.name
    
    class Meta:
        app_label = 'hoodwinked'