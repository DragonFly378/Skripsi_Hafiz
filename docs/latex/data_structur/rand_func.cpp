#include <iostream>
#include <cstdlib>
#include <ctime>
#include <vector>

using namespace std;


int main() {
    // // Mengatur seed acak
    // srand(time(0));

    // // Mendefinisikan ukuran array
    // int rows = 50;

    // // Membuat array dengan bilangan bulat acak antara 0 hingga 4
    // vector<int> arr(rows);
    // for (int i = 0; i < rows; ++i) {
    //     arr[i] = rand() % 5;  // Menghasilkan bilangan acak antara 0 hingga 4
    // }

    // // Menampilkan array
    // for (int i = 0; i < rows; ++i) {
    //     cout << arr[i] << " ";
    // }
    // cout << endl;

    int komponen_gmm = 5;
    int jumlah_fitur = 3;
    vector<int> jumlah_sampel;
    ublas::vector<double> coefs;
    ublas::matrix<double> means;
    ublas::matrix<double> covariances;


    
    covariances = ublas::zero_matrix<double>(komponen_gmm, jumlah_fitur, jumlah_fitur);
    // coefs.resize(komponen_gmm, 0.0);


    for (int k = 0; k < komponen_gmm; ++k) {
        cout << "Covariances for Component " << k << ":" << endl;
        for (int i = 0; i < jumlah_fitur; ++i) {
            for (int j = 0; j < jumlah_fitur; ++j) {
                cout << covariances[k][i][j] << " ";
            }
            cout << endl;
        }
        cout << endl;
    }
    return 0;
}
