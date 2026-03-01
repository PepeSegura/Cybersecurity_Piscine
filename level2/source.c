#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void no()
{
    puts("NOPE.");
    exit(1);
}

void ok()
{
    puts("Good job.");
}

int main(void) {
    char input[24] = {0};
    printf("Please enter key: ");
    int ret = scanf("%23s", input);

    if (ret != 1)
        no();
    if (input[1] != '0')
        no();
    if (input[0] != '0')
        no();

    fflush(stdin);

    char key[9] = {0};

    key[0] = 'd';

    char c[4] = {0};

    int index_key = 1;
    int input_index = 2;
    while (1)
    {
        int key_not_full = 0;
        if (strlen(key) < 8)
        {
            key_not_full = input_index < strlen(input);
        }
        if (key_not_full == 0)
            break;

        c[0] = input[input_index];
        c[1] = input[input_index + 1];
        c[2] = input[input_index + 2];

        int decoded_char = atoi(c);
        key[index_key] = decoded_char;
        index_key += 1;
        input_index += 3;
    }

    if (strcmp(key, "delabere"))
        no();
    ok();
}

// first 2 bytes must be '0''0'
// then, write the ascii code for each letter to complete the word delabere
// taking into account that thte 'd' was already in the key, so only elabere

//   d   e   l   a   b   e   r   e
// 100 101 108 097 098 101 114 101

// key = 00101108097098101114101