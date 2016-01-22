from flask import current_app
from random import randint
from bson.objectid import ObjectId
from datetime import datetime

class MongoUtils(object):

    mongo = None

    def __init__(self, mongo):
        self.mongo = mongo

    def _insert_one(self, collection_name, doc):
        result = self.mongo.db[collection_name].insert_one(doc)
        return str(result.inserted_id)

    def _find_one(self, collection_name, id):
        return self.mongo.db[collection_name].find_one({'_id': ObjectId(id)})

    def _update_one(self, collection_name, id, update):
        return self.mongo.db[collection_name].update({'_id': ObjectId(id)}, {'$set': update})

    def _delete_one(self, collection_name, id):
        return self.mongo.db[collection_name].delete_one({'_id': ObjectId(id)})

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

    def get_publisher_published_campaigns(self, publisher_id):
        #TODO: date filter and status: published
        return self.find_campaigns({'publisher.id': publisher_id, 'status': 'published'})

    def get_publisher_stopped_campaigns(self, publisher_id):
        #TODO: date filter and status: stopped
        return self.find_campaigns({'publisher.id': publisher_id, 'status': 'stopped'})

    def get_publisher_draft_campaigns(self, publisher_id):
        #TODO: date filter and status: draft
        return self.find_campaigns({'publisher.id': publisher_id, 'status': 'draft'})

    # CAMPAIGNS
    def insert_one_campaign(self, doc):
        return self._insert_one('campaigns', doc)

    def find_one_campaign(self, id):
        return self._find_one('campaigns', id)

    def delete_one_campaign(self, id):
        return self._delete_one('campaigns', id)

    def update_one_campaign(self, id, update):
        return self._update_one('campaigns', id, update)

    def set_campaign_as_published(self, id):
        self.set_campaign_status(id, 'published')

    def set_campaign_as_stopped(self, id):
        self.set_campaign_status(id, 'stopped')

    def set_campaign_as_draft(self, id):
        self.set_campaign_status(id, 'draft')

    def set_campaign_status(self, id, status):
        self.mongo.db['campaigns'].update({'_id': ObjectId(id)}, {'$set': {'status': status}})

    def find_campaigns(self, query={}):
        return self._find('campaigns', query)

    def insert_asset_url(self, campaign_id, asset_id, url):
        self.mongo.db['campaigns'].update({'_id': ObjectId(campaign_id)}, {'$set': {'assets.%s' % asset_id: url}})

    def remove_asset_url(self, campaign_id, asset_id):
        self.mongo.db['campaigns'].update({'_id': ObjectId(campaign_id)}, { '$unset': { 'assets.%s' % asset_id: ""}})

    def get_ongoing_campaign_asset_url_for_publisher(self, host):
        # Get list of eligible ad campaigns to return
        cursor = self.mongo.db['campaigns'].find({
            'publisher.host': host,
            'status': 'published',
            'start': {
                '$lte': datetime.now()
            },
            'end': {
                '$gte': datetime.now()
            },
            '$where': 'this.impressions.count < this.impressions.goal'
        })
        campaigns = list(cursor)

        # There are no on-going campaigns
        if len(campaigns) == 0:
            return None
        else:

            # Select a random campaign from the list
            campaign = campaigns[randint(0, len(campaigns)-1)]

            # Update impression count for the selected campaign.
            self._increment_impression(campaign['_id'])

            # Remove ID
            campaign.pop("_id", None)

            return campaign


    # IMPRESSION RATE
    def _increment_impression(self, campaign_id):
        self.mongo.db['campaigns'].update({'_id': ObjectId(campaign_id)}, {'$inc': {'impressions.count': 1}})

    def update_impression_rate(self, pid, rate):
        self.mongo.db['users'].update({'_id': ObjectId(pid)}, {'$set': {'impressionRate': rate}})

