Testing the Oatbran
===================

::

    # python standard library
    import unittest
    import random
    import re
    
    #third-party
    try:
        import numpy.random as nrandom
    except ImportError:
        pass
    # this package
    from randomizer import Randomizer
    from oatbran import *
    
    

::

    L_GROUP = '('
    R_GROUP = ')'
    L_PERL_GROUP = L_GROUP + "?"
    
    

::

    class TestOatBranGroup(unittest.TestCase):
        def test_group(self):
            """
            Does the group method add parentheses?
            """
            sample = Randomizer.letters()
            exp = Group.group(sample)
            self.assertEqual("(" + sample + ")",exp)
            matched = re.search(exp,sample+Randomizer.letters()).groups()[0]
            self.assertEqual(matched, sample)
            return
    
        def test_named(self):
            """
            Does the named method create a named group?
            """
            name = Randomizer.letters()
            sample = Randomizer.letters()
            text = Randomizer.letters() + sample + Randomizer.letters()
            exp = Group.named(name=name, expression=sample)
            expected = '(?P<' + name + '>' + sample + ")"
            self.assertEqual(expected, exp)
            matched = re.search(exp, text).groupdict()[name]
            self.assertEqual(sample, matched)
            return
    
        def test_followed_by(self):
            """
            Does it match strings followed by a pattern?
            """
            body = Randomizer.letters()
            sub_string = Randomizer.letters()
            suffix = Randomizer.letters()
            text = body + sub_string + suffix
            name = 'followed'
            expression = Group.named(name,
                                     sub_string + Group.followed_by(suffix))
            match = re.search(expression, text)
            self.assertEqual(match.group(name), sub_string)
    
        def test_not_followed_by(self):
            """
            Does not_followed_by create a negative lookahead assertion?
            """
    
            prefix = Randomizer.letters(maximum=5)
            suffix = Randomizer.letters_complement(prefix)
            expr = Group.not_followed_by(suffix)
            text = Randomizer.letters() 
            self.assertEqual(L_PERL_GROUP + '!' + suffix + R_GROUP,
                             expr)
    
            self.assertIsNone(re.search(text + expr, text + suffix))
            self.assertIsNotNone(re.search(text + expr, text))
            return
    
        def test_preceded_by(self):
            "Does it match a substring with a prefix?"
            name = 'preceded'
            body = Randomizer.letters()
            sub_string = Randomizer.letters()
            prefix = Randomizer.letters()
            expression = Group.named(name,
                                     Group.preceded_by(prefix) + sub_string)
            text = body + prefix + sub_string
            match = re.search(expression, text)
            self.assertEqual(match.group(name),
                             sub_string)
    
        def test_not_preceded_by(self):
            '''
            Does it create a negative look-behind expression?
            '''
            prefix = Randomizer.letters()
            expr = Group.not_preceded_by(prefix)
            self.assertEqual(L_PERL_GROUP + "<!" + prefix + R_GROUP,
                             expr)
            text = Randomizer.letters(minimum=5)
    
            is_preceded_by = prefix + text
            self.assertIsNone(re.search(expr + text, is_preceded_by))
            self.assertIsNotNone(re.search(expr + text, text))
            return
    
    

::

    class TestOatBranClass(unittest.TestCase):
        def test_class(self):
            '''
            Does it convert the string to a character class?
            '''
            sample = Randomizer.letters()
            expression = CharacterClass.character_class(sample)
            self.assertEqual(LEFT_BRACKET + sample + RIGHT_BRACKET, expression)
    
            sub_string = random.choice(sample)
            complement = Randomizer.letters_complement(sample)
    
            self.assertIsNotNone(re.search(expression, sub_string))
            self.assertIsNone(re.search(expression, complement))
            return
    
        def test_not(self):
            '''
            Does it convert the string to a non-matching class?
            '''
            sample = Randomizer.letters(maximum=10)
            complement = Randomizer.letters_complement(sample)
            expression = CharacterClass.not_in(sample)
            self.assertEqual(LEFT_BRACKET + '^' + sample + RIGHT_BRACKET,
                             expression)
    
            self.assertIsNone(re.search(expression, sample))
            self.assertIsNotNone(re.search(expression, complement))
            return
    
        def test_alpha_num(self):
            """
            Does it return alpha-num character class (plus underscore)?
            """
            expression = CharacterClass.alpha_num
            character = random.choice(string.letters + string.digits + '_')
            non_alpha = random.choice(string.punctuation.replace('_', ''))
            self.assertIsNotNone(re.search(expression, character))
            self.assertIsNone(re.search(expression, non_alpha))
            return
    
        def test_alpha_nums(self):
            """
            Does it return the expression to match one or more alpha-nums?
            """
            expression = CharacterClass.alpha_nums
    
    



