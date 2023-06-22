from celery import shared_task
from .models import Link, Collected_data
from .Amazon import Amazon

def collect_data(data, server):
    
    # get the raw data
    soup = server.send_request(data.product_link)

    # extract the data in the form of a dictionary
    saving_data = server.product_details(soup)

    process = Collected_data(
            name = data,
            title = saving_data['title'],
            rating = saving_data['rating'],
            review = saving_data['review'],
            isAvaliable = saving_data['isAvaliable'],
            price = saving_data['price'],
            mrp = saving_data['mrp'],
            seller = saving_data['seller'],
            ASIN = saving_data['ASIN'],
            First_date = saving_data['First_date'],

        )
    
    process.save()


@shared_task
def data_collection_trigger() -> None:
    # get all the links from which we need to collect data
    all_links = Link.objects.all().filter(collection=True)

    # starting the session
    server = Amazon()

    # iterate these links
    for data in all_links:
        collect_data(data, server)

    # closing the session
    server.close_session()


# celery -A my_site worker --pool=solo -l info
# celery -A my_site beat --loglevel=info

