from pathlib import Path
from helpers.config import Config







def main():
    print('hello')



if __name__ == '__main__':

    app_path = Path(__file__).parent
    CONFIG = Config(app_path)


    main()