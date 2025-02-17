# Copyright (c) 2022 SUSE Linux LLC.  All rights reserved.
#
# This file is part of suse-migration-services.
#
# suse-migration-services is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# suse-migration-services is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with suse-migration-services. If not, see <http://www.gnu.org/licenses/>
#
"""Run various pre-checks"""
import argparse
import logging

from suse_migration_services.defaults import Defaults
from suse_migration_services.logger import Logger

import suse_migration_services.prechecks.repos as check_repos  # type: ignore
import suse_migration_services.prechecks.fs as check_fs  # type: ignore
import suse_migration_services.prechecks.kernels as check_multi_kernels  # type: ignore


def main():
    """
    DistMigration pre checks before migration starts

    Checks whether
      - repositories' locations are not remote
      - filesystems in fstab are using LUKS encryption
      - Multiple kernels are installed on the system and multiversion.kernels
        in /etc/zypp/zypp.conf is not set to 'running, latest'
    """
    Logger.setup(system_root=False)
    log = logging.getLogger(Defaults.get_migration_log_name())
    log.info('Running pre migration checks')

    cli_parser = argparse.ArgumentParser(
        prog='suse-migration-pre-checks',
        description='Check for existing conditions that will cause a migration to fail'
    )

    cli_parser.add_argument(
        '-f',
        '--fix',
        action='store_true',
        help="Remove additional kernels and set 'multiversion.kernels = running,latest'"
    )
    cli_parser.add_argument(
        '-t',
        '--target',
        action='store_true',
        help="Specify if the kernel prechecks are run using chroot on the mounted "
             "target filesystem. This is used when the prechecks are launched as a "
             "systemd processes during the migration"
    )
    args = cli_parser.parse_args()

    check_repos.remote_repos()
    check_fs.encryption()
    check_multi_kernels.multiversion_and_multiple_kernels(args.fix, args.target)
