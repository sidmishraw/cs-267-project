#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include "SimplicialComplexNew.h"
#include "SCExport.h"
#include <dlfcn.h>

using namespace std;

int main()
{
    // ----------------------------------
    // API Testing: Usage 1
    // ----------------------------------
    SimplicialCmplx sim1(4, 0.097, 7, 3);
    const char *input[3];
    input[0] = "1110000";
    input[1] = "0111000";
    input[2] = "1101000";

    for (int i = 0; i < 3; i++)
        sim1.setBitMapRow(7, i, input[i]);

    sim1.process();

    // ----------------------------------
    // API Testing: Usage 2
    // ----------------------------------
    const char *file_path = "../data/dataSample-small1.dat";
    SimplicialCmplx sim2(4, 0.097, 7, 3, file_path);
    sim2.process();

    // ----------------------------------
    // Library Testing Usage - acquire exported APIs
    // ----------------------------------
    void* handle = dlopen("SCExport.so", RTLD_LAZY);

    SimplicialCmplx* (*create)();
    void (*initiallize)(SimplicialCmplx*, int, float, int, int, const char*);
    void (*setBitMapRow)(SimplicialCmplx*, int, int, const char*);
    void (*process)(SimplicialCmplx*);
    void (*remove)(SimplicialCmplx *);

    create = (SimplicialCmplx* (*)())dlsym(handle, "createInstance");
    initiallize = (void (*)(SimplicialCmplx*, int, float, int, int, const char*))dlsym(handle, "initialize");
    setBitMapRow = (void (*)(SimplicialCmplx*, int, int, const char*))dlsym(handle, "setBitMapRow");
    process = (void (*)(SimplicialCmplx*))dlsym(handle, "process");
    remove = (void (*)(SimplicialCmplx*))dlsym(handle, "removeInstance");

    // ----------------------------------
    // Library Testing Usage 1
    // ----------------------------------
    SimplicialCmplx* my_class1 = (SimplicialCmplx*)create();
    initiallize(my_class1, 4, 0.97, 7, 3, file_path);
    process(my_class1);
    remove(my_class1);

    // ----------------------------------
    // Library Testing Usage 2
    // ----------------------------------
    SimplicialCmplx* my_class2 = (SimplicialCmplx*)create();
    initiallize(my_class2, 4, 0.97, 7, 3, NULL);
    for (int i = 0; i < 3; i++)
        setBitMapRow(my_class2,7, i, input[i]);
    process(my_class2);
    remove(my_class2);

    return 0;
}