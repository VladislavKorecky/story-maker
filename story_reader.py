import yaml


class StoryManager:
    def __init__(self):
        self.story = None
        self.frame = None
        self.variables = {}

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
        text = self.frame.get("text")

        var_start_index = None
        for ch_index in range(len(text)):
            if text[ch_index] == '{':
                var_start_index = ch_index
            elif text[ch_index] == '}':
                text = text.replace(text[var_start_index:ch_index + 1], str(self.variables.get(text[var_start_index + 1:ch_index])))

        print(text)

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

        # select action
        action = int(input())

        # handle variables
        if "variables" in self.frame:
            var = self.frame.get("variables")
            self.variables[var[action][0]] = var[action][1]

        # set next frame
        self.frame = self.story[self.frame.get("actions")[action]]