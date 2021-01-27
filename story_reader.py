import yaml

class StoryManager:
    def __init__(self):
        self.story = None
        self.frame = None

    def start(self, file_name):
        with open(file_name) as file:
            # load story
            self.story = yaml.load(file, Loader=yaml.FullLoader)

            # load first frame
            self.frame = self.story[0]

            while self.frame is not None:
                self.load_frame()

    def load_frame(self):
        # print text
        print(self.frame.get("text"))

        # check if the frame is end frame
        if len(self.frame.get("options")) == 0:
            self.frame = None
            return

        # check for errors
        if len(self.frame.get("actions")) != len(self.frame.get("options")):
            raise Exception("\"options\" must be equal to \"to\"")

        # display options
        for option_index in range(len(self.frame.get("options"))):
            print(str(option_index) + " " + self.frame.get("options")[option_index])

        # handle actions
        action = int(input())
        self.frame = self.story[self.frame.get("actions")[action]]