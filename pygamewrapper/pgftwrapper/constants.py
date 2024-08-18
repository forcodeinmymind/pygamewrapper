"""constants for pgftwrapper
2024-07-30
1.0.0
"""
import os

X = 0
Y = 1

MINX, MAXX, MINY, MAXY, ADVX, ADVY = range(6)
metrics_type_names = ("minx", "maxx", "miny", "maxy", "advx", "advy")

# str_calibration = r"0123456789abcdefghijklmnopqrstuvwxyzäöüABCDEFGHIJKLMNOPQRSTUVWXYZÄÖÜ !\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ ¡¢£¤¥¦§¨©ª«¬®¯°±²³´µ·¸¹º»¼½¾¿Ææ×ØÝÞßç÷øþĦħĿŀŁłŒœŦŧſƋƉƋƌƍƏƐƑƔƕƘƢƣƥƦƧƩƱ↵↓↔←→↑·☼ϟ☾❅❆♁▲▼►◄■▄▬▀░▒▓█░▒▓│┤║╣╗╝¢┐└┴┬├─┼╚╔╩╦╠═╬♛♕♚♔♜♖♝♗♞♘♟♙☗☖♠♣♦♥❥♡♢♤♧⚀⚁⚂⚃⚄⚅⚇⚆⚈⚉♚♛♜♝♞♟♔♕♖♗♘♙♠♣♥♦♤♧♡♢☗☖"
path = os.path.dirname(__file__)
path = os.path.join(path, "Codepage 850_manuel sorted.txt")
with open(path, "r", encoding="utf-8") as file:
    str_calibration = file.read()
