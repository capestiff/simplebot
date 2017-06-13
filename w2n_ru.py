russian_number_system = {
    'ноль': 0,
    'один': 1,
    'одна': 1,
    'одну': 1,
    'два': 2,
    'две': 2,
    'три': 3,
    'четыре': 4,
    'пять': 5,
    'шесть': 6,
    'семь': 7,
    'восемь': 8,
    'девять': 9,
    'десять': 10,
    'одиннадцать': 11,
    'двенадцать': 12,
    'тринадцать': 13,
    'четырнадцать': 14,
    'пятнадцать': 15,
    'шестнадцать': 16,
    'семнадцать': 17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать': 20,
    'тридцать': 30,
    'сорок': 40,
    'пятьдесят': 50,
    'шестьдесят': 60,
    'семьдесят': 70,
    'восемьдесят': 80,
    'девяносто': 90,
    'сто': 100,
    'двести': 200,
    'триста': 300,
    'четыреста': 400,
    'пятьсот': 500,
    'шестьсот': 600,
    'семьсот': 700,
    'восемьсот': 800,
    'девятьсот': 900,
    'тысяча': 1000,
    'тысяч': 1000,
    'тысячи': 1000,
    'миллион': 1000000,
    'миллиона': 1000000,
    'миллионов': 1000000,
    'миллиард': 1000000000,
    'миллиарда': 1000000000,
    'миллиардов': 1000000000,
    'целая': '.',
    'целых': '.',
    'целую': '.',
    'и': '.',
    'десятых': 0.1,
    'десятая': 0.1,
    'сотых': 0.01,
    'сотая': 0.01,
    'тысячных': 0.001,
    'тысячная': 0.001,
    'плюс': 0,
    'минус': 0,
    'разделить': 0,
    'умножить': 0,
    'на': 0,
}

"""
function to form numeric multipliers for million, billion, thousand etc.
input: list of strings
return value: integer
"""

def number_formation(number_words):
    numbers = []
    for number_word in number_words:
        numbers.append(russian_number_system[number_word])
    if len(numbers) == 4:
        if 1000 in numbers or 1000000 in numbers or 1000000000 in numbers:
            return (numbers[0] + numbers[1] + numbers[2]) * numbers[3]
        else:
            return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        if 1000 in numbers or 1000000 in numbers or 1000000000 in numbers:
            return (numbers[0] + numbers[1]) * numbers[2]
        else:
            return numbers[0] + numbers[1] + numbers[2]
    elif len(numbers) == 2:
        if 1000 in numbers or 1000000 in numbers or 1000000000 in numbers:
            return numbers[0] * numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


"""
function to convert post decimal digit words to numerial digits
input: list of strings
output: double
"""

def decimal_formation(decimal_words):
    numbers = []
    for number_word in decimal_words:
        numbers.append(russian_number_system[number_word])
    if len(numbers) == 4:
        if 0.1 in numbers or 0.01 in numbers or 0.001 in numbers:
            return (numbers[0] + numbers[1] + numbers[2]) * numbers[3]
    elif len(numbers) == 3:
        if 0.1 in numbers or 0.01 in numbers or 0.001 in numbers:
            return (numbers[0] + numbers[1]) * numbers[2]
    elif len(numbers) == 2:
        if 0.1 in numbers or 0.01 in numbers or 0.001 in numbers:
            return numbers[0] * numbers[1]
    elif len(numbers) == 1:
            return numbers[0] * 0.1
    else:
        return numbers[0]

"""
function to return integer for an input `number_sentence` string
input: string
output: int or double or None
"""


def word_to_num(number_sentence):

    number_sentence = number_sentence.lower()  # converting input to lowercase

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in russian_number_system:
            clean_numbers.append(word)

    # separate decimal part of number (if exists)
    if clean_numbers.count('целых') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('целых')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('целых')]
    if clean_numbers.count('целую') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('целую')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('целую')]
    if clean_numbers.count('целая') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('целая')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('целая')]
    if clean_numbers.count('и') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('и')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('и')]

    if 'миллиард' in clean_numbers:
        billion_index = clean_numbers.index('миллиард')
    elif 'миллиарда' in clean_numbers:
        billion_index = clean_numbers.index('миллиарда')
    elif 'миллиардов' in clean_numbers:
        billion_index = clean_numbers.index('миллиардов')
    else:
        billion_index = -1

    if 'миллион' in clean_numbers:
        million_index = clean_numbers.index('миллион')
    elif 'миллиона' in clean_numbers:
        million_index = clean_numbers.index('миллиона')
    elif 'миллионов' in clean_numbers:
        million_index = clean_numbers.index('миллионов')
    else:
        million_index = -1

    if 'тысяча' in clean_numbers:
        thousand_index = clean_numbers.index('тысяча')
    elif 'тысячи' in clean_numbers:
        thousand_index = clean_numbers.index('тысячи')
    elif 'тысяч' in clean_numbers:
        thousand_index = clean_numbers.index('тысяч')
    else:
        thousand_index = -1

    total_sum = 0  # storing the number to be returned

    if len(clean_numbers) > 0:
        if len(clean_numbers) == 1:
                total_sum += russian_number_system[clean_numbers[0]]
        else:
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum += thousand_multiplier * 1000

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:])
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:])
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum += hundreds

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = decimal_formation(clean_decimal_numbers)
        total_sum += decimal_sum

    return total_sum