from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('../templates'))
from . import DashboardHandler


class Handler(DashboardHandler):
    async def get(self):
        self.handler_name = __file__
        await super().get()

    @staticmethod
    def modify_doc(doc):
        print(Handler.data)
        pass

    async def get_data(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
