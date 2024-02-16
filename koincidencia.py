from koincidencia_fuggvenyek import *


def main():

    tc=time_controller_csatlakozas()

    idokezdet = datetime.datetime.now()


    configure(tc,200)





    idovege=datetime.datetime.now()
    print()
    print(idovege-idokezdet)


if __name__ == "__main__":
    main()
