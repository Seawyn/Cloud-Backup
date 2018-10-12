Projeto de Redes de Computadores - Cloud Backup

Grupo 17
Elementos:
    Aylton Silva, nº86390
    Joana Teodoro, nº86440
    Jorge Pacheco, nº86457

O projeto desenvolvido consiste em 3 aplicações: um utilizador (user.py), um servidor central (CS.py) e um servidor de backup (BS.py).

Estas 3 componentes devem ser compiladas na seguinte ordem e forma:

  python3 CS.py [-p CSport]
  python3 BS.py [-b BSport] [-n CSname] [-p CSport]
  python3 user.py [-n CSname] [-p CSport]

Os argumentos em parênteses retos são opcionais.
