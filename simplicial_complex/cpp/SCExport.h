#ifndef __SCEXPORT_H__
#define __SCEXPORT_H__

#include "SimplicialComplexNew.h"

extern "C"
{
    SimplicialCmplx* createInstance();
    void removeInstance(SimplicialCmplx *p_instance);
    void initialize(SimplicialCmplx *p_instance, int rules, float threshold, int cols, int rows, const char *file_path);
    void setBitMapRow(SimplicialCmplx *p_instance, int cols, int row, const char *data);
    void process(SimplicialCmplx *p_instance);
    void directProcess(int rules, float threshold, int cols, int rows, const char *data);
}

#endif