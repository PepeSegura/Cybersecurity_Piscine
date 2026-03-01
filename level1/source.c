#include <string.h>
#include <stdio.h>

int main(void) {
    const char password[] = "__stack_check";
    char input[100] = {0};

    printf("Please enter key: ");
    scanf("%s", input);

    if (strcmp(password, input) == 0)
        printf("Good job.\n");
    else
        printf("Nope.\n");
}