.. autosummary::
   :toctree: api

   TestQuantifier.test_one_or_more
   TestQuantifier.test_zero_or_more
   
::

    class TestQuantifier(unittest.TestCase):
        def test_one_or_more(self):
            """
            Does it return the one-or-more metacharachter?
            """
            character = random.choice(string.letters)
            complement = Randomizer.letters_complement(character)
    
            text = Randomizer.letters() + character * random.randint(1,100) + R
    andomizer.letters()
            expression = character + '+'
            self.assertIsNone(re.search(expression, complement))
            self.assertIsNotNone(re.search(expression, text))
            return
    
        def test_zero_or_more(self):
            """
            Does it return the kleene star?
            """
            substring = Randomizer.letters()
            text = Randomizer.letters()
            complement = text + Randomizer.letters_complement(substring)
            expression = text + Quantifier.zero_or_more('(' + substring + ')')
            text_1 = text + substring * random.randint(0, 10) + Randomizer.lett
    ers()
            self.assertIsNotNone(re.search(expression, complement))
            self.assertIsNotNone(re.search(expression, text_1))
            return
    
        def test_zero_or_one(self):
            """
            Does it return the zero-or-one quantifier?
            """
            substring = Randomizer.letters()
            text = Randomizer.letters()
            expression = text +  Quantifier.zero_or_one("(" + substring + ")")
            text_1 = text + substring * random.randint(1,100)
            text_2 = text + substring * random.randint(1,100)
            self.assertIsNotNone(re.search(expression, text_1))
            self.assertEqual(re.search(expression, text_2).groups()[0], substri
    ng)
            return
    
        def test_exactly(self):
            """
            Does it return the repetition suffix?
            """
            repetitions = Randomizer.integer(minimum=1, maximum=5)
            repeater = Randomizer.letters()
            expected = "{" + "{0}".format(repetitions) + "}"
            quantifier = Quantifier.exactly(repetitions)
            self.assertEqual(expected, quantifier)
            expression = "(" + repeater + ")" + quantifier
            text = Randomizer.letters() + repeater * (repetitions + Randomizer.
    integer(minimum=0))
            self.assertIsNotNone(re.search(expression, text))
            self.assertEqual(re.search(expression, text).groups(), (repeater,))
    
            return
    
        def test_m_to_n(self):
            """
            Does it return the expression to match m-to-n repetitions
            """
            m = Randomizer.integer(minimum=5)
            n = Randomizer.integer(minimum=m+1)
            substring = Randomizer.letters()
            quantifier = Quantifier.m_to_n(m,n)
            expression = '(' + substring + ')' + quantifier
            self.assertEqual("{" + str(m) + ',' + str(n) + '}',quantifier)
            text = Randomizer.letters() + substring * Randomizer.integer(m, n)
            complement = (Randomizer.letters_complement(substring) +
                          substring * Randomizer.integer(0,m-1))
            too_many = substring * Randomizer.integer(n+1, n*2)
            self.assertIsNotNone(re.search(expression, text))
            self.assertIsNone(re.search(expression, complement))
            self.assertEqual(re.search(expression, too_many).groups(), (substri
    ng,))
            return
    
    
    

