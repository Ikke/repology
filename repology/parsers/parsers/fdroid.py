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

import xml.etree.ElementTree

from repology.package import PackageFlags
from repology.parsers import Parser


class FDroidParser(Parser):
    def iter_parse(self, path, factory):
        root = xml.etree.ElementTree.parse(path)

        for application in root.findall('application'):
            name = application.find('name').text
            license_ = application.find('license').text
            category = application.find('category').text
            www = application.find('web').text
            appid = application.find('id').text

            upstream_version_code = int(application.find('marketvercode').text)
            for package in application.findall('package'):
                version_code = int(package.find('versioncode').text)
                version = package.find('version').text

                if name and version:
                    pkg = factory.begin()

                    pkg.name = name.strip()
                    pkg.version = version
                    pkg.licenses = [license_]
                    pkg.category = category
                    pkg.homepage = www if www else None
                    pkg.extrafields = {'id': appid}
                    pkg.flags = PackageFlags.devel if version_code > upstream_version_code else 0

                    yield pkg
