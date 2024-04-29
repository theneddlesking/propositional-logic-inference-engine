from src.knowledge_base import KnowledgeBase
from src.query import Query

class FileParser:

    @staticmethod
    def parse_standard_file_from_path(file_path: str) -> tuple[KnowledgeBase, Query]:
        with open(file_path, 'r') as file:
            # get the lines from the file
            lines = file.readlines()
            
            # file must have 4 lines
            if len(lines) != 4:
                raise ValueError('File must have 4 lines')
            
            # first line must be "TELL"
            if lines[0].strip() != 'TELL':
                raise ValueError('First line must be "TELL"')
            
            # third line must be "ASK"
            if lines[2].strip() != 'ASK':
                raise ValueError('Third line must be "ASK"')
            
            # second line is the knowledge base
            knowledge_base = KnowledgeBase.from_string(lines[1].strip())

            # fourth line is the query
            query = Query.from_string(lines[3].strip())

            # return the knowledge base and query
            return knowledge_base, query