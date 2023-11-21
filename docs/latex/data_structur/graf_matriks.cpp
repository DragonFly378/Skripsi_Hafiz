#include <iostream>
#include <vector>
#include <random>

int main() {
    const int rows = 5;
    const int cols = 5;

    // Define a random number generator
    std::random_device rd;
    std::mt19937 gen(rd());
    std::uniform_int_distribution<> dis(1, 100); // Change the range as per your requirement

    // Create a 5x5 matrix with random integer values
    std::vector<std::vector<int>> matrix(rows, std::vector<int>(cols));

    // Fill the matrix with random values
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            matrix[i][j] = dis(gen);
        }
    }

    // Display the matrix
    std::cout << "Matrix:" << std::endl;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << matrix[i][j] << "\t";
        }
        std::cout << std::endl;
    }

    // Find neighbors for each index
    std::vector<std::vector<int>> neighbors(rows, std::vector<int>(cols));
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            int count = 0;

            // Loop over the neighboring cells
            for (int x = i - 1; x <= i + 1; ++x) {
                for (int y = j - 1; y <= j + 1; ++y) {
                    if (x >= 0 && x < rows && y >= 0 && y < cols && !(x == i && y == j)) {
                        neighbors[i][j]++;
                    }
                }
            }
        }
    }

    // Display the number of neighbors for each index
    std::cout << "\nNumber of neighbors for each index:" << std::endl;
    for (int i = 0; i < rows; ++i) {
        for (int j = 0; j < cols; ++j) {
            std::cout << neighbors[i][j] << "\t";
        }
        std::cout << std::endl;
    }

    return 0;
}
