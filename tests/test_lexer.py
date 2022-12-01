from lexer import Lexer, Token


def test_normalization():
    assert Lexer.normalize_text('!1||0') == '! 1 || 0'
    assert Lexer.normalize_text('!()&||->==').strip() == '! ( ) & || -> =='


def test_unknown_names():
    assert set(Lexer.get_unknown_names('1 -> true -> True -> ?a')) == {'True', '?a'}


def test_tokens():
    lexer = Lexer('! 1 -> ! ( false -> true )')
    result = list(lexer.iterator())
    assert result == [
        Token(type='NOT', op_type='UNARY', value='!', real_position=0),
        Token(type='BOOL', op_type='FACTOR', value=True, real_position=2),
        Token(type='IMPLICATION', op_type='BINARY', value='->', real_position=4),
        Token(type='NOT', op_type='UNARY', value='!', real_position=7),
        Token(type='LPAREN', op_type='FACTOR', value='(', real_position=9),
        Token(type='BOOL', op_type='FACTOR', value=False, real_position=11),
        Token(type='IMPLICATION', op_type='BINARY', value='->', real_position=17),
        Token(type='BOOL', op_type='FACTOR', value=True, real_position=20),
        Token(type='RPAREN', op_type='FACTOR', value=')', real_position=25),
        Token(type='EOF', op_type='EOF', value=None, real_position=None)
    ]
