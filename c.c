#include <stdio.h>

int main() {
    long long total = 0;
    for (int i = 1; i <= 100000000; i++) {
        total += i;
    }
    printf("%lld\n", total);
    return 0;
}
