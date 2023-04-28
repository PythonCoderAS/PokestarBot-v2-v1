#include <stdio.h>

#include <math.h>

#include "libminecraftxp.h"


unsigned long long xp_for_inner(unsigned long long level) {
    if (level >= 32){
        return 9 * (level - 1) - 158;
    } else if (17 <= level && level <= 31) {
        return 5 * (level - 1) - 38;
    } else if (1 <= level && level <= 16) {
        return 2 * (level - 1) + 7;
    } else if (level < 1){
        return 0;
    }

}

unsigned long long xp_at_inner(unsigned long long level) {
    if (level >= 32){
        return trunc(4.5 * pow(level, 2) - 162.5 * level + 2220);
    } else if (17 <= level && level <= 31) {
        return trunc(2.5 * pow(level, 2) - 40.5 * level + 360);
    } else if (0 <= level && level <= 16) {
        return trunc(pow(level, 2)) + 6 * level;
    }
}

unsigned long long calculate_level_inner(unsigned long long experience) {
    unsigned long long current_level = 0L;
    unsigned long long xp = experience;
    unsigned long long xp_needed;
    while (xp >= 0) {
        current_level++;
        xp_needed = xp_for_inner(current_level);
        if (xp_needed > xp) {
            current_level++;
            break;
        }
        xp = xp - xp_needed;
    }
    return current_level - 2;
}

/*int main(int argc, char ** argv) {
    printf("%lu\n", sizeof(unsigned long long));
    printf("%llu\n", calculate_level_inner(18446744073709551615 ULL));
}*/
