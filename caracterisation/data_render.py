from abc import ABC, abstractmethod


class DataRenderBase(ABC):
    '''
    Base Structure for get a output file
    '''

    @abstractmethod
    def generate_output_file(self):
        '''Generate the output file'''


class DataRenderJSON(DataRenderBase):
    '''
    Class to use for generate a JSON output file
    '''

    def generate_output_file(self):
        
        return super().generate_output_file()
