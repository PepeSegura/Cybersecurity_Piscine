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
    if (input[1] != '2')
        no();
    if (input[0] != '4')
        no();

    fflush(stdin);

    char key[9] = {0};

    key[0] = '*';

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

    if (strcmp(key, "********"))
        no();
    ok();
}

// first 2 bytes must be '4''2'
// then, write the ascii code for each letter to complete the word "********"
// taking into account that there was already 1 '*' in the key we only need to put 7 more

//   *   *   *   *   *   *   *   *
// 042 042 042 042 042 042 042 042

// key = 42042042042042042042042