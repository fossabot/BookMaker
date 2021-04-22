# coding=utf8
# the above tag defines encoding for this document and is for Python 2.x compatibility

import re

regex = r" {0,3}\|(.+)\n *\|((:?-+([0-9]*)-+:?\|)*)\n((?: *\|.*(?:\n|$))*)\n*"

test_str = ("|Method|Result|\n"
            "|:-28-|:--39--|\n"
            "|d.clear()|Removes all items from dict d|\n"
            "|d.copy()|Returns a shallow copy of dict d|\n"
            "|d.fromkeys(s, v)|Returns a dict whose keys are the items in sequence s and whose values are all None, or default to v if v is given|\n")

matches = re.finditer(regex, test_str, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):

    print("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum=matchNum, start=match.start(),
                                                                        end=match.end(), match=match.group()))

    for groupNum in range(0, len(match.groups())):
        groupNum = groupNum + 1

        print("Group {groupNum} found at {start}-{end}: {group}".format(groupNum=groupNum, start=match.start(groupNum),
                                                                        end=match.end(groupNum),
                                                                        group=match.group(groupNum)))

# Note: for Python 2.7 compatibility, use ur"" to prefix the regex and u"" to prefix the test string and substitution.
