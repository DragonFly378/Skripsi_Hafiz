#include <iostream>
#include <boost/numeric/ublas/matrix.hpp>
#include <boost/numeric/ublas/io.hpp>

int main() {
    // Define the matrices
    boost::numeric::ublas::matrix<double> matrix1(3, 2);
    boost::numeric::ublas::matrix<double> matrix2(2, 3);

    // Assign values to the matrices
    for (std::size_t i = 0; i < matrix1.size1(); ++i) {
        for (std::size_t j = 0; j < matrix1.size2(); ++j) {
            matrix1(i, j) = i + j;
        }
    }

    for (std::size_t i = 0; i < matrix2.size1(); ++i) {
        for (std::size_t j = 0; j < matrix2.size2(); ++j) {
            matrix2(i, j) = i * j;
        }
    }

    // Perform matrix multiplication
    boost::numeric::ublas::matrix<double> result = boost::numeric::ublas::prod(matrix1, matrix2);

    // Print the result
    std::cout << "Matrix 1:\n" << matrix1 << "\n\n";
    std::cout << "Matrix 2:\n" << matrix2 << "\n\n";
    std::cout << "Matrix Multiplication Result:\n" << result << "\n";

    return 0;
}