::

    class TestBoundaries(unittest.TestCase):
        def test_word_boundary(self):
            """
            Does it add word-boundaries to the expression
            """
            word = Randomizer.letters()
            expected = r'\b' + word + r'\b'
            expression = Boundaries.word(word)
            bad_word = word + Randomizer.letters()
            text = ' '.join([Randomizer.letters(),word,Randomizer.letters()])
            self.assertIsNone(re.search(expression, bad_word))
            self.assertIsNotNone(re.search(expression, text))
            return
    
        def test_string_boundary(self):
            """
            Does it add boundaries to match a whole line?
            """
            substring = Randomizer.letters()
            expression = Boundaries.string(substring)
            expected = "^" + substring + "$"
            self.assertEqual(expected, expression)
            self.assertIsNotNone(re.search(expression, substring))
            self.assertIsNone(re.search(expression, ' ' + substring))
            return
    
        def test_string_start(self):
            """
            Does it have return a string start metacharacter?
            """
            metacharacter = Boundaries.string_start
            expected = '^'
            self.assertEqual(expected, metacharacter)
            word = Randomizer.letters()
            expression = Boundaries.string_start + word
            text = word + Randomizer.letters()
            self.assertIsNotNone(re.search(expression, text))
            self.assertIsNone(re.search(expression, " " + text))
            return
    
        def test_string_end(self):
            """
            Does it return the end of string metacharacter?
            """
            metacharacter = Boundaries.string_end
            word = Randomizer.letters()
            expression = word + metacharacter
            text = Randomizer.letters() + word
            self.assertIsNotNone(re.search(expression, text))
            self.assertIsNone(re.search(expression, text + Randomizer.letters()
    ))
            return
    
    

