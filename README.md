logicStatementsParser
=====================

Can parse statements following types:

```
false || !true & !(!false || !false) -> true == false
```

This statement returns `False`.

Supported operations:
1. Not `!`
2. And `&`
3. Or `||`
4. Implication `->`
5. Equality `==`

And file cases_creator.py adds next feature:
you can write letters into statement and look
for answers in all cases.

For example:

`a & true`

a   result
--- ------
0   False
1   True
