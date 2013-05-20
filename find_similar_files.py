#!/usr/bin/python

import sys
import collections
import hashlib

DEFAULT_THRESHOLD = 0.8

test_file_list = ['test1.html', 'test2.html', 'test3.html']

def find_similar_files(files, threshold):
    file_indexes = [FileIndex(f) for f in files]
    while file_indexes:
        current = file_indexes.pop()
        scores = [(current.compare(fi), fi) for fi in file_indexes]
        scores = filter(lambda x: x[0] > threshold, scores)
        scores.sort(reverse=True)
        if scores:
            print '\n'
            print '=' * 79
            print current.filename
            for score, scoring_index in scores:
                print score, scoring_index.filename

class FileIndex(object):
    def __init__(self, filename):
        self.filename = filename
        self.index = collections.defaultdict(lambda: 0)
        self.total_lines = 0
        self.build()

    def build(self):
        lines = self.read_and_clean_file()
        self.total_lines = len(lines)
        for l in lines:
            line_hash = self.hash_line(l)
            self.index[line_hash] += 1

    def read_and_clean_file(self):
        f = open(self.filename)
        lines = [l.strip() for l in f.readlines()]
        lines = filter(None, lines)
        return lines

    def hash_line(self, line):
        return hashlib.new('md5', line).hexdigest()[:20]

    def compare(self, comparison_index):
        matching_lines = 0
        total_lines = self.total_lines + comparison_index.total_lines
        if not total_lines:
            return 0
        for h,c in self.index.items():
            matching_lines += min(c, comparison_index.index.get(h, 0))
        return float(matching_lines) * 2 / total_lines


def main():
    print sys.argv[1]
    try:
        file_list_name = sys.argv[1]
        f = open(file_list_name)
        files = [fn.strip() for fn in f.readlines()]
        files = filter(None, files)
        f.close()
    except IndexError:
        files = test_file_list
    find_similar_files(files, DEFAULT_THRESHOLD)

if __name__ == '__main__':
    main()