::

    class TestNumbers(unittest.TestCase):
        def test_decimal_point(self):
            """
            Does it return a decimal point literal?
            """
            metacharacter = Numbers.decimal_point
            test = random.uniform(0,100)
            self.assertIsNotNone(re.search(metacharacter, str(test)))
            self.assertIsNone(re.search(metacharacter, Randomizer.letters()))
            return
    
        def test_digit(self):
            """
            Does it return the digit character class?
            """
            metacharacter = CharacterClass.digit
            test = Randomizer.integer(maximum=9)
            self.assertIsNotNone(re.search(metacharacter, str(test)))
            self.assertIsNone(re.search(metacharacter, Randomizer.letters()))
            return
    
        def test_non_digit(self):
            """
            Does it return the anything-but-a-digit metacharacter?
            """
            metacharacter = CharacterClass.non_digit
            test = str(Randomizer.integer(maximum=9))
            self.assertIsNone(re.search(metacharacter, test))
            return
    
        def test_non_zero(self):
            """
            Does it return an expression to match 1-9 only?
            """
            expression = CharacterClass.non_zero_digit
            test = str(random.choice(range(1,10)))
            self.assertIsNotNone(re.search(expression, test))
            self.assertIsNone(re.search(expression, '0'))
            return
    
        def test_single_digit(self):
            """
            Does it return an expression to match only one digit?
            """
            expression = Numbers.single_digit
            test = str(Randomizer.integer(maximum=9))
            two_many = str(Randomizer.integer(minimum=10))
            self.assertIsNotNone(re.search(expression, test))
            self.assertIsNone(re.search(expression, two_many))
            return
    
        def test_two_digits(self):
            """
            Does it return an expression to match exactly two digits?
            """
            expression = Numbers.two_digits
            test = str(Randomizer.integer(minimum=10,maximum=99))
            fail = random.choice([str(Randomizer.integer(0,9)), str(Randomizer.
    integer(100,1000))])
            self.assertIsNotNone(re.search(expression, test))
            self.assertIsNone(re.search(expression, fail))
            return
    
        def test_one_hundreds(self):
            """
            Does it match values from 100-199?
            """
            number = "{0}".format(random.randint(100,199))
            low_number = str(random.randint(-99,99))
            high_number = str(random.randint(200,500))
            float_number = str(random.uniform(100,199))
            text = Randomizer.letters() + str(random.randint(100,199))
            name = 'onehundred'
            expression = re.compile(Group.named(name,
                                                Numbers.one_hundreds))
            self.assertIsNotNone(re.search(Numbers.one_hundreds, number))
            self.assertIsNone(re.search(Numbers.one_hundreds, low_number))
            self.assertIsNone(re.search(Numbers.one_hundreds, high_number))
            # it only checks word boundaries and the decimal point is a boundar
    #y
            self.assertIsNotNone(re.search(Numbers.one_hundreds, float_number))
    
            # it needs a word boundary so letters smashed against it will fail
            self.assertIsNone(re.search(Numbers.one_hundreds, text))
            return
    
        def test_digits(self):
            "Does it match one or more digits?"
            expression = Group.named(name='digits', expression=Numbers.digits)
            first = "{0}".format(random.randint(0,9))
            rest = str(random.randint(0,1000))
            test = first + rest
            self.assertIsNotNone(re.search(expression, test))
            match = re.search(expression, test)
            self.assertEqual(match.group('digits'), test)
            mangled = Randomizer.letters() + test + Randomizer.letters()
            match = re.search(expression, mangled)
            self.assertEqual(match.group('digits'), test)
            return
    
        def test_zero(self):
            "Does it match zero by itself?"
            name = 'zero'
            expression = Group.named(name,
                                     Numbers.zero)
            prefix = random.choice(['', ' '])
            suffix = random.choice(['', ' '])
            zero = '0'
            text = prefix + zero + suffix
            match = re.search(expression, text)
            self.assertEqual(match.group(name), zero)
            self.assertIsNone(re.search(expression, str(random.randint(1,100)))
    )
            return
            
    
        def test_positive_integers(self):
            'Does it only match 1,2,3,...?'
            name = 'positiveintegers'
            expression = Group.named(name,
                                     Numbers.positive_integer)
            regex = re.compile(expression)
            # zero should fail
            self.assertIsNone(regex.search('0' ))
    
            # positive integer (without sign) should match
            first_digit = str(nrandom.randint(1,9))
            positive_integer = first_digit + ''.join(str(i) for i in nrandom.ra
    ndom_integers(1,9,
                                                                               
    size=nrandom.randint(100)))
            match = regex.search(positive_integer)
            self.assertEqual(match.group(name), positive_integer)
    
            # negative integer should fail
            negation = '-' + positive_integer
            self.assertIsNone(regex.search(negation))
    
            # surrounding white space should be trimmed off
            spaces = " " * nrandom.randint(100) + positive_integer + ' ' * nran
    dom.randint(100)
            match = regex.search(spaces)
            self.assertEqual(match.group(name), positive_integer)
    
            # leading zero should fail
            leading_zeros = '0' * nrandom.randint(1,100) + positive_integer
            self.assertIsNone(regex.search(leading_zeros))
            return
    
        def test_integers(self):
            """
            Does it match positive and negative integers?
            """
            name = 'integer'
            expression = Group.named(name, Numbers.integer)
            regex = re.compile(expression)
            # 0 alone should match
            zero = '0'
            match = regex.search(zero)
            self.assertEqual(match.group(name), zero)
    
            # positive_integers should match
            first_digit = str(nrandom.randint(1,9))
            positive = first_digit +''.join(str(i) for i in nrandom.random_inte
    gers(0,9, nrandom.randint(1, 100)))
            match = regex.search(positive)
            self.assertEqual(match.group(name), positive)
    
            # negatives should match
            negative = '-' + positive
            match = regex.search(negative)
            self.assertEqual(match.group(name), negative)
    
            # white space boundaries should work too
            number = nrandom.choice(('','-')) + positive
            text = " " * nrandom.randint(10) + number  + ' ' * nrandom.randint(
    10)
            match = regex.search(text)
            self.assertEqual(match.group(name), number)
    
            # punctuation should work (like for csvs)
            text = number + ','
            match = regex.search(text)
            self.assertEqual(match.group(name), number)
    
            # match prefix to decimal points
            # this is not really what I wanted but otherwise it's hard to use i
    #n text
            text = number + '.' + str(nrandom.randint(100))
            match = regex.search(text)
            self.assertEqual(match.group(name), number)
            return
    
        def test_nonnegative_integer(self):
            """
            Does it match positive integers and 0?
            """
            name = 'nonnegative'
            expression = Group.named(name,
                                     Numbers.nonnegative_integer)
            regex = re.compile(expression)
            number = str(nrandom.randint(1,9)) + str(nrandom.randint(1000))
            match = regex.search(number)
            self.assertEqual(number, match.group(name))
    
            # should match 0
            zero = '0'
            match = regex.search(zero)
            self.assertEqual(match.group(name), zero)
    
            # should not match negative
            # but, to allow it in text, it will grab the integer to the right
            # in other words, it assumes the `-` is part of a sentence but not 
    #part of the number
            negation = '-' + number
            match = regex.search(negation)
            self.assertEqual(match.group(name), number)
            return
    
        def assert_match(self, regex, text, name, expected):
            match = regex.search(text)
            actual = match.group(name)
            message = "Source: '{t}', Expected: {e}, Actual: {a}".format(t=text
    ,
                                                                         e=expe
    cted,
                                                                         a=actu
    al)
            self.assertEqual(actual, expected, msg=message)
            return
    
        def test_real(self):
            """
            Does it match floating-point numbers?
            """
            name = 'real'
            expression = Group.named(name,
                                     Numbers.real)
            regex = re.compile(expression)
            # does it match 0?
            zero = '0'
            self.assert_match(regex, zero, name, zero)
    
            # does it match a leading 0?
            number = '0.' + str(nrandom.randint(100))
            self.assert_match(regex, number, name, number)
    
            # does it match a whole decimal
            number = str(nrandom.randint(1,100)) + '.' + str(nrandom.randint(10
    0))
            self.assert_match(regex, number, name, number)
    
            # what about positive and negative?
            number = (random.choice(('', '-')) + str(nrandom.randint(100)) +
                      random.choice(('', '.')) + str(nrandom.randint(100)))
            text = ' ' * nrandom.randint(5) + number + ' ' * nrandom.randint(5)
    
            self.assert_match(regex, text, name, number)
    
            # what happens if it comes at the end of a sentence?
            #number = (random.choice(('', '-')) + str(nrandom.randint(100)) +
            #          random.choice(('', '.')) + str(nrandom.randint(100)))
            #text = number + '.'
            #self.assert_match(regex, text, name, number)
    
            # I decided to let it be more lenient and match 2. as a decimal
            return
    
        def test_hexadecimal(self):
            """
            Does it match hexadecimal numbers?
            """
            name = 'hexadecimal'
            number = ''.join((random.choice(string.hexdigits) for char in xrang
    e(random.randint(1,100))))
            non_hex = 'IJKLMNOPQRSTUVWXYZ'
            text = random.choice(non_hex) + number + non_hex
            expression = re.compile(Group.named(name,
                                     Numbers.hexadecimal))
            match = expression.search(text)
            self.assertEqual(match.group(name), number)
            return
    
    
    

