from random import randint
from bson.objectid import ObjectId

class MongoUtils(object):

    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo

    def _insert_one(self, collection_name, doc):
        result = self.mongo.db[collection_name].insert_one(doc)
        return str(result.inserted_id)

    def _find_one(self, collection_name, id):
        return self.mongo.db[collection_name].find_one({'_id': ObjectId(id)})

    def _find(self, collection_name, query={}):
        cursor = self.mongo.db[collection_name].find(query)
        return list(cursor)

    # USERS
    def insert_one_user(self, doc):
        return self._insert_one('users', doc)

    def find_one_user(self, id):
        return self._find_one('users', id)

    def find_one_user_by_email(self, email):
        return self.mongo.db['users'].find_one({'email': email})

    def find_users(self, query={}):
        return self._find('users', query)

    def update_publisher_available_ad_spaces(self, publisher_id, ad_spaces):
        self.mongo.db['users'].update({'_id': ObjectId(publisher_id)}, {'$set': {'adSpaces': ad_spaces}})


    # CAMPAIGNS
    def insert_one_campaign(self, doc):
        return self._insert_one('campaigns', doc)

    def find_campaigns(self, query={}):
        return self._find(self, 'campaigns', query)

    def insert_asset_url(self, campaign_id, asset_id, url):
        #campaign = self.find({'_id': ObjectId(campaign_id)})

        self.mongo.db.campaigns.update({'_id': ObjectId(campaign_id)}, {'$set': {'assets.%s' % asset_id: url}})

    def get_ongoing_campaign(self):
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


    # IMPRESSION RATE
    def _increment_impression(self, campaign_id):
        self.mongo.db.campaigns.update({'_id': ObjectId(campaign_id)}, {'$inc': {'impressions.count': 1}})

    def update_impression_rate(self, pid, rate):
        self.mongo.db['users'].update({'_id': ObjectId(pid)}, {'$set': {'impressionRate': rate}})

