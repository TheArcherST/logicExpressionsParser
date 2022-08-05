logicExpressionsParser
=====================

Can parse expressions following types:

```
false || !true & !(!false || !false) -> true == false
```

This returns `False`.

Supported operations:
1. Not `!`
2. And `&`
3. Or `||`
4. Implication `->`
5. Equality `==`

And file cases_creator.py adds next feature:
you can write letters into statement and look
for answers in all cases. Note that you must 
write `?` before your letter or name.

For example:

`?a & true`

```

?a   result
--- ------
0   False
1   True

```
