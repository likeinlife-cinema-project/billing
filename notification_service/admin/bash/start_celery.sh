#!/bin/bash
celery -A notifications worker -B --loglevel=DEBUG