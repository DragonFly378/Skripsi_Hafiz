// Struktur Data Node dari piksel
class Node {
    public:
        bool isForeground;
        double foregroundProbability;
        double backgroundProbability;
        vector<GaussianComponent> gmmComponents;
}
