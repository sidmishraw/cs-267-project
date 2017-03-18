/*
 * CS298 Thesis Project -- Simplicial Complex Version New
 * David Le (Student ID: 008-144-669)
 * January 18, 2016
 */

#include <algorithm>
#include <iostream>
#include <sstream>
#include <string>
#include <time.h>
#include <stdio.h>
#include "SimplicialComplexNew.h"

bool brief = false;
bool debug = false;

/*
 * Sort by QualifiedCount/ColumnIndex
 */
bool compareCounts(pair<short, int>& elem1, pair<short, int>& elem2)
{
    if (elem1.second != elem2.second) { return (elem1.second < elem2.second); }
    return (elem1.first < elem2.first);
}

/*
 * argument 1: # of association rules
 * argument 2: threshold for qualification
 * argument 3: # of columns
 * argument 4: # of records
 * argument 5: input data file
 * argument 6: show brief summary only
 */

SimplicialCmplx::SimplicialCmplx()
    : m_rules(0)
    , m_threshold(0.f)
    , m_cols(0)
    , m_rows(0)
    , m_has_initialized(false)
    , m_fpResult(NULL)
    , m_thresholdLimit(0)
{
    cout << "Invalid constructor!! \
    Usage: SimplicialCmplx(int rules, float threshold, int cols, int rows" << endl;
}

SimplicialCmplx::SimplicialCmplx(int rules, float threshold, int cols, int rows)
{
    m_has_initialized = false;
    initialize(rules, threshold, cols, rows);
}

SimplicialCmplx::SimplicialCmplx(int rules, float threshold, int cols, int rows, const char *file_path)
{
    m_has_initialized = false;
    initialize(rules, threshold, cols, rows);

    string input_file = file_path;
    if (!readFile(input_file, cols, rows)) return;
    m_has_initialized = true;
}

SimplicialCmplx::~SimplicialCmplx()
{

}

void SimplicialCmplx::initialize(int rules, float threshold, int cols, int rows)
{
    m_rules = rules;
    m_threshold = threshold;
    m_cols = cols;
    m_rows = rows;
    
    m_data.assign(cols, vector<bool>(rows, false));
    m_lookup.assign(cols, vector<int>());
    m_thresholdLimit = (int)(threshold * rows);
    m_thresholdLimit = (m_thresholdLimit == 0 ? 1 : m_thresholdLimit);

    m_fpResult = fopen("results.txt", "wt");
}

void SimplicialCmplx::setBitMapRow(int cols, int rows, const char *row_data)
{
    if (cols < 0 || cols > m_cols || rows < 0 || rows > m_rows) return;
    for (int i = 0; i < cols; i++)
        m_data[i][rows] = row_data[i] == '1';

    m_has_initialized = true;
}

bool SimplicialCmplx::isLookupValid()
{
   // check lookup table if it's valid
    int lookup_checksum = 0;
    for (int i = 0; i < m_cols; i++)
        lookup_checksum += m_lookup[i].size();

    return lookup_checksum != 0;
}

void SimplicialCmplx::process()
{
    if (!m_has_initialized)
    {
        cout << "Please initialize properly" << endl;
        return;
    }

    // check lookup table if it's valid
    if (!isLookupValid())
    {
        // construct lookup table
        for (int col = 0; col < m_cols; col++)
        {
            m_lookup[col].reserve(m_rows);
            for (int row = 0; row < m_rows; row++)
            {
                if (m_data[col][row] == true) m_lookup[col].push_back(row);
            }
        }
        for (int col = 0; col < m_cols; col++) m_lookup[col].shrink_to_fit();
    }

    // reduce and sort topology space for faster processing
    reduceSpace();

    cout << endl << "running simplicial complex... rules:" << m_rules << ", threshold:" << m_threshold << ", qcols:" << m_qcols.size() << endl;
    map<short, int>::iterator shape;
    for (int index = (int)m_qcols.size() - 1; index >= 0; index--) {
        short col = m_qcols[index].first;
        string gname = to_string(col);
        Simplex simplex;
        buildSimplex(simplex, gname, 1, m_lookup[col], m_qcols, index + 1);
        connectSimplex(simplex);
        // track time for all shapes for every 10 vertices processed
        if (index == 0 || index == (m_qcols.size() - 1) || (index % 10) == 0) {
            cout << " col " << index << ", shape";
            for (shape = m_results.begin(); shape != m_results.end(); shape++) {
                cout << " " << shape->first << ":" << shape->second;
            }
            cout << endl;
        }
    }
}

bool SimplicialCmplx::readFile(string strFile, int numCols, int numRows)
{
    FILE* fp;
    fp = fopen(strFile.c_str(), "rt");
    if (!fp)
    {
        cout << "Error: Failed to open file for writing. " << strFile << endl;
        return false;
    }

    int length, col;
    for (col = 0; col < numCols; col++) {
        m_lookup[col].reserve(numRows);
    }

    for (int row = 0; row < numRows; row++) {
        fscanf(fp, "%d", &length);
        for (int i = 0; i < length; i++) {
            fscanf(fp, "%d", &col);
            m_data[col][row] = true;
            m_lookup[col].push_back(row);
        }
    }

    for (col = 0; col < numCols; col++) {
        m_lookup[col].shrink_to_fit();
    }

    fclose(fp);

    return true;
}

