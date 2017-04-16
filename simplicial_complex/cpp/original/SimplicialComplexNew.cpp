/*
 * CS298 Thesis Project -- Simplicial Complex Version New
 * David Le (Student ID: 008-144-669)
 * January 18, 2016
 */

#include <algorithm>
#include <map>
#include <vector>
#include <iostream>
#include <sstream>
#include <string>
#include <time.h>
#include <stdio.h>

// #include "windows.h"
// #include "psapi.h"

#undef DUMP_BITMAP
#define BITMAP_FNAME "input_bitmap.txt"

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

vector<vector<bool> > data;         // [col][row#] -- input data matrix
vector<vector<int> > lookup;        // [col][row#] -- inverted list of 1's
vector<pair<short, int> > qcols;    // [simplex, count] -- sorted list of qualified counts
map<short, int> results;            // [simplex, #items]
FILE* fpResult;
int numRules, thresholdLimit;
double runtimeReading, runtimeAlgorithm, runtimeWriting;
long clockStart;
bool brief = false;
bool debug = false;

bool readFile(string strFile, int numCols, int numRows);
void reduceSpace();
bool compareCounts(pair<short, int>& elem1, pair<short, int>& elem2);
void buildSimplex(Simplex& simplex, string& gname, int nrules, vector<int>& ones, vector<pair<short, int> >& cols, int start);
void connectSimplex(Simplex& simplex);
void printSimplex(Simplex& simplex);

/*
 * argument 1: # of association rules
 * argument 2: threshold for qualification
 * argument 3: # of columns
 * argument 4: # of records
 * argument 5: input data file
 * argument 6: show brief summary only
 */
int main (int argc, char* argv[])
{
    cout << "***" << endl;
    cout << "*** CS298 Thesis Project: Advanced Simplicial Complex" << endl;
    cout << "*** San Jose State University" << endl;
    cout << "*** Computer Science Graduate Department" << endl;
    cout << "*** By Dr Ty Lin and David Le" << endl;
    cout << "*** Date: January 18, 2016" << endl;
    cout << "***" << endl << endl;

    if (argc < 6) { 
        cout << "Usage: SimplicialComplex <#rules> <threshold> <#columns> <#records> <data_file> [-brief]" << endl; 
        return 0; 
    }

    numRules = atoi(argv[1]);
    float threshold = (float)atof(argv[2]);
    int numColumns = atoi(argv[3]);
    int numRecords = atoi(argv[4]);
    string inputFile = argv[5];
    for (int i = 6; i < argc; i++) {
        if (strcmp(argv[i], "-brief") == 0) {
            brief = true;
        }
        if (strcmp(argv[i], "-debug") == 0) {
            debug = true;
        }
    }
    if (!brief) {
        fpResult = fopen("results.txt", "wt");
        cout << "Open Output File" << " " << fpResult << endl;
        // if (err) { 
        //     cout << "Error: Failed to open results.txt file for writing." << endl; 
        //     return 0; 
        // }
    }

    data.assign(numColumns, vector<bool>(numRecords, false));
    lookup.assign(numColumns, vector<int>());
    thresholdLimit = (int)(threshold * numRecords);
    thresholdLimit = (thresholdLimit == 0 ? 1 : thresholdLimit);

    cout << "reading data from " << inputFile << "..." << endl;
    readFile(inputFile, numColumns, numRecords);
    clockStart = clock();

    // Save the input data to a bit-map file
#ifdef DUMP_BITMAP
    cout << "writting bit-map..." << endl;
    FILE *p_bitmap_file = NULL;
    p_bitmap_file = fopen(BITMAP_FNAME, "wt");

    for (int i = 0; i < numRecords; i++)
    {
        for (int j = 0; j < numColumns; j++)
        {
            fprintf(p_bitmap_file, "%d ", (int)data[j][i]);
        }
        fprintf(p_bitmap_file, "\n");
    }
    cout << "finish writting bit-map..." << endl;
    fclose(p_bitmap_file);
#endif
    //

    // reduce and sort topology space for faster processing
    reduceSpace();

    // visit each simplex once starting with lowest # of 1's
    long startTrack = clock();
    numRules = min(numRules, numColumns);
    cout << endl << "running simplicial complex... rules:" << numRules << ", threshold:" << threshold << ", qcols:" << qcols.size() << endl;
    map<short, int>::iterator shape;
    for (int index = (int)qcols.size() - 1; index >= 0; index--) {
        short col = qcols[index].first;
        string gname = to_string(col);
        Simplex simplex;
        buildSimplex(simplex, gname, 1, lookup[col], qcols, index + 1);
        connectSimplex(simplex);
        // track time for all shapes for every 10 vertices processed
        if (index == 0 || index == (qcols.size() - 1) || (index % 10) == 0) {
            cout << " col " << index << ", shape";
            for (shape = results.begin(); shape != results.end(); shape++) {
                cout << " " << shape->first << ":" << shape->second;
            }
            cout << " (" << (clock() - startTrack) / 1000.0 << " secs)" << endl; cout.flush();
            startTrack = clock();
        }
    }
    runtimeAlgorithm = (clock() - clockStart) / 1000.0;
    clockStart = clock();

    cout << endl << "writing simplicial complex results..." << endl;
    for (shape = results.begin(); shape != results.end(); shape++) {
        cout << endl << shape->first << "-way support items: " << shape->second << endl;
    }
    if (!brief) {
        cout << endl << "simplicial complex results are written to results.txt." << endl;
        fclose(fpResult);
    }
    runtimeWriting = (clock() - clockStart) / 1000.0;

    // PROCESS_MEMORY_COUNTERS pmc;
    // GetProcessMemoryInfo(GetCurrentProcess(), &pmc, sizeof(pmc));
    // double memUsedMB = (int)((pmc.WorkingSetSize / 1048576.0) * 100) / 100.0;

    // cout << endl;
    // cout << "~~~ time1: reading file takes " << runtimeReading << " secs" << endl;
    // cout << "~~~ time2: simplicial complex takes " << runtimeAlgorithm << " secs" << endl;
    // cout << "~~~ time3: writing results takes " << runtimeWriting << " secs" << endl;
    // cout << endl;
    // cout << "~~~ total memory used: " << memUsedMB << " MB" << endl;
    // cout << endl;
	// system("pause");//TYLIN
    return 1;
}

