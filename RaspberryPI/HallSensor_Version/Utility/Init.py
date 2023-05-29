class Config:
    def __init__(self):
        self.Story = str()
        self.Writter = str()
        self.UUID = str()
        self.AudioPath = str()
        self.PlayList = dict()
        self.EffectList = dict()

    def load_config(self):
        import json

        with open('./config/init_Data.json') as json_file:
            json_data = json.load(json_file)
        
        return json_data

    def get_config(self, item):
        return self.load_config()[item]

    def load_audioList(self):
        import glob
        
        return glob.glob('./Story/Audio/*')

    def get_audioList(self):
        self.audioList = self.load_audioList()

        return self.audioList