/*
 * This function run once on the data matrix to reduce the number of columns or 0-simplicies
 * so that the program can operate on reduced topological space. It also sorts the columns
 * depending on the number of 1's appear in each column. This allows the program to run
 * a lot faster because any initial 0-simplex below the threshold will be excluded.
 */
void SimplicialCmplx::reduceSpace()
{
    m_qcols.reserve(m_lookup.size());
    for (int col = 0; col < (int)m_lookup.size(); col++) {
        int count = (int)m_lookup[col].size();
        if (count >= m_thresholdLimit) {
            m_qcols.push_back(pair<short, int>(col, count));
        }
    }
    m_qcols.shrink_to_fit();
    sort(m_qcols.begin(), m_qcols.end(), compareCounts);
}

/*
 * The goal of this function is to build the simplex structure that is required for the algorithm to visit each
 * simplex once, moving from lowest # of 1's to highest. Below is the format of the structure and what is being
 * stored inside it.
 *   Simplex Structure:
 *     1. name of simplex: "0", "0 1", "0 1 2" and etc.
 *     2. # of rules or simplex dimension: 1 is for 0-simplex, 2 is for 1-simplex and so on.
 *     3. indices to all AND'ed ones for this simplex. ex: inverted list={0,1000,65000}.
 *     4. all qualified columns associated with this simplex with all AND'ed indices.
 *          ex: [col=0, inverted list={0,1122,32000,65123}]
 *              [col=4, inverted list={1,1122,32111,65000}]
 *              [col=1256, inverted list={0,32000,65000}]
 *          note: all {col,inverted_list} pairs must qualify the given threshold
 */
void SimplicialCmplx::buildSimplex(Simplex& simplex, string& gname, int nrules, vector<int>& ones, vector<pair<short, int> >& cols, int start)
{
    simplex.gname = gname;
    simplex.nrules = nrules;
    simplex.ones = ones;
    int nlinks = (int)cols.size() - start;
    if (nlinks > 0) {
        simplex.links.reserve(nlinks);
        for (int index = start; index < cols.size(); index++) {
            short col = cols[index].first;
            pair<short, vector<int> > link;
            link.second.reserve(ones.size());
            for (int row = 0; row < ones.size(); row++) {
                if (m_data[col][ones[row]]) {
                    link.second.push_back(ones[row]);
                }
            }
            if (link.second.size() >= m_thresholdLimit) {
                link.first = col;
                link.second.shrink_to_fit();
                simplex.links.push_back(link);
            }
        }
        simplex.links.shrink_to_fit();
    }
}

/*
 * Once the simplex is successfully created by buildSimplex, this function then uses that information 
 * to connect all possible links on topological space to it. However, it must do it in a way that
 * is efficient and avoid reconnecting simplex links by navigating from left-to-right of all the 
 * qualified columns. As it tries to connect each of the simplex dimension, it prints out the simplex
 * name and the large itemsets computed. Once all information are reported for this simplex, it
 * affectively combines the next link to build a higher-dimension simplex and repeat the process.
 *
 * This is also known as finding all the star-neighbors for a given 0-simplex, called 'V' (vertex).
 * Build all the open simplicies that have 'V' as a phase. Note that once completed, all these
 * open simplicies must be removed from 'K'
 */
void SimplicialCmplx::connectSimplex(Simplex& simplex)
{
    m_results[simplex.nrules]++;
    printSimplex(simplex);
    if (simplex.nrules < m_rules) {
        for (int i = 0; i < simplex.links.size(); i++) {
            pair<short, vector<int> >& link = simplex.links[i];
            string gname = simplex.gname + " " + to_string(link.first);
            vector<pair<short, int> > cols;
            cols.reserve(simplex.links.size() - i - 1);
            for (int j = i + 1; j < simplex.links.size(); j++) {
                pair<short, vector<int> >& sublink = simplex.links[j];
                cols.push_back(make_pair(sublink.first, (int)sublink.second.size()));
            }
            Simplex subsimplex;
            buildSimplex(subsimplex, gname, simplex.nrules + 1, link.second, cols, 0);
            connectSimplex(subsimplex);
        }
    }
}

void SimplicialCmplx::printSimplex(Simplex& simplex)
{
    if (brief) {
        return; // do nothing
    }
    if (debug) {
        string inverted = "";
        for (int i = 0; i < simplex.ones.size(); i++) {
            inverted += to_string(simplex.ones[i]) + (i == simplex.ones.size() - 1 ? "" : " ");
        }
        fprintf(m_fpResult, "[%s] {%s}\n", simplex.gname.c_str(), inverted.c_str());
        for (int i = 0; i < simplex.links.size(); i++) {
            pair<short, vector<int> >& link = simplex.links[i];
            string connected = "";
            for (int j = 0; j < link.second.size(); j++) {
                connected += to_string(link.second[j]) + (j == link.second.size() - 1 ? "" : " ");
            }
            fprintf(m_fpResult, " => [%d] {%s}\n", link.first, connected.c_str());
        }
    }
    else {
        fprintf(m_fpResult, "[%s] %ld\n", simplex.gname.c_str(), simplex.ones.size());
    }
}
