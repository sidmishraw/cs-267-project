#ifndef __SimplicialComplexNew_H__
#define __SimplicialComplexNew_H__

#include <vector>
#include <map>
#include <string>

using namespace std;

/*
 * Simplicial complex is a collection of open simplicies, also known as 'K', such that every 
 * phases of the open simplex is in K. A collection of all association rules (database object) 
 * form a simplicial complex (geometry object). 
 *
 * Aprior principle in data mining is called closed condition in simplicial complex.
 */
struct Simplex {
    string gname;                   // group name: "0", "0 1", "0 1 2" and etc
    short nrules;                   // # of rules: 1, 2, 3 and etc
    vector<int> ones;               // [row#] -- inverted list of 1's
    vector<pair<short, vector<int> > > links; // [simplex, links] -- connected vertices on graph with AND'ed ones
};

class SimplicialCmplx
{
public:
    SimplicialCmplx();
    SimplicialCmplx(int rules, float threshold, int cols, int rows);
    SimplicialCmplx(int rules, float threshold, int cols, int rows, const char *file_path);
    ~SimplicialCmplx();

    void initialize(int rules, float threshold, int cols, int rows, const char *file_path);
    void setBitMapRow(int cols, int rows, const char *data);
    void process();

private:
    void initialize(int rules, float threshold, int cols, int rows);
    bool readFile(string strFile, int numCols, int numRows);
    void reduceSpace();
    void buildSimplex(Simplex& simplex, string& gname, int nrules, vector<int>& ones, vector<pair<short, int> >& cols, int start);
    void connectSimplex(Simplex& simplex);
    void printSimplex(Simplex& simplex);
    bool isLookupValid();

    vector<vector<bool> > m_data;         // [col][row#] -- input data matrix
    vector<vector<int> > m_lookup;        // [col][row#] -- inverted list of 1's
    vector<pair<short, int> > m_qcols;    // [simplex, count] -- sorted list of qualified counts
    map<short, int> m_results;            // [simplex, #items]
    FILE* m_fpResult;
    int m_thresholdLimit;

    int m_has_initialized;
    int m_rules;
    float m_threshold;
    int m_cols;
    int m_rows;
};

#endif