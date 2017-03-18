#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "SimplicialComplexNew.h"

using namespace std;

int main()
{
    // Testing: Usage 1
    SimplicialCmplx sim1(4, 0.097, 7, 3);
    const char *input[3];
    input[0] = "1110000";
    input[1] = "0111000";
    input[2] = "1101000";

    for (int i = 0; i < 3; i++)
        sim1.setBitMapRow(7, i, input[i]);

    sim1.process();

    // Testing: Usage 2
    const char *file_path = "../data/dataSample-small1.dat";
    SimplicialCmplx sim2(4, 0.097, 7, 3, file_path);
    sim2.process();

    return 0;
}