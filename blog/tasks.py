from bucket import bucket
from celery import shared_task


# TODO: can be asunc?
def all_bucket_objects_task():
    result = bucket.get_objects()
    return result


@shared_task
def delete_object_task(key):
    return bucket.delete_object(key)
    

@shared_task
def download_object_task(key):
    return bucket.download_object(key)
    