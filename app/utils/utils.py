from urlparse import urlparse

class Utils(object):

    def ad_spaces(self):
        ad_spaces = [
            {
                'id': 'leaderboard-728x90',
                'label': 'Leaderboard 728x90',
                'width': 728,
                'height': 90,
            },
            {
                'id': 'full-banner-468x60',
                'label': 'Full Banner 468x60',
                'width': 468,
                'height': 60,
            },
            {
                'id': 'half-page-300x600',
                'label': 'Half-Page Ad 300x600',
                'width': 300,
                'height': 600,
            },
            {
                'id': 'wide-skyscraper-160x160',
                'label': 'Wide Skyscraper 160x160',
                'width': 160,
                'height': 160,
            },
            {
                'id': 'vertical-rectangle-240x400',
                'label': 'Vertical Rectangle 240x400',
                'width': 240,
                'height': 400,
            },
            {
                'id': 'medium-rectangle-300x250',
                'label': 'Medium Rectangle 300x250',
                'width': 300,
                'height': 250,
            }
        ]

        return ad_spaces

    def available_ad_spaces(self, publisher):
        available_ad_spaces = []

        for ad_space in self.ad_spaces():
            if ad_space['id'] in publisher['adSpaces']:
                available_ad_spaces.append(ad_space)

        return available_ad_spaces

    def get_host(self, url):
        parsed_website = urlparse(url)

        # we want test paths to work (e.g. localhost:8000) as well as URLs without http://
        # so plan for eventuality to use path property instead of netloc.
        host = parsed_website.path if parsed_website.netloc == '' else parsed_website.netloc

        # If host is something like: xxx.foo.bar then we just want foo.bar
        if len(host.split('.')) == 3:
            host = host[host.index('.')+1:]

        return host