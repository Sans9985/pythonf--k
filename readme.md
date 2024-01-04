# pythonf--k
a "language" which makes zero sense (literally)

## requirements
- python 3.x
- at most 128kB of disk space
  (though you can change the "memory" size easily so this depends on that)

## basics
this "language" is inspired from brainf--k, another "language" which uses about 7 characters.

pythonf--k is supposed to be an "easier" version, but it became different from brainf--k.

this language also has:
- a pointer
- **32 768 bytes** of "memory" *(wow thats a lot)*
- instructions *(so unique)*

## few details
- every instruction is executed in python (!)
- the base interpreter is in python (wow)
- every instruction is **one** special character
- **empty lines are ignored**

## what are the characters, and what do they do?

### legend:
- `[a]` = **required**;
- `{n}` = optional;
- `|x|` = *ignored*;

0. `*{c}`

    this is a comment. **comments must be on separate lines.**

1. `>{n}` and `<{n}`

    these change the pointer by `n`.
    if `n` is not provided, it'll change the pointer by 1.

    if the pointer goes under 0 or above 32767,
    it'll simply roll over to the other limit.

2. `/|x|`

    this reads the `input` file (with that specific name,
    doesn't work with other names), and inserts it into the memory
    at the current position of the pointer.
    
    *`x` is ignored.*

3. `\|x|`

    this does the same as `/`, except it loads the `output` file.

    *`x` is ignored.*

4. `.{n}`

    this writes the "memory" into the `output` file. (if it doesn't exists, it'll be created)

    if `n` is present (and its not 1), it will insert a `\n` after every `n`th byte.

5. `^{n}`

    this writes 1 byte into memory.

    `n` is a "byte", so it can only be **between 0 and 255**.

    if the parameter isn't present, it'll be replaced with `1`.

6. `,{n}`

    this sets the pointer value to `n`. if `n` is missing, it'll set the pointer to `1`.

7. `~([a];{b};...):[n]`

    this is a loop. it can only accept other characters as instructions in the places of `a` and `b`. **(except `~`)**

    it can have infinite instructions, but they must be separated by `;`. it will do the instructions `n` times.

    trailing semicolons are allowed, but **not** recommended.

    **`a` and `n` are required.**

    example of a loop:
    ```
    * write a capital A 128 times
    ~(^65;>):128
    ```

8. `_{s}`

    this simply writes `s` to the console.
    
    if `s` doesn't exists, it writes `1` to the console.
