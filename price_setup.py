import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bn_core.settings')
django.setup()

from bn_app.models import (Region, Service, ServiceInternalCost, ServicePayout,
                           ServicePublicPrice)

source_region: str = ''
target_region: str = ''

def price_setup():
    source_region = _select_region(is_source=True)
    print(f'source region: {source_region}')
    target_region = _select_region(is_target=True)
    print(f'target region: {target_region}')

    if source_region == target_region:
        print('Source region and target region cannot be the same.')
    else:
        print('Gathering services for source region...')


def _select_region(is_source=False, is_target=False):

    regions = Region.objects.all()

    if is_source:
        print('Select source region:')
    elif is_target:
        print('Select target region:')

    for idx, element in enumerate(regions):
        print('{}) {}'.format(idx + 1, element))

    i = input('Enter number: ')

    try:
        if int(i) >= 1 and int(i) <= len(regions):
            return regions[int(i) - 1]
    except:
        pass

    return None

if __name__ == '__main__':
    price_setup()
