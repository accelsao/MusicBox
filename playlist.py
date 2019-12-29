import argparse
import os
import pickle


class MusicLists(dict):
    def __init__(self, file=None):
        super(MusicLists, self).__init__()

        self.file = file

        if os.path.exists(file) and os.path.getsize(file) > 0:
            with open(file, 'rb') as f:
                dic = pickle.load(f)
                self.update(dic)


    def addSong(self, tags, url):
        tags.append('songs')
        for l in tags:
            if l not in self:
                self[l] = list()
            if url not in self[l]:
                self[l].append(url)

    def removeSong(self, tags, url):
        if tags is None:
            tags = self.keys()

        for l in tags:
            if url in self[l]:
                self[l].remove(url)
                if len(self[l]) == 0:
                    del self[l]

    def saveSong(self):
      with open(self.file, 'wb') as f:
        pickle.dump(self, f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--mode', type=str, help='set action mode, [add, remove, clear]', required=True)
    parser.add_argument('-t', '--tags', nargs='*', type=str, help='set tags for the song')
    parser.add_argument('-id', '--url_id', type=str, help='youtube url ID', required=True)
    args = parser.parse_args()

    m = MusicLists('playlist.p')

    if args.mode == 'add':
        m.addSong(args.tags, args.url_id)
    elif args.mode == 'remove':
        m.removeSong(args.tags, args.url_id)
    else:
        print('only "add" or "remove" is acceptable mode')

    m.saveSong()

    print('current playlist: {}'.format(m))