bool readFile(string strFile, int numCols, int numRows)
{
    clockStart = clock();
    FILE* fp;
    fp = fopen(strFile.c_str(), "rt");
    // if (err) {
    //     cout << "Error: Failed to open file for writing. " << strFile << endl;
    //     return false;
    // }

    int length, col;
    for (col = 0; col < numCols; col++) {
        lookup[col].reserve(numRows);
    }
    
    int max_length = -1;

    for (int row = 0; row < numRows; row++) {
        fscanf(fp, "%d", &length);



        for (int i = 0; i < length; i++) {
            
            fscanf(fp, "%d", &col);
            data[col][row] = true;
            lookup[col].push_back(row);

            if (col > max_length) max_length = col;
        }
    }
    cout << "The max col length: " << max_length << endl;

    for (col = 0; col < numCols; col++) {
        lookup[col].shrink_to_fit();
    }

    fclose(fp);

    runtimeReading = (clock() - clockStart) / 1000.0;

    return true;
}

/*
 * This function run once on the data matrix to reduce the number of columns or 0-simplicies
 * so that the program can operate on reduced topological space. It also sorts the columns
 * depending on the number of 1's appear in each column. This allows the program to run
 * a lot faster because any initial 0-simplex below the threshold will be excluded.
 */
void reduceSpace()
{
    qcols.reserve(lookup.size());
    for (int col = 0; col < (int)lookup.size(); col++) {
        int count = (int)lookup[col].size();
        if (count >= thresholdLimit) {
            qcols.push_back(pair<short, int>(col, count));
        }
    }
    qcols.shrink_to_fit();
    sort(qcols.begin(), qcols.end(), compareCounts);
}

/*
 * Sort by QualifiedCount/ColumnIndex
 */
bool compareCounts(pair<short, int>& elem1, pair<short, int>& elem2)
{
    if (elem1.second != elem2.second) { return (elem1.second < elem2.second); }
    return (elem1.first < elem2.first);
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
void buildSimplex(Simplex& simplex, string& gname, int nrules, vector<int>& ones, vector<pair<short, int> >& cols, int start)
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
                if (data[col][ones[row]]) {
                    link.second.push_back(ones[row]);
                }
            }
            if (link.second.size() >= thresholdLimit) {
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
void connectSimplex(Simplex& simplex)
{
    results[simplex.nrules]++;
    printSimplex(simplex);
    if (simplex.nrules < numRules) {
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

void printSimplex(Simplex& simplex)
{
    if (brief) {
        return; // do nothing
    }
    if (debug) {
        string inverted = "";
        for (int i = 0; i < simplex.ones.size(); i++) {
            inverted += to_string(simplex.ones[i]) + (i == simplex.ones.size() - 1 ? "" : " ");
        }
        fprintf(fpResult, "[%s] {%s}\n", simplex.gname.c_str(), inverted.c_str());
        for (int i = 0; i < simplex.links.size(); i++) {
            pair<short, vector<int> >& link = simplex.links[i];
            string connected = "";
            for (int j = 0; j < link.second.size(); j++) {
                connected += to_string(link.second[j]) + (j == link.second.size() - 1 ? "" : " ");
            }
            fprintf(fpResult, " => [%d] {%s}\n", link.first, connected.c_str());
        }
    }
    else {
        fprintf(fpResult, "[%s] %ld\n", simplex.gname.c_str(), simplex.ones.size());
    }
}
