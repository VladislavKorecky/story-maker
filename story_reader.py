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
            self.set_frame(0)

            while self.frame is not None:
                self.load_frame()

    def load_frame(self):
        # check for "if" key
        if "if" in self.frame:
            if self.frame.get("if"):
                statements = self.frame.get("statements")
                for statement in statements:
                    if self.variables.get(statement[0]) == statement[1]:
                        self.set_frame(statement[2])
                        return

        # print text
        text = self.frame.get("text")

        var_start_index = None
        ch_index = 0
        while ch_index < len(text):
            if text[ch_index] == '{':
                var_start_index = ch_index
            elif text[ch_index] == '}':
                text = text.replace(text[var_start_index:ch_index + 1], str(self.variables.get(text[var_start_index + 1:ch_index])))
            ch_index += 1

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

            # arithmetics
            if type(var[action][1]) is str:
                try:
                    var[action][1] = eval(var[action][1])
                except:
                    pass

            self.variables[var[action][0]] = var[action][1]

        # set next frame
        self.set_frame(self.frame.get("actions")[action])

    def set_frame(self, id):
        for frame in self.story:
            if frame.get("id") == id:
                self.frame = frame
