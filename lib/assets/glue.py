import sys

from awsglue.utils import getResolvedOptions
from hello import hello_print
#from world import wolrd_print

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['BUCKET'])

## call library
hello_print()
#wolrd_print()