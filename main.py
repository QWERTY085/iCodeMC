from loader import dp, mybot
import logging as lg

if __name__ == '__main__':
    lg.basicConfig(level=lg.DEBUG)
    lg.info(f'Handlers loaded: {lg.__name__}')
    dp.run_polling(mybot)
