#!/usr/bin/env python
from __future__ import print_function

import argparse
import re
import sys
import subprocess


def main(raw_args=sys.argv[1:]):
    parser = argparse.ArgumentParser(
        description='Tag Docker images with a version and push the tags')
    parser.add_argument(
        'image_tag', help='the Docker image to (re-)tag and push')
    parser.add_argument(
        'version', help='the full version to tag the image with')
    parser.add_argument(
        '-d', '--dry-run', action='store_true',
        help="don't execute any Docker commands, just print them")

    args = parser.parse_args(raw_args)
    image_tag, version, dry_run = args.image_tag, args.version, args.dry_run

    image, tag = split_image_tag(image_tag)

    # Generate all the tags
    versioned_tags = generate_versioned_tags(tag, version)
    versioned_image_tags = [':'.join((image, vtag)) for vtag in versioned_tags]

    # Tag the image with all the tags
    for versioned_image_tag in versioned_image_tags:
        cmd('docker', 'tag', image_tag, versioned_image_tag, dry_run=dry_run)

    # Push all the tags
    for versioned_image_tag in versioned_image_tags:
        cmd('docker', 'push', versioned_image_tag, dry_run=dry_run)


def split_image_tag(image_tag):
    """ Split an image tag into its name and tag parts (<name>[:<tag>]). """
    image_tag_parts = image_tag.split(':', 1)
    image = image_tag_parts[0]
    tag = image_tag_parts[1] if len(image_tag_parts) == 2 else None
    return image, tag


def generate_versioned_tags(tag, version):
    """
    Generate tags with version information from the given version. Appends the
    version to the given tag after removing the existing version if present.
    e.g. 'foo', '5.4.1'     => ['5.4.1-foo', '5.4-foo', '5-foo']
         '5.4-foo', '5.4.1' => ['5.4.1-foo', '5.4-foo', '5-foo']
         '2.7-foo', '5.4.1' => ['5.4.1-2.7-foo', '5.4-2.7-foo', '5-2.7-foo']
         '5.4', '5.4.1'     => ['5.4.1', '5.4', '5']
         None, '5.4.1'      => ['5.4.1', '5.4', '5']
    """
    sub_versions = generate_sub_versions(version)
    if tag is None:
        # No existing tag, just tag with all versions
        return sub_versions

    unversioned_tag = get_unversioned_tag(tag, sub_versions)
    if not unversioned_tag:
        # No part of existing tag is not a version, just tag with all versions
        return sub_versions

    return ['-'.join((v, unversioned_tag)) for v in sub_versions]


def generate_sub_versions(version):
    """
    Generate strings of the given version to different degrees of precision.
    e.g. '5.4.1' => ['5.4.1', '5.4', '5']
         '5.5.0-alpha' => ['5.5.0-alpha', '5.5.0', '5.5', '5']
    """
    sub_versions = []
    while version:
        sub_versions.append(version)
        version = re.sub(r'[.-]?\w+$', r'', version)
    return sub_versions


def get_unversioned_tag(tag, sub_versions):
    """
    Trim the sub version from the start of the given tag if one of the given
    sub versions is present.
    """
    for sub_version in sub_versions:
        # Tag either is a version, or is the form <version>-<tag>
        if tag == sub_version:
            return ''
        if tag.startswith(sub_version + '-'):
            return tag[len(sub_version) + 1:]

    return tag


def cmd(*args, **kwargs):
    if kwargs.get('dry_run', False):
        print(*args)
        return
    subprocess.check_call(args)

if __name__ == '__main__':  # pragma: no cover
    main()
