# -*- coding: utf-8 -*-
import math
import os

from django.conf import settings

from boto.s3.connection import S3Connection
from boto.exception import *
from boto.s3.key import Key
import time
import StringIO
import logging
import hashlib

from filechunkio import FileChunkIO

logger = logging.getLogger(__name__)


operator = None


def get_operator():
    global operator
    if not operator:
        operator = ObjectStorage()
    return operator


class ObjectStorage():
    def __init__(self):
        logger.info("connecting to S3...")
        self.conn = S3Connection(
             aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
             aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
             is_secure=settings.AWS_S3_USE_SSL,
             host=settings.AWS_S3_HOST,
             port=settings.AWS_S3_PORT,
             calling_format=settings.AWS_S3_CALLING_FORMAT)
        self.bucket = self._get_bucket(settings.AWS_STORAGE_BUCKET_NAME)
        logger.info("success connected to S3")

    def _get_bucket(self, bucket_name):
        """ Sometimes a handle to a bucket is not established right away so try
        it a few times. Raise error is connection is not established. """
        for i in range(5):
            try:
                bucket = self.conn.get_bucket(bucket_name)
                logger.info("Using cloud object store with bucket '%s'", bucket.name)
                return bucket
            except S3ResponseError:
                try:
                    logger.warn("Bucket not found, creating s3 bucket with handle '%s'", bucket_name)
                    self.conn.create_bucket(bucket_name)
                except S3ResponseError:
                    logger.exception("Could not get bucket '%s', attempt %s/5", bucket_name, i + 1)
                    time.sleep(2)
        # All the attempts have been exhausted and connection was not established,
        # raise error
        raise S3ResponseError

    def download_file(self, key, local_path):
        handler = self.bucket.new_key(key)
        handler.get_contents_to_filename(local_path)

    def key_exists(self, obj_path):
        exists = False
        try:
            # A hackish way of testing if the obj_path is a folder vs a file
            is_dir = obj_path[-1] == '/'
            if is_dir:
                keyresult = self.bucket.get_all_keys(prefix=obj_path)
                if len(keyresult) > 0:
                    exists = True
                else:
                    exists = False
            else:
                key = Key(self.bucket, obj_path)
                exists = key.exists()
        except S3ResponseError:
            logger.exception("Trouble checking existence of S3 key '%s'", obj_path)
            return False
        if obj_path[0] == '/':
            raise Exception
        return exists

    def delete(self, obj_path, entire_dir=False):
        try:
            if entire_dir:
                results = self.bucket.get_all_keys(prefix=obj_path)
                for key in results:
                    logger.info("Deleting key %s", key.name)
                    key.delete()
                return True
            else:
                if self.key_exists(obj_path):
                    key = Key(self.bucket, obj_path)
                    logger.info("Deleting key %s", key.name)
                    key.delete()
                    return True
        except S3ResponseError:
            logger.exception("Could not delete key '%s' from S3", obj_path)
        return False

    def upload_file_obj(self, src_file_obj, obj_path):
        hasher = hashlib.md5()
        try:
            key = self.bucket.new_key(obj_path)
            mp = self.bucket.initiate_multipart_upload(obj_path)
            i = 0
            # s3 multipart upload should be larger than 5MB
            for chunk in src_file_obj.chunks(5 * 2 ** 20):
                size = len(chunk)
                hasher.update(chunk)
                i += 1
                fp = StringIO.StringIO(chunk)
                mp.upload_part_from_file(fp, part_num=i, md5=key.compute_md5(fp, size))

            mp.complete_upload()
            self.bucket.set_acl('public-read', obj_path)
            return hasher.hexdigest()
        except S3ResponseError:
            logger.exception("Could not upload key '%s' to S3", obj_path)
        except Exception, ex:
            logger.exception("Could not read source to key '%s' to S3: %s" % (obj_path, ex))
        return None

    def upload_local_file(self, file_path, obj_path):
        hasher = hashlib.md5()
        try:
            key = self.bucket.new_key(obj_path)
            mp = self.bucket.initiate_multipart_upload(obj_path)
            chunk_size = 5 * 2 ** 20
            file_size = os.stat(file_path).st_size
            # s3 multipart upload should be larger than 5MB
            chunk_count = int(math.ceil(file_size / float(chunk_size)))
            for i in range(chunk_count):
                offset = chunk_size * i
                bytes = min(chunk_size, file_size - offset)
                with FileChunkIO(file_path, 'r', offset=offset, bytes=bytes) as fp:
                    mp.upload_part_from_file(fp, part_num=i + 1)

            mp.complete_upload()
            self.bucket.set_acl('public-read', obj_path)
            return hasher.hexdigest()
        except S3ResponseError:
            logger.exception("Could not upload key '%s' to S3", obj_path)
        except Exception, ex:
            logger.exception("Could not read source to key '%s' to S3: %s" % (obj_path, ex))
        return None


    def size(self, obj_path):
        try:
            key = self.bucket.get_key(obj_path)
            if key:
                return key.size
        except S3ResponseError, ex:
            logger.error("Could not get size of key '%s' from S3: %s" % (obj_path, ex))
        except Exception, ex:
            logger.error("Could not get reference to the key object '%s'; returning -1 for key size: %s" % (obj_path, ex))
        return -1

    def last_modified(self, obj_path):
        try:
            key = self.bucket.get_key(obj_path)
            if key:
                return key.last_modified
        except S3ResponseError, ex:
            logger.error("Could not get last_modified of key '%s' from S3: %s" % (obj_path, ex))
        except Exception, ex:
            logger.error("Could not get reference to the key object '%s'; returning None for key size: %s" % (obj_path, ex))
        return None