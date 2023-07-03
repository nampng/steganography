/*
I'll do this one day. Going to do Python first since I like Python.

*/

#include <iostream>
#include <fstream>
#include <string>

using namespace std;

int main()
{
    string inputFileName;
    cin >> inputFileName;

    fstream inputStream{inputFileName, inputStream.binary | inputStream.in};

    if (!inputStream.is_open())
    {
        cout << "Failed to open file " << inputFileName << '\n';
        return 1;
    }

    cout << "Opened " << inputFileName << '\n'; 
   
    inputStream.seekg(0, ios::end); 
    auto size = inputStream.tellg();
   
    cout << "File is size " << size << '\n';

    char data[(int)size];
    
    inputStream.seekg(0, ios::beg);
    inputStream.read(data, size);

    cout << "Done.\n";
    return 0;
}
