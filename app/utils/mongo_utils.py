from random import randint
from bson.objectid import ObjectId

class MongoUtils(object):

    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo

    def save(self, doc):
        self.mongo.db.campaigns.save(doc)

    def get(self):
        # Get list of eligible ad campaigns to return
        # TODO: add date filter
        cursor = self.mongo.db.campaigns.find({ "$where": "this.impressions.count != this.impressions.goal" } )
        campaigns = list(cursor)

        # Select a random campaign from the list
        campaign = campaigns[randint(0,len(campaigns)-1)]

        # Update impression count for the selected campaign.
        self._increment_impression(campaign['_id'])

        # Remove ID
        campaign.pop("_id", None)

        return campaign

    def all(self):
        return self.find()

    def find(self, query={}):
        cursor = self.mongo.db.campaigns.find(query)
        return list(cursor)

    def _increment_impression(self, campaign_id):
        self.mongo.db.campaigns.update({'_id': ObjectId(campaign_id)}, {'$inc': {'impressions.count': 1}})
