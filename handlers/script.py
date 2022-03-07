import random


class alpha:

    alphabet = "abcdefghijklmnopqrstuvwxyz1234567890`',!?.-^:абвгґдеєжзиіїйклмнопрстуфхцчшщьюяыэъ)(*=_[]+@{}\n " + '"'

    count = len(alphabet)

    @staticmethod
    def dictionary_liter():
        alpha_dict = dict()
        for liter, i in zip(alpha.alphabet, range(alpha.count)):
            alpha_dict.update({liter: (i + 1)})
        return alpha_dict

    @staticmethod
    def dictionary_number():
        alpha_dict = dict()
        for liter, i in zip(alpha.alphabet, range(alpha.count)):
            alpha_dict.update({str(i + 1): liter})
        return alpha_dict


class cesar:
    with open("key.txt", "r") as file:
        key = int(file.read())
    alphabet_dict_liter = alpha.dictionary_liter()
    alphabet_dict_position = alpha.dictionary_number()

    @staticmethod
    def to_cesar(string: str):
        string = string.lower()

        current_liter_position = []
        for liter in string:
            current_liter_position.append(cesar.alphabet_dict_liter.get(liter))

        convert_position = []
        for position in current_liter_position:
            if position + cesar.key > alpha.count:
                position = (position + cesar.key) % alpha.count
            else:
                position += cesar.key
            convert_position.append(position)

        result = ""
        for position in convert_position:
            liter = cesar.alphabet_dict_position.get(str(position))
            if random.randint(0, 10) > 5:
                result += liter.upper()
            else:
                result += liter
        return result

    @staticmethod
    def from_cesar(string: str):
        string = string.lower()

        current_liter_position = []
        for liter in string:
            current_liter_position.append(cesar.alphabet_dict_liter.get(liter))

        convert_position = []
        for position in current_liter_position:
            if position - cesar.key <= 0:
                position = position + alpha.count - cesar.key
            else:
                position -= cesar.key
            convert_position.append(position)

        result = ""
        for position in convert_position:
            result += cesar.alphabet_dict_position.get(str(position))

        return result

