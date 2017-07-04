#!/usr/bin/env python
import os
import sys

def local_exists():
    for p in sys.path:
        lc = os.path.join(p, 'local_config.py')
        if os.path.exists(lc):
            print("Found local_config.py here:{}".format(lc))
            return True

    return False



if __name__ == "__main__":

    savedir = os.getcwd()
    rundir = os.path.dirname(__file__)
    if rundir:
        print("Running from {}".format(rundir))
        os.chdir(rundir)

    if local_exists():
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "local_config")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "datasheet_ai.settings.dev")


    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        # The above import may fail for some other reason. Ensure that the
        # issue is really that Django is missing to avoid masking other
        # exceptions on Python 2.
        try:
            import django
        except ImportError:
            raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
            )
        raise
    execute_from_command_line(sys.argv)
