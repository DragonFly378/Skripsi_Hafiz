#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>

using namespace std;


vector<int> getAboveThreshold(vector<int> numbers, int threshold) {
  vector<int> res;
  for(int i = 0; i< numbers.size(); i++){
    if (numbers[i] != threshold) {
      numbers.pop_back();
    }else{
      break;
    }
  }
  
  for (int j = 0; j<numbers.size(); j++) {
    cout<< numbers[j] << endl;
  }
}

int main() {
    



    return 0;
}