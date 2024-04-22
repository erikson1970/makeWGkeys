#!/usr/bin/python3
import argparse
from zlib import decompress
from base64 import b64decode
from random import randint
from random import seed

try:
    import argcomplete
except ImportError:
    argcomplete = None


def _version():
    return "0.2"


timefmt = "%j:%H:%M:%S.%f "


def create_parser(description):
    p = argparse.ArgumentParser(description=description)
    p.add_argument(
        "-l",
        "--length",
        type=int,
        default=80,
        help="max char length to send [80]",
    )
    p.add_argument(
        "-a",
        "--actors",
        type=int,
        default=3,
        help="max number of actors [5]",
    )
    p.add_argument(
        "-c",
        "--count",
        type=int,
        default=1,
        help="number of sentences to return[1]",
    )
    p.add_argument(
        "-f",
        "--foods",
        type=int,
        default=2,
        help="max number of foods [2]",
    )
    p.add_argument(
        "-v",
        "--verbs",
        type=int,
        default=2,
        help="max number of verbs [2]",
    )
    p.add_argument(
        "-s",
        "--spaces",
        type=str,
        default=" ",
        help="replace spaces with char [ None ]",
    )
    p.add_argument(
        "-d",
        "--seed",
        type=int,
        default=-9999,
        help="Set a seed for random number generation",
    )

    if argcomplete:
        argcomplete.autocomplete(p)
    return p


class DocumentGenerator:
    wordsStore = []
    theSeed = -9999

    def __init__(self):
        self.wordsStore = [
            ii.split(" ")
            for ii in decompress(
                b64decode(
                    """eJw9VMuS3DYMvOsr8Cuz6y07W2PHFVflkBtEYSR6SIIGyXnk69OQ1qk5aFR
                        oNYBGAyc2LfSWMxOnmbtpa8RdaOaC33SaJdGfKd6iA1JcuatRUL3KQnPicJ3F7Amc8caZTjfHV
                        Q5Ms8a0g4Z8YBYA/mgMygRU4aBlYbpYdJgJLxcbsQNnkQv90Lp51tJRjKcL+MtJR5XplOTBZRG
                        jrwdEULNRFfGUYTvylcXkTq8bW9KOnhyXtKI5HevWgYtoCbi+aXnSKUtyNsu8IKDUNIHMuHzUb
                        05MbzdJz4KalhVvYYBnGEAo3Po2jE4zZIrpf8SmtaKqxXjV8tFic6YvbBWPWfiGB+LlSpe4Tqf
                        RevSpxPSkOTZMqMWdY1Vtv9V8YDJvKf4LPfvmJJ5K7o4yhkYvUn5yBs8J7OAZlwt7U12THJCjl
                        pcEdaH2Bb0H7tQyozqwDL7x9GK8JHkiE2YWTO/UN1cVWmlB1Cf1FXp5kQubT2E1HWWha7zHI8M
                        rJ5npR8AcpHdadKXOrSPHdeRfg3fEDZX+HQPshTqEVxTZKspJkpHolfMiaGUPJqnbbgvxeMziY
                        XEjfzYOQhd90CUxRl6QIz0hCyCbRfReXfjXLakcYkIXa50y3MQWi0yfuEQoC8aIjuGdHeJEwKy
                        K+C0u9B3Uu5VQHjReqUF/YAq0i9OnZ4Isf0UXLkUf3x3Loz6bIqEfiTC7n7zRmQFGkeUBBxxOq
                        Vz5ydNbR5d0do/imV1c2M6wekC0Fn+b6TPP5iV/U2PSig0emT6GWIXDNn2RAgf8oyjHF8GoA3R
                        EbcJGcsAeoYoaV1qwBDDMHrUWs6v/jj2n08COPqnCPm6TeYegEa41iUN0hqNLQU9VLQyPwQvwS
                        k0jA5CleTdPMnwOYW+ye6BqFtixYIOnd90w5OWwExqQ6rfGd/rXiCU4oGH4cKNwwSFq14idCc4
                        F1laP1Xgfu2LfGOciwkb41gwCQbv9JDVM4JDuHHGSzqMwQZXiW9H3uPH9oDrr6qcIm7A3Bnd2j
                        c37wlgA7Yy5+LGYziNwoxfDafTz4APnGWuXBHcKQM04ndN3cfnPAq47kEEhbI4PAO5+wfat+g8
                        M6Ats"""
                )
            )
            .decode("utf-8")
            .split("\n")
        ]
        self.wordCnt = len(self.wordsStore) - 1

    def setSeed(self, seedMe):
        self.theSeed = seedMe
        if self.theSeed != -9999:
            seed(self.theSeed)

    def sentence(self, actors=5, actorAnimalOdds=1, verbs=2, foods=2):
        def joinNice(ll, n2plus=", ", n2=" and "):
            """Join a list of words with ',' and/or 'and' depending on number of items in list"""
            return (
                "{}{}{}{}".format(n2plus.join(ll[:-1]), n2plus, n2[1:], ll[-1])
                if len(ll) > 2
                else ("{}{}{}".format(ll[0], n2, ll[1]) if len(ll) > 1 else ll[0])
            )

        # results = "{} the {} {} {}.".format(
        results = "{} {} {}.".format(
            joinNice(
                [
                    self.wordsStore[randint(0, self.wordCnt)][randint(0, 1)]
                    + (
                        " the " + self.wordsStore[randint(0, self.wordCnt)][2]
                        if randint(0, actorAnimalOdds) > 0
                        else ""
                    )
                    for ii in range(randint(1, actors))
                ]
            ),
            joinNice(
                [
                    self.wordsStore[randint(0, self.wordCnt)][3]
                    for _ in range(randint(1, verbs))
                ]
            ),
            joinNice(
                [
                    "a " + self.wordsStore[randint(0, self.wordCnt)][4]
                    for _ in range(randint(1, foods))
                ]
            ),
        )
        return results


def getter(
    count=1,
    maxLen=400,
    maxTries=400,
    actors=5,
    actorAnimalOdds=1,
    verbs=2,
    foods=2,
    mySeed=-9999,
):
    gen = DocumentGenerator()
    gen.setSeed(mySeed)
    while count > 0:
        thisSent = (maxLen + 1) * "x"
        while len(thisSent) > maxLen and maxTries > 0:
            thisSent = gen.sentence(
                actors=actors, actorAnimalOdds=actorAnimalOdds, verbs=verbs, foods=foods
            )
            maxTries -= 1
        count -= 1
        yield thisSent


def _main():
    fmt = "Sentence Generator Sender v{0:s}: "
    description = fmt.format(_version())
    maxLen = 60
    p = create_parser(description)

    args = p.parse_args()

    for i in getter(
        count=args.count,
        maxLen=args.length,
        maxTries=400,
        actors=args.actors,
        actorAnimalOdds=1,
        verbs=args.verbs,
        foods=args.foods,
        mySeed=args.seed,
    ):
        if args.spaces == " ":
            print(i)
        else:
            print(i.replace(" ", args.spaces))


if __name__ == "__main__":
    _main()