::

    class TestFormalDefinition(unittest.TestCase):
        def test_empty_string(self):
            "Does it match only an empty string?"
            name = 'empty'
            expression = Group.named(name,
                                     FormalDefinition.empty_string)
            empty = ''
            not_empty = Randomizer.letters()
            match = re.search(expression, empty)
            self.assertEqual(empty, match.group(name))
            self.assertIsNone(re.search(expression, not_empty))
            return
    
        def test_alternation(self):
            """
            Does it match alternatives?
            """
            name = 'or'
            # this might fail if one of the terms is a sub-string of another
            # and the longer term is chosen as the search term
            terms = [Randomizer.letters() for term in range(random.randint(10, 
    100))]
            expression = Group.named(name,
                                     FormalDefinition.alternative.join(terms))
            test = terms[random.randrange(len(terms))]
            match = re.search(expression, test)
            self.assertEqual(test, match.group(name))
            return
    
        def test_kleene_star(self):
            """
            Does it match zero or more of something?
            """
            name = 'kleene'
            term = random.choice(string.letters)
            expression = Group.named(name,
                                     term + FormalDefinition.kleene_star)
            test = term * random.randint(0, 100)
            match = re.search(expression, test)
            self.assertEqual(test, match.group(name))
            return
    
    

::

    class TestNetworking(unittest.TestCase):
        def test_octet(self):
            """
            Does it match a valid octet?
            """
            name = 'octet'
            expression = re.compile(Group.named(name,
                                                Networking.octet))
            for t1 in '198 10 1 255'.split():
                match = expression.search(t1)
                self.assertEqual(t1, match.group(name))
            bad_octet = random.randint(256, 999)
            self.assertIsNone(expression.search(str(bad_octet)))
            return
    
        def test_ip_address(self):
            """
            Does it match a valid ip address?
            """
            name = 'ipaddress'
            expression = re.compile(Group.named(name,
                                                Networking.ip_address))
            for text in '192.168.0.1 10.10.10.2 76.83.100.234'.split():
                match = expression.search(text)
                self.assertEqual(match.group(name), text)
            for bad_ip in "10.10.10 12.9.49.256 ape".split():
                self.assertIsNone(expression.search(bad_ip))
            return
    
        def test_mac_address(self):
            name = 'macaddress'
            expression = re.compile(Group.named(name,
                                                Networking.mac_address))
            text = 'f8:d1:11:03:12:58'
            self.assertEqual(expression.search(text).group(name),
                             text)
            return
    
    



