# File for the queue system that the music bot use

# Currently no imports

# A queue system for the music bot
class musicQueue():
    def __init__(self):
        self.queue_list = []

    # Queues in a list
    def queue(self, data):
        self.queue_list.append(youtubeVidMeta(data))

    # Dequeues the first item in list
    def dequeue(self):
        self.queue_list.pop(0)

    # Returns a copy of the list
    def dump(self):
        return [vid_meta for vid_meta in self.queue_list]
    
    # Check if list is empty
    def empty(self):
        return len(self.queue_list) == 0

    # Remove all item in list
    def clean(self):
        self.queue_list.clear()

    # Returns the first item in list
    def first(self):
        return self.queue_list[0]

    # Returns the last item in list
    def last(self):
        return self.queue_list[-1]

    # Returns the song data in the specified index
    def get_at_index(self, index: int):
        return self.queue_list[index]

    # Remove a song's data in the specified index
    def remove_at_index(self, index: int):
        self.queue_list.pop(index)

    def get_len(self):
        return len(self.queue_list)

# A class representing a youtube video
# Contains metadata such as title, url, etc...
class youtubeVidMeta():
    def __init__(self, data):
        self.url = data['formats'][0]['url']
        self.duration = data['duration']
        self.title = data['title']
        self.vid_id = data['id']
        self.channel = data['channel']
        self.thumbnail = data['thumbnail']

    # Display the duration in mm:ss format
    def get_time(self):
        m, s = divmod(self.duration, 60)
        return "{:02d}:{:02d}".format(m, s)

    # Returns the original video link
    def get_vid_url(self):
        return f"https://www.youtube.com/watch?v={self.vid_id}"

    def get_embedded_title(self):
        return f"[{self.title}]({self.get_vid_url()})"

    # Prints data, for debugging
    def printData(self):
        print(f"Title: {self.title}")
        print(f"Duration: {self.duration}")
        print(f"Url: {self.url}")