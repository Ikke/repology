# Copyright (C) 2016-2017 Dmitry Marakasov <amdmi3@amdmi3.ru>
#
# This file is part of repology
#
# repology is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# repology is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with repology.  If not, see <http://www.gnu.org/licenses/>.

import os

from repology.logger import Logger
from repology.parsers import Parser
from repology.parsers.maintainers import extract_maintainers


def SanitizeVersion(version):
    origversion = version

    pos = version.rfind('-')
    if pos != -1:
        version = version[0:pos]

    if version != origversion:
        return version, origversion
    else:
        return version, None


class MSYS2Parser(Parser):
    def iter_parse(self, path, factory):
        for packagedir in os.listdir(path):
            with open(os.path.join(path, packagedir, 'desc'), 'r', encoding='utf-8') as descfile:
                key = None
                value = []

                data = {}

                for line in descfile:
                    line = line.strip()
                    if line.startswith('%') and line.endswith('%'):
                        key = line[1:-1]
                        value = []
                    elif line == '':
                        data[key] = value
                    else:
                        value.append(line)

                if 'BASE' in data and data['NAME'][0] != data['BASE'][0]:
                    factory.log('{} skipped, subpackage'.format(data['NAME'][0]), severity=Logger.WARNING)
                    continue

                pkg = factory.begin()

                pkg.name = data['NAME'][0]
                pkg.version, pkg.origversion = SanitizeVersion(data['VERSION'][0])

                if 'DESC' in data:
                    pkg.comment = data['DESC'][0]

                if 'URL' in data:
                    pkg.homepage = data['URL'][0]

                if 'LICENSE' in data:
                    pkg.licenses = data['LICENSE']

                pkg.maintainers = sum(map(extract_maintainers, data['PACKAGER']), [])

                if 'GROUPS' in data:
                    pkg.category = data['GROUPS'][0]

                yield pkg
