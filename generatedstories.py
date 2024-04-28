from random import sample, shuffle
import os


class GeneratedStories:
    """
        Class for poulation of Mad libs stories

        Tests
        >>> s = GeneratedStories()
        Loaded 23 MadLibs stories from 'static/stories.txt'

        >>> s
        <GeneratedStories stories=23>

        >>> len(s.stories)==23
        True

        >>> len(s.quick_select_required_items)==5
        True
    """

    def __init__(self, file_path=os.path.join(os.path.dirname(
            __file__), "static/stories.txt"), sampled_amount=5):
        """Initializes the GeneratedStories Class"""
        self.stories = []
        self.file_path = os.path.join(os.path.dirname(
            __file__), file_path)
        self.load_stories_from_txt(self.file_path)
        self.sampled_amount = sampled_amount
        self.quick_select_stories = self.get_random_stories()
        self.quick_select_required_items = []
        self.required_items()
        for i in self.quick_select_required_items:
            shuffle(i)

    def get_random_stories(self):
        """Sample the current stories list by shuffling and returning a subset"""
        if len(self.stories) == 0:
            return 'Stories List Empty'
        return sample(self.stories, self.sampled_amount)

    def __repr__(self):
        return '<GeneratedStories stories=' + str(len(self.stories)) + '>'

    def required_items(self):
        """Generate a required items list of words based on the story"""
        for i in self.quick_select_stories:
            word_list_stack = []
            word_list_return = []
            for k, j in enumerate(i):
                if j == '{':
                    word_list_stack.append(k)
                    continue
                if j == '}':
                    if i[word_list_stack[-1]:word_list_stack[-1] + 1] != '{':
                        raise ValueError(
                            'Story ID: ' + str(k + 1) +
                            ' Brace closed Index at ' + str(k) +
                            ' Total Story: <begin>(' + i[0:k] + ') <end>(' +
                            i[k + 1:] + ")")
                    word_list_return.append(i[word_list_stack[-1]+1:k])
                    word_list_stack.append(k)
            self.quick_select_required_items.append(word_list_return)

    def load_stories_from_txt(self, file_path):
        """Load stories from a .txt file located in static folder"""
        self.stories.clear()
        with open(self.file_path, 'r') as file:
            for line in [line.rstrip('\n') for line in file.readlines()]:
                self.stories.append(line)
        print(f'Loaded {str(len(self.stories))} MadLibs stories from \'' +
              f"""{self.file_path[len(os.path.dirname(
                  __file__)) + 1:]}'""")
