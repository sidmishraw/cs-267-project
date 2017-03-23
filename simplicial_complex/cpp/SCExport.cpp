#include "SCExport.h"
#include <iostream>

using namespace std;

SimplicialCmplx* createInstance()
{
    return new SimplicialCmplx();
}

void removeInstance(SimplicialCmplx *p_instance)
{
    if (!p_instance)
        delete p_instance;
}

void initialize(SimplicialCmplx *p_instance, int rules, float threshold, int cols, int rows, const char* file_path)
{
    if (!p_instance) return;
    if (file_path)
        p_instance->initialize(rules, threshold, cols, rows, file_path);
    else
        p_instance->initialize(rules, threshold, cols, rows, NULL);
}

void setBitMapRow(SimplicialCmplx *p_instance, int cols, int row, const char *data)
{
    if (!p_instance) return;
    p_instance->setBitMapRow(cols, row, data);
}

void process(SimplicialCmplx *p_instance)
{
    if (!p_instance) return;
    p_instance->process();
}

void directProcess(int rules, float threshold, int cols, int rows, const char *data)
{
    if (!data) return;

    // initialize
    SimplicialCmplx *p_instance = new SimplicialCmplx(rules, threshold, cols, rows);

    // set bit-vector
    char *p_row_data = (char *)malloc(cols * sizeof(char));
    for (int i = 0; i < rows; i++)
    {
        memcpy(p_row_data, data + i * cols, cols * sizeof(char));
        p_instance->setBitMapRow(cols, i, p_row_data);
    }
    free(p_row_data);

    // process
    p_instance->process();

    // release
    delete p_instance;
}
