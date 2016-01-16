class FormUtils(object):

    @staticmethod
    def get_business_types():
        return [
            ('restaurant-cafe','Restaurant / Cafe'),
            ('website','Website'),
        ]

    @staticmethod
    def get_industries():
        return [
            ('education', 'Education'),
            ('hospitality','Hospitality'),
            ('media', 'Media'),
            ('it','IT')
        ]

    @staticmethod
    def get_website_types():
        return [
            ('e-commerce','e-Commerce'),
            ('entertainment','Entertainment'),
            ('news','News')
        ]