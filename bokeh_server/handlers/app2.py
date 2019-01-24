from jinja2 import Environment, FileSystemLoader

from . import DashboardHandler

env = Environment(loader=FileSystemLoader('../templates'))


class Handler(DashboardHandler):

    async def get(self):
        self.handler_name = __file__
        await super().get()

    @staticmethod
    def modify_doc(self):
        """
        modify and build your doc here
        :param self:
        :return:
        """
        print(Handler.data)
        pass

    async def get_data(self):
        pass


def main():
    pass


if __name__ == '__main__':
    main()
