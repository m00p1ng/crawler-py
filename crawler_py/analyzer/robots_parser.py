import re

from .. import storage
from ..urls import remove_www_prefix
from ..utils import print_log
from ..database import Database as db


class RobotsParser:
    def __init__(self, hostname, content):
        self.hostname = hostname
        self.content = content
        self.resources = []

    def extract_link(self):
        print_log("Extracting robots.txt")
        lines = self._split_lines()
        for i, line in enumerate(lines):
            if re.match(r'^User-Agent: \*', line, re.IGNORECASE):
                self.resources = self._match_disallow_link(i + 1, lines)
                break
        return self.resources

    def _split_lines(self):
        lines = self.content.split('\n')
        lines = [line.strip() for line in lines]
        return lines

    def _match_disallow_link(self, i, lines):
        resources = []
        while i < len(lines) and not re.match(r'^User-Agent', lines[i], re.IGNORECASE):
            result = re.match(r'^Disallow: (.*)', lines[i])
            if result:
                resources.append(result.group(1))
            i += 1
        return resources

    def save(self, resources=None):
        print_log(f"Adding '{self.hostname}' disallow lists")
        if resources is None:
            resources = self.resources

        for resource in resources:
            data = {
                "hostname": self.hostname,
                "resource": '/' + resource.strip("/"),
            }
            if not db.disallow_links.find_one(data):
                db.disallow_links.insert_one(data)

        if re.search(r'User-Agent', self.content, re.IGNORECASE):
            storage.save(
                f"{remove_www_prefix(self.hostname)}/robots.txt", self.content)

        print_log(f"'{self.hostname}' disallow lists were added")
