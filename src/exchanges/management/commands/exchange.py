
from django.core.management.base import BaseCommand 

from urllib import request

from xml.etree import ElementTree

from exchanges.models import Exchange


class Command(BaseCommand): 
    help = 'Parse exchange rates from nationalbank.kz'
  
    def handle(self, *args, **kwargs): 
        url = 'https://nationalbank.kz/rss/rates_all.xml'

        response = request.urlopen(url).read()

        tree = ElementTree.fromstring(response)

        rates = []

        for node in tree.findall('channel'):
            for item in node.findall('item'):
                title = item.find('title')
                description = item.find('description')
                if title is not None and description is not None:
                    rates.append(Exchange(
                        currency=title.text.lower(),
                        rate=description.text,
                    ))
        Exchange.objects.all().delete()
        Exchange.objects.bulk_create(rates)
        
